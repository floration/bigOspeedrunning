import numpy as np, itertools, sys
from math import comb
from decomp import *
import decomp
def stats(n,p,d):
    N=2**n
    X=np.array(list(itertools.product([1,-1],repeat=n)),dtype=float)
    pv=p(X); f=np.sign(pv); w=np.abs(pv)
    AS=0
    for i in range(n):
        Y=X.copy();Y[:,i]*=-1
        idx=((Y<0).astype(int)@(2**np.arange(n-1,-1,-1)))
        AS+=np.mean(f!=f[idx])
    subsets=sorted([S for k in range(n+1) for S in itertools.combinations(range(n),k)],key=len)
    deg=np.array([len(S) for S in subsets])
    Chi=np.stack([np.prod(X[:,list(S)],axis=1) if S else np.ones(N) for S in subsets],1)
    Q,_=np.linalg.qr(np.sqrt(w)[:,None]*Chi)
    h=np.prod(X,1)*f
    G=Q.T@(h[:,None]*Q)
    B=np.zeros((n+1,n+1))
    for r in range(n+1):
        for s in range(n+1):
            B[r,s]=(G[np.ix_(deg==s,deg==r)]**2).sum()/N
    D=np.add.outer(np.arange(n+1),np.arange(n+1))-n
    ED2=(B*D**2).sum()
    b=n*comb(n-1,(n-1)//2)/2**n
    supp=D[B>1e-9]
    return AS,ED2,4*d*b,supp.min(),supp.max(),B
rng=np.random.default_rng(int(sys.argv[2]) if len(sys.argv)>2 else 0)
n=int(sys.argv[1])
best={}
for trial in range(int(sys.argv[3]) if len(sys.argv)>3 else 60):
    d=rng.integers(1,4)
    kind=rng.integers(0,3)
    if kind==0: # random gaussian coefficients up to degree d
        terms=[S for k in range(d+1) for S in itertools.combinations(range(n),k)]
        c=rng.normal(size=len(terms))*np.array([rng.exponential() for _ in terms])
        p=lambda X,terms=terms,c=c: sum(ci*(np.prod(X[:,list(S)],1) if S else 1) for ci,S in zip(c,terms))
    elif kind==1: # symmetric: poly in sum with d roots
        roots=rng.normal(scale=np.sqrt(n),size=d)+0.123
        p=lambda X,roots=roots: np.prod([X.sum(1)-r for r in roots],0)
    else: # weighted sum then poly
        a=rng.exponential(size=n); roots=rng.normal(scale=np.sqrt((a**2).sum())*0.7,size=d)+0.0123
        p=lambda X,a=a,roots=roots: np.prod([X@a-r for r in roots],0)
    try: AS,ED2,L,mn,mx,B=stats(n,p,d)
    except Exception as e: continue
    r1=AS/ED2 if ED2>0 else 0; r2=ED2/L
    for key,val in (('AS/ED2',r1),('ED2/4db',r2),('AS/(8db)',AS/(2*L))):
        if val>best.get(key,(0,))[0]: best[key]=(val,d,kind,round(AS,3),round(ED2,3),mn,mx)
for k,v in best.items(): print(k,v)
