import numpy as np, json, sys
from scipy.optimize import minimize
from fl import uv, moments, H2
c=json.load(open('/home/claude/jv1000/subset-sum/selfcontained-2026/certificates/candidate_base.json'))
rc=[float(t) for t in c['rc']]; sc=[float(t) for t in c['sc']]; kap=float(c['kappa'])
x,u,v=uv(rc,sc,kap)
SC=float(sys.argv[1]) if len(sys.argv)>1 else 1.2e-9   # C slack target
GAPM=float(sys.argv[2]) if len(sys.argv)>2 else 1.1e-8+2e-9  # eta - log2M target
names=['tau0','eta','mu','a','gamma','l','p','q_m']
z0=np.array([float(c[k]) for k in names])
S=1e6; SZ=1e-6  # scale of moment constraints
def cons(y):
    z=z0+SZ*y
    t,e,mu,a,g,l,p1,p2=z
    D=e-t; G=2*t-e
    m1,m2=moments(x,u,v,p1,p2,D,D/G)
    return np.array([
      H2(2*a)/2-g-SC,
      t-(l+(H2(a)-g)*mu)-SC,
      t-(1-mu-l+(1-g)*mu)-SC,
      t-(1-mu+(H2(a)+H2(.5-a)-g)*mu-e)-SC,
      2*t-H2(.5-a)*mu-.5-SC,
      e-GAPM-m1, e-GAPM-m2])*S
import os
y0=np.load('y.npy') if os.path.exists('y.npy') else np.zeros(8)
res=minimize(lambda y:y[0], y0, method='SLSQP', constraints=[{'type':'ineq','fun':cons}],
             options=dict(ftol=1e-12,maxiter=1000), jac=lambda y:np.eye(8)[0])
print(res.message, res.nit)
y=res.x; z=z0+SZ*y
print({k:'%.12f'%v for k,v in zip(names,z)})
print('cons',cons(y)/S)
print('tau0 %.10f  old %.10f  diff %.3e'%(z[0],z0[0],z[0]-z0[0]))
np.save('z1.npy',z); np.save('y.npy',y)
