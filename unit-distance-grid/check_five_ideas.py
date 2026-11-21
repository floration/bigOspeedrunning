import numpy as np, sys
sys.argv=['x']; import os; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'check_grid.py')).read().split("if __name__")[0])
rng=np.random.default_rng(7)
# (novel) prolongation: does the second-order system add constraints? only if rank < #rows
for N,j in [(5,5),(7,4),(4,7)]:
    Mx=matrix(rng,sample(rng,'plane',N),sample(rng,'plane',j)); s=np.linalg.svd(Mx,compute_uv=False)
    print('prolongation',N,j,'rows',Mx.shape[0],'rank',(s>1e-9*s[0]).sum())
# (breaking) derivation killing anchor coordinates: U_l = 0 -> drop those columns
for N,j in [(2,5),(3,4),(2,4),(1,5)]:
    for loci in LOCI[:5]:
        P=sample(rng,loci[0],N);Q=sample(rng,loci[1],j);Mx=matrix(rng,P,Q)
        keep=[c for c in range(Mx.shape[1]) if not (c>=3*N and (c-3*N)%3!=2)]
        Mk=Mx[:,keep]; _,s,vh=np.linalg.svd(Mk); r=(s>1e-9*s[0]).sum(); K=vh[r:].conj().T
        # A_i column index in reduced: left blocks unchanged (3i+2); A'_l at 3N+l
        f=any(np.linalg.norm((np.eye(len(keep))[3*i+2]-np.eye(len(keep))[3*N+l])@K)<1e-7 for i in range(N) for l in range(j))
        print('U=0 branch',N,j,loci,'kerdim',len(keep)-r,'forced',f)
