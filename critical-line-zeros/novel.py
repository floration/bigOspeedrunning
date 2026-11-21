import numpy as np, itertools, sys
from scipy.optimize import minimize
tn,wn=np.polynomial.legendre.leggauss(400); tn=tn/2; wn=wn/2
def setup(Wf):
    W=Wf(tn); I1=W@wn; I2=(W*W)@wn
    D=np.abs(tn[:,None]-tn[None,:]); I3=(W*wn)@D@(W*wn)
    H=2-(I2+I3)/I1**2
    k=lambda x: (np.cos(2*np.pi*np.multiply.outer(x,tn))@(W*wn))/I1
    return H,k
def lim(Wf,mu,R):
    H,k=setup(Wf); best=9
    def e(g):
        p=len(g); G=np.tile(g,R+2); y=np.concatenate([[0],np.cumsum(G)])
        d=np.array([y[i+r]-y[i] for i in range(p) for r in range(1,R)])
        return mu*np.mean(g)+2*np.sum(k(d)**2)/p
    for p in (1,2,3):
        for st in itertools.product([1.04,1.97],repeat=p):
            r=minimize(e,np.array(st),method="Nelder-Mead",options={"xatol":1e-6,"fatol":1e-12})
            best=min(best,r.fun)
    return H,best,(H-mu)/(1-best)
R=10; mu=0.0055
for a,b in [(1.5,0),(1.5,0.2),(1.5,-0.2),(1.4,0.3),(1.6,-0.3),(1.5,0.5),(1.3,0.6)]:
    H,e,L=lim(lambda t: np.cos(a*t)*(1+b*t*t),mu,R)
    print(f"a={a} b={b} H={H:.7f} e={e:.7f} limit={L:.7f}",flush=True)
