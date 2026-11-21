import numpy as np, itertools, sys
n=int(sys.argv[1]); N=2**n
X=np.array(list(itertools.product([1,-1],repeat=n)),dtype=float)
subsets=sorted([S for k in range(n+1) for S in itertools.combinations(range(n),k)],key=len)
deg=np.array([len(S) for S in subsets])
Chi=np.stack([np.prod(X[:,list(S)],axis=1) if S else np.ones(N) for S in subsets],1)
ham=((X[:,None,:]!=X[None,:,:]).sum(2))
rng=np.random.default_rng(int(sys.argv[2]))
worst=-1e9
for t in range(int(sys.argv[3])):
    mode=t%3
    if mode==0: w=rng.exponential(size=N)**rng.uniform(0,4)
    elif mode==1: w=np.exp(rng.normal(scale=3,size=N))
    else: w=np.abs(X@rng.normal(size=n)+rng.normal())+1e-3
    Q,_=np.linalg.qr(np.sqrt(w)[:,None]*Chi)
    M=(Q*(deg-n/2))@Q.T
    for k in range(5):
        h=rng.choice([-1,1],size=N) if k<2 else np.sign(X@rng.normal(size=n)+1e-9)*(np.prod(X,1) if k>2 else 1)
        ne=(h[:,None]!=h[None,:])
        lhs=(M**2)[ne].sum(); rhs=0.25*((ham==1)&ne).sum()
        worst=max(worst,lhs/rhs)
        if lhs>rhs*(1+1e-9): print("VIOLATION mode",mode,"k",k,lhs/rhs)
print("max ratio",worst)
