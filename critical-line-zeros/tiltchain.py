import numpy as np, itertools, sys
from scipy.integrate import quad
from scipy.optimize import minimize
def Hval(a):
    W=lambda t: np.cos(a*t)
    I1=quad(W,-.5,.5)[0]; I2=quad(lambda t:W(t)**2,-.5,.5)[0]
    inner=lambda s: quad(lambda t:W(t)*(s-t),-.5,s)[0]
    I3=2*quad(lambda s:W(s)*inner(s),-.5,.5,epsabs=1e-13,epsrel=1e-13)[0]
    return 2-(I2+I3)/I1**2
def mk(a):
    t=a/(2*np.pi); n0=0.5*(np.sinc(-t)+np.sinc(t))
    return lambda x: 0.5*(np.sinc(x-t)+np.sinc(x+t))/n0
def e_R(g,k,mu,R):
    p=len(g); G=np.tile(g,R+2); y=np.concatenate([[0],np.cumsum(G)])
    s=0
    for i in range(p):
        for r in range(1,R): s+=k(y[i+r]-y[i])**2
    return mu*np.mean(g)+2*s/p
def lim(a,mu,R):
    H=Hval(a); k=mk(a); best=(9,None)
    for p in (1,2,3,4):
        for st in itertools.product([1.03,1.97],repeat=p):
            r=minimize(lambda g:e_R(g,k,mu,R),np.array(st),method="Nelder-Mead",options={"xatol":1e-7,"fatol":1e-12,"maxiter":4000})
            if r.fun<best[0]: best=(r.fun,r.x)
    e=best[0]; return H,e,(H-mu)/(1-e),best[1]
R=int(sys.argv[1])
for a in [float(v) for v in sys.argv[2].split(',')]:
    for mu in [float(v) for v in sys.argv[3].split(',')]:
        H,e,b,g=lim(a,mu,R); print(f"R={R} a={a:.4f} mu={mu} H={H:.7f} e={e:.7f} limit={b:.7f} g={np.round(g,3)}",flush=True)
