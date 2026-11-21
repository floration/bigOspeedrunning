import numpy as np, itertools, sys
n=int(sys.argv[1]); N=2**n
X=np.array(list(itertools.product([1,-1],repeat=n)),dtype=float)
subsets=sorted([S for k in range(n+1) for S in itertools.combinations(range(n),k)],key=len)
deg=np.array([len(S) for S in subsets])
Chi=np.stack([np.prod(X[:,list(S)],axis=1) if S else np.ones(N) for S in subsets],1)
ham=((X[:,None,:]!=X[None,:,:]).sum(2))
L1=-(ham==1).astype(float)*0.25; L1+=np.diag(-L1.sum(1)); P=np.linalg.pinv(L1)
def val(lw):
    Q,_=np.linalg.qr(np.exp(lw/2)[:,None]*Chi); M=(Q*(deg-n/2))@Q.T
    K=M**2; np.fill_diagonal(K,0); Lw=-K+np.diag(K.sum(1))
    return np.linalg.eigvals(P@Lw).real.max()
rng=np.random.default_rng(int(sys.argv[2])); best=0
for r in range(int(sys.argv[3])):
    lw=rng.normal(scale=rng.uniform(0,8),size=N); cur=val(lw)
    for it in range(800):
        l2=lw+rng.normal(scale=rng.choice([0.1,1,4]),size=N)*(rng.random(N)<rng.choice([0.05,0.3,1]))
        v=val(l2)
        if v>=cur: lw,cur=l2,v
    best=max(best,cur); print(r,cur,flush=True)
print("max",best)
