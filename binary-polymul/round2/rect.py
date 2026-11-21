import itertools, random, sys
from functools import lru_cache
# roots
roots=[]
for i in range(8):
    for j in range(i+1,8):
        for sg in (1,-1):
            v=[0]*8; v[i]=2; v[j]=2*sg; roots.append(tuple(v))
for bits in range(128):
    w=[0]+[(bits>>k)&1 for k in range(7)]
    if sum(w)%2==0: roots.append(tuple(1-2*x for x in w))
assert len(roots)==120
dot=lambda u,v: sum(a*b for a,b in zip(u,v))
orth=[[ (i!=j and dot(roots[i],roots[j])==0) for j in range(120)] for i in range(120)]
# bases: sparse, x in F2^3 labels coordinate x
idx={r:i for i,r in enumerate(roots)}
def line(v):
    if tuple(v) in idx: return idx[tuple(v)]
    return idx[tuple(-x for x in v)]
bases=[]
for a in range(1,8):
    B=[]
    for x in range(8):
        y=x^a
        if x<y:
            for sg in (1,-1):
                v=[0]*8; v[x]=2; v[y]=2*sg; B.append(line(v))
    bases.append(B)
par=lambda n: bin(n).count('1')%2
simplex=[tuple(par(a&x) for x in range(1,8)) for a in range(8)]
signs=[r for r in range(56,120)]
used=set()
for r in signs:
    if r in used: continue
    w=tuple((1-roots[r][x])//2 for x in range(1,8))
    B=[]
    for c in simplex:
        ww=[0]+[ (p^q) for p,q in zip(w,c)]
        B.append(line([1-2*t for t in ww]))
    used|=set(B); bases.append(B)
assert len(bases)==15 and sorted(sum(bases,[]))==list(range(120))
for B in bases:
    for p in B:
        for q in B:
            if p!=q: assert orth[p][q]
# trees: heap nodes 1..15, node->tuple of positions
def trees_all():
    out=[]; S=set(range(8))
    for A in itertools.combinations(range(8),4):
        if 0 not in A: continue
        Bc=tuple(sorted(S-set(A)))
        def halves(X):
            X=list(X); r=[]
            for p in itertools.combinations(X,2):
                if X[0] in p: r.append((p,tuple(sorted(set(X)-set(p)))))
            return r
        for a1,a2 in halves(A):
            for b1,b2 in halves(Bc):
                leaves=[a1[0],a1[1],a2[0],a2[1],b1[0],b1[1],b2[0],b2[1]]
                out.append(leaves)
    return out
TREES=trees_all(); assert len(TREES)==315
def nodes(leaves):
    n={}
    for k in range(8): n[8+k]=frozenset([leaves[k]])
    for k in range(7,0,-1): n[k]=n[2*k]|n[2*k+1]
    return n
NODES=[nodes(t) for t in TREES]
S=1-1/1298.14
def pen(a,b):
    c=8-a-b
    return a**S+b**S+(c**S if c else 0)-8**S
def solve(X,Y,tx,ty,want_plan=False):
    nx=NODES[tx]; ny=NODES[ty]; BX=bases[X]; BY=bases[Y]
    memo={}
    def dp(s,t):
        if (s,t) in memo: return memo[(s,t)]
        src=[BX[p] for p in nx[s]]; tgt=[BY[p] for p in ny[t]]
        anyp=any(orth[u][v] for u in src for v in tgt)
        if not anyp: memo[(s,t)]=(0.0,None); return memo[(s,t)]
        best=(float('inf'),None)
        if all(orth[u][v] for u in src for v in tgt):
            best=(pen(len(src),len(tgt)),('R',len(src),len(tgt)))
        if s<8:
            c=dp(2*s,t)[0]+dp(2*s+1,t)[0]
            if c<best[0]: best=(c,('S',))
        if t<8:
            c=dp(s,2*t)[0]+dp(s,2*t+1)[0]
            if c<best[0]: best=(c,('T',))
        memo[(s,t)]=best; return best
    v=dp(1,1)[0]
    if not want_plan: return v
    hist={}
    def emit(s,t):
        c,ch=dp(s,t)
        if ch is None: return
        if ch[0]=='R': hist[(ch[1],ch[2])]=hist.get((ch[1],ch[2]),0)+1
        elif ch[0]=='S': emit(2*s,t); emit(2*s+1,t)
        else: emit(s,2*t); emit(s,2*t+1)
    emit(1,1); return v,hist
def profile(tx,ty):
    H={}
    for X in range(15):
        for Y in range(15):
            _,h=solve(X,Y,tx[X],ty[Y],True)
            for k,v in h.items(): H[k]=H.get(k,0)+v
    T={8:0,22:240,36:240}; P={1:1200+45,2:1200,4:1200,7:720+45}
    for (a,b),n in H.items():
        T[8]+=5*n
        for r in (a,b,8-a-b):
            if r: P[r]=P.get(r,0)+5*n
    return H,T,P
def f(s,T,P): return sum(v*k**s for k,v in T.items())-sum(v*r**s for r,v in P.items())
def root(T,P):
    lo,hi=0.0,1.0
    if f(1,T,P)<=0: return None
    for _ in range(100):
        m=(lo+hi)/2
        if f(m,T,P)>0: hi=m
        else: lo=m
    return hi
