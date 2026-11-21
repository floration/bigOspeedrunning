import numpy as np, itertools, sys
n=int(sys.argv[1]); N=2**n
X=np.array(list(itertools.product([1,-1],repeat=n)),dtype=float)
subsets=sorted([S for k in range(n+1) for S in itertools.combinations(range(n),k)],key=len)
deg=np.array([len(S) for S in subsets])
Chi=np.stack([np.prod(X[:,list(S)],axis=1) if S else np.ones(N) for S in subsets],1)
ham=((X[:,None,:]!=X[None,:,:]).sum(2))
def ratio(lw,h):
    Q,_=np.linalg.qr(np.exp(lw/2)[:,None]*Chi)
    M=(Q*(deg-n/2))@Q.T
    ne=(h[:,None]!=h[None,:])
    rhs=0.25*((ham==1)&ne).sum()
    if rhs==0: return -1
    return (M**2)[ne].sum()/rhs
rng=np.random.default_rng(int(sys.argv[2]))
glob=0
for restart in range(int(sys.argv[3])):
    lw=rng.normal(scale=rng.uniform(0,5),size=N); h=rng.choice([-1,1],size=N)
    if restart%2: h=np.sign(X@rng.normal(size=n)+0.01)
    cur=ratio(lw,h)
    for it in range(1500):
        lw2=lw.copy(); h2=h.copy()
        if rng.random()<0.25: j=rng.integers(N); h2[j]*=-1
        else: lw2+=rng.normal(scale=rng.choice([0.05,0.5,3]),size=N)*(rng.random(N)<rng.choice([0.1,1]))
        r=ratio(lw2,h2)
        if r>=cur: lw,h,cur=lw2,h2,r
    glob=max(glob,cur); print(restart,round(cur,6),flush=True)
print("max",glob)
