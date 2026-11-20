import numpy as np, json, sys, time
from scipy.optimize import minimize
from fl import uv, moments
c=json.load(open(sys.argv[1]))
t,e=float(c['tau0']),float(c['eta']); D=e-t; aG=D/(2*t-e)
w0=np.concatenate([[float(c['kappa']),float(c['p']),float(c['q_m'])],[float(x) for x in c['rc']],[float(x) for x in c['sc']]])
N=8192
def mm(w):
    x,u,v=uv(w[3:35],w[35:67],w[0],N=N)
    return moments(x,u,v,w[1],w[2],D,aG)
m10,m20=mm(w0); print('start',m10-e,m20-e)
# minimize max(m1,m2) smoothly: log-sum-exp with sharpness
K=2e7
def f(w):
    m1,m2=mm(w); a=(m1-e)*K; b=(m2-e)*K; mx=max(a,b)
    return (mx+np.log(np.exp(a-mx)+np.exp(b-mx)))/K*1e6
def g(w,h=1e-7):
    f0=f(w); gr=np.zeros_like(w)
    for i in range(len(w)):
        ww=w.copy(); ww[i]+=h; gr[i]=(f(ww)-f0)/h
    return gr
t0=time.time()
r=minimize(f,w0,jac=g,method='L-BFGS-B',options=dict(maxiter=int(sys.argv[2]),gtol=1e-14,ftol=1e-18))
w=r.x; m1,m2=mm(w)
print(r.message,r.nit,'%.0fs'%(time.time()-t0)); print('end',m1-e,m2-e,'gain in max: %.3e'%(max(m10,m20)-max(m1,m2)))
np.save('w.npy',w)
