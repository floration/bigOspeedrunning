import numpy as np, itertools, sys
n=int(sys.argv[1]); N=2**n
X=np.array(list(itertools.product([1,-1],repeat=n)),dtype=float)
subsets=sorted([S for k in range(n+1) for S in itertools.combinations(range(n),k)],key=len)
deg=np.array([len(S) for S in subsets])
Chi=np.stack([np.prod(X[:,list(S)],axis=1) if S else np.ones(N) for S in subsets],1)
ham=((X[:,None,:]!=X[None,:,:]).sum(2))
L1=-(ham==1).astype(float)*0.25; L1+=np.diag(-L1.sum(1))
rng=np.random.default_rng(int(sys.argv[2])); worst=-1
for t in range(int(sys.argv[3])):
    w=np.exp(rng.normal(scale=rng.uniform(0,6),size=N))
    Q,_=np.linalg.qr(np.sqrt(w)[:,None]*Chi)
    M=(Q*(deg-n/2))@Q.T
    K=M**2; np.fill_diagonal(K,0); Lw=-K+np.diag(K.sum(1))
    ev=np.linalg.eigvalsh(L1-Lw)
    # generalized: max eig of Lw relative to L1 on complement of constants
    evals=np.linalg.eigvals(np.linalg.pinv(L1)@Lw).real.max()
    worst=max(worst,evals); 
print("max generalized eig Lw vs L1:",worst, " (>1 means PSD comparison fails)")
# adversarial: perturb log-weights to maximize generalized eigenvalue
