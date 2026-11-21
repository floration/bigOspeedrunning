import numpy as np, itertools, sys
from math import comb, sqrt, pi
def analyze(n, pfun, d, name):
    N=2**n
    X=np.array(list(itertools.product([1,-1],repeat=n)),dtype=float)
    p=pfun(X); assert np.all(p!=0)
    f=np.sign(p); w=np.abs(p)
    # AS
    AS=0
    for i in range(n):
        Y=X.copy();Y[:,i]*=-1
        idx=((Y<0).astype(int)@(2**np.arange(n-1,-1,-1)))
        AS+=np.mean(f!=f[idx])
    subsets=sorted([S for k in range(n+1) for S in itertools.combinations(range(n),k)],key=len)
    deg=np.array([len(S) for S in subsets])
    Chi=np.stack([np.prod(X[:,list(S)],axis=1) if S else np.ones(N) for S in subsets],1)
    A=np.sqrt(w)[:,None]*Chi
    Q,_=np.linalg.qr(A)
    M=(Q*(deg-n/2))@Q.T
    chi=np.prod(X,1); h=chi*f
    # pair stats
    ham=((X[:,None,:]!=X[None,:,:]).sum(2))
    eq=(h[:,None]==h[None,:])
    M2=M**2
    A0=np.trace(M2); Ah=M2[(ham==1)&eq].sum(); F=M2[ham>=2].sum(); Fh=M2[(ham>=2)&eq].sum()
    Eh=((ham==1)&eq).sum()
    T2=4*(A0+Ah+Fh)
    # coupling
    HQ=h[:,None]*Q
    G=Q.T@HQ  # blocks
    B=np.zeros((n+1,n+1))
    for r in range(n+1):
        for s in range(n+1):
            B[r,s]=(G[np.ix_(deg==s,deg==r)]**2).sum()
    ED2=sum(B[r,s]*(r+s-n)**2 for r in range(n+1) for s in range(n+1))/N
    b=n*comb(n-1,(n-1)//2)/2**n
    print(f"{name} n={n} d={d}: AS={AS:.4f} |Eh|/N={Eh/N:.4f} 4(Ah+A0+F)/N={4*(Ah+A0+F)/N:.4f} 8(Ah+A0)/N={8*(Ah+A0)/N:.4f} 2T2/N={2*T2/N:.4f} 2ED2={2*ED2:.4f} lemma 8db={8*d*b:.4f}")
    print(f"   A0/N={A0/N:.4f} Ah/N={Ah/N:.4f} F/N={F/N:.4f} Fh/N={Fh/N:.4f} offdiag-neighbor-noneq/N={M2[(ham==1)&~eq].sum()/N:.4f}")
    return B
if __name__=="__main__":
    n=int(sys.argv[1])
    analyze(n,lambda X:X.sum(1)+0.0 if n%2 else X.sum(1)+0.5,1,"MAJ")
    analyze(n,lambda X:(X.sum(1))**2-n+0.37*0 - 1.5 if True else 0,2,"|sum|^2 thr")
    rng=np.random.default_rng(1)
    c=rng.normal(size=n); analyze(n,lambda X:X@c,1,"randLTF")
