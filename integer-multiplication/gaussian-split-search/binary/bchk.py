# Own GF(2) checker for the binary strong-bit word (reads the word as data only).
# Values are Python ints: bit i = input x_i. Adjoints: bit j = output j.
import json,gzip,sys,math
from collections import Counter,defaultdict
CALLS=36
CALLER_PAID={1:444,7:444,**{k:444 for k in range(14,57,7)}}
CALLER_TG={8:444,**{k:444 for k in range(15,65,7)},127:222}
def load(p): return json.load(gzip.open(p)) if p.endswith('.gz') else json.load(open(p))
def rowmask(r): return sum((b&1)<<i for i,b in enumerate(r))
def span(vs):
    s={0}
    for v in vs: s|={o^v for o in s}
    return frozenset(s)
def rank(vs):
    basis=[]
    for v in vs:
        for b in basis: v=min(v,v^b)
        if v: basis.append(v)
    return len(basis)
class Word:
    def __init__(s,d):
        s.d=d; s.pub=d['public']; F=d['frames']
        s.S={int(k):span([rowmask(r) for r in v['B']]) for k,v in F.items()}
        s.D={int(k):v['dim'] for k,v in F.items()}
        for k in s.S: assert len(s.S[k])==2**s.D[k],k
    def grade(s,a,b):
        A,B=s.S[a],s.S[b]
        assert A<B or B<A,('nest',a,b)
        return abs(s.D[a]-s.D[b])
def replay(w):
    """forward replay with locality checks; returns list of move records and final values"""
    d=w.d; pub=w.pub
    loc=dict(enumerate(d['start'])); val={i:1<<i for i in range(pub)}
    moves=[]  # (t,field,a,b,value)
    dirty=0
    for t,ins in enumerate(d['program']):
        op=ins[0]
        if op=='INIT': assert ins[1] not in loc; loc[ins[1]]=ins[2]; val[ins[1]]=0
        elif op=='ADD':
            y,x,c=ins[1:]; assert loc[y]==loc[x]==c,('loc',t); assert x!=y; val[y]^=val[x]
        elif op=='MOVE':
            f,a,b=ins[1:]; assert loc[f]==a,('mvloc',t); assert a!=b
            moves.append((t,f,a,b,val[f])); loc[f]=b
        elif op=='SWAP':
            a,b=ins[1:]; loc[a],loc[b]=loc[b],loc[a]; val[a],val[b]=val[b],val[a]
        elif op=='CLEAR':
            f,c=ins[1:]; assert loc[f]==c; dirty+=val[f]!=0; loc.pop(f); val.pop(f)
        else: raise ValueError(op)
    return moves,val,loc,dirty
def adjoint(w):
    """backward pass: adjoint (output mask) of each MOVE (by program index) and of each input"""
    d=w.d; pub=w.pub; prog=d['program']
    adj=defaultdict(int)
    for i in range(pub): adj[i]=1<<i
    madj={}
    for t in range(len(prog)-1,-1,-1):
        ins=prog[t]; op=ins[0]
        if op=='ADD': adj[ins[2]]^=adj[ins[1]]
        elif op=='MOVE': madj[t]=adj[ins[1]]
        elif op=='SWAP': a,b=ins[1:]; adj[a],adj[b]=adj[b],adj[a]
        elif op=='CLEAR': adj[ins[1]]=0
        elif op=='INIT': adj[ins[1]]=0
    inadj={i:adj[i] for i in range(pub)}
    return madj,inadj
def expected_from_outputs(val,pub):
    pairs=[]; main=set()
    for j in range(pub):
        v=val[j]; assert v>>j&1
        sup=[i for i in range(pub) if v>>i&1]
        assert len(sup) in (1,2)
        if len(sup)==2: x=[i for i in sup if i!=j][0]; pairs.append((x,j)); main|={x,j}
    return pairs,main
def histograms(w,moves,main):
    paid=Counter(); tg=Counter()
    for t,f,a,b,v in moves: paid[w.grade(a,b)]+=1
    for i in range(w.pub):
        if i not in main:
            a,z=w.d['start'][i],w.d['final'][i]
            tg[w.grade(a,z)]+=1 if a!=z else 0
    return paid,tg
def allcalls(paid,tg):
    P=Counter({k:CALLS*v for k,v in paid.items()}); T=Counter({k:CALLS*v for k,v in tg.items()})
    P.update(CALLER_PAID); T.update(CALLER_TG); return P,T
def root(P,T,lo=0.0,hi=0.02):
    from decimal import Decimal as Dm,getcontext
    getcontext().prec=50
    L={k:Dm(k).ln() for k in set(P)|set(T)}
    f=lambda c:sum(n*((1-c)*L[k]).exp() for k,n in T.items())-sum(n*((1-c)*L[k]).exp() for k,n in P.items())
    lo,hi=Dm(lo),Dm(hi); s=f(lo)>0; assert s!=(f(hi)>0)
    for _ in range(120):
        m=(lo+hi)/2
        if (f(m)>0)==s: lo=m
        else: hi=m
    return float(lo),lo
def check(d,expect_pairs=None,verbose=True):
    w=Word(d); moves,val,loc,dirty=replay(w)
    pub=w.pub
    for i in range(pub): assert loc[i]==d['final'][i],('final loc',i)
    pairs,main=expected_from_outputs(val,pub)
    if expect_pairs is not None: assert sorted(pairs)==sorted(expect_pairs),'map changed'
    paid,tg=histograms(w,moves,main)
    P,T=allcalls(paid,tg); r,_=root(P,T)
    res=dict(moves=len(moves),dirty=dirty,pairs=len(pairs),paid=dict(sorted(paid.items())),tg=dict(sorted(tg.items())),
             n_paid=sum(P.values()),n_tg=sum(T.values()),lin_paid=sum(k*v for k,v in P.items()),lin_tg=sum(k*v for k,v in T.items()),root=r)
    if verbose: print(res)
    return res,w,moves,val,pairs,main
if __name__=='__main__':
    for p in sys.argv[1:]: print(p); check(load(p))
