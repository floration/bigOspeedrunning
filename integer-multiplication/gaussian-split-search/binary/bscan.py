# GF(2) helper-split scan on the binary word (own code).
import sys,pickle
sys.path.insert(0,'/home/claude/work/binary')
from bchk import *
from collections import defaultdict,Counter
def sub_in(vs,maskG):
    """basis of span(vs) ∩ {v: v & ~maskG == 0}, via elimination on non-G bits first"""
    # reduce: track combos; eliminate on non-G part
    basis=[]  # (key on nonG part, full vector)
    zero=[]
    for v in vs:
        for kb,fv in basis:
            if v & ~maskG & kb: pass
        # standard: reduce by pivot bits on nonG
        x=v
        for piv,fv in basis:
            if x>>piv&1: x^=fv
        ng=x&~maskG
        if ng:
            piv=ng.bit_length()-1
            # keep basis reduced on piv
            basis=[(p,(f^x) if f>>piv&1 else f) for p,f in basis]
            basis.append((piv,x))
        elif x: zero.append(x)
    # zero vectors: reduce to independent
    out=[]
    for z in zero:
        for b in out: z=min(z,z^b)
        if z: out.append(z)
    return out
def scan(d,verbose=True):
    res,w,moves,val,pairs,main=check(d,verbose=False)
    madj,inadj=adjoint(w)
    pub=w.pub
    # adjoint sanity: inadj[i] = outputs containing x_i
    for i in range(pub):
        col=sum(1<<j for j in range(pub) if val[j]>>i&1); assert inadj[i]==col,i
    groups=defaultdict(list)
    for i in range(pub):
        if i not in main and d['start'][i]!=d['final'][i]: groups[(d['start'][i],d['final'][i])].append(i)
    if verbose: print('groups',len(groups),Counter((w.D[a],w.D[z],len(G)) for (a,z),G in groups.items()).most_common(20))
    inp=defaultdict(list); arr=defaultdict(list); dep=defaultdict(list)
    for i in range(pub): inp[d['start'][i]].append(1<<i)
    for t,f,a,b,v in moves: arr[b].append(v); dep[a].append(madj[t])
    out=[]
    for (a,z),G in groups.items():
        mG=sum(1<<i for i in G)
        for c in w.S:
            if not (w.S[a]<w.S[c]<w.S[z]): continue
            if not dep[c]: continue
            U=sub_in(dep[c],mG)
            if not U: continue
            W=sub_in(inp[c]+arr[c],mG)
            if not W: continue
            M=[[bin(x&y).count('1')&1 for y in U] for x in W]
            hit=any(any(r) for r in M)
            out.append(dict(a=a,z=z,c=c,g=len(G),dc=w.D[c],W=len(W),U=len(U),hit=hit,Wv=W,Uv=U))
    return out,res
if __name__=='__main__':
    for p in sys.argv[1:]:
        out,res=scan(load(p))
        print(p,'pairs with both spaces',len(out),'hits',sum(o['hit'] for o in out))
        print(Counter((o['g'],o['dc'],o['W'],o['U']) for o in out).most_common(30))
        for o in out:
            if o['hit']: print({k:v for k,v in o.items() if k not in('Wv','Uv')})
        pickle.dump(out,open(p.split('/')[-1]+'.scan.pkl','wb'))
