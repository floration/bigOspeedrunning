import numpy as np, json
from scipy.optimize import minimize
from fl import uv, moments, H2
c=json.load(open('candidate_tight.json'))
sn=['tau0','eta','mu','a','gamma','l','p','q_m']
s0=np.array([float(c[k]) for k in sn]); W=np.load('w.npy')
s0[6:8]=W[1:3]; kap=W[0]; rc=W[3:35]; sc=W[35:67]
x,u,v=uv(rc,sc,kap,N=16384)
SC=1.2e-9; GAPM=1.3e-8
def cons(y):
    z=s0+1e-6*y; t,e,mu,a,g,l,p1,p2=z; D=e-t; G=2*t-e
    m1,m2=moments(x,u,v,p1,p2,D,D/G)
    return 1e6*np.array([H2(2*a)/2-g-SC, t-(l+(H2(a)-g)*mu)-SC, t-(1-mu-l+(1-g)*mu)-SC,
      t-(1-mu+(H2(a)+H2(.5-a)-g)*mu-e)-SC, 2*t-H2(.5-a)*mu-.5-SC, e-GAPM-m1, e-GAPM-m2])
print('start cons',cons(np.zeros(8))/1e6)
y=np.zeros(8)
for i in range(6):
    r=minimize(lambda y:y[0],y,jac=lambda y:np.eye(8)[0],method='SLSQP',constraints=[{'type':'ineq','fun':cons}],options=dict(ftol=1e-13,maxiter=300))
    if cons(r.x).min()>-1e-6: y=r.x
    print(i,'tau0 %.10f'%(s0[0]+1e-6*y[0]),'minc %.2e'%(cons(y).min()/1e6))
z=s0+1e-6*y; np.save('z_new.npy',z); print(cons(y)/1e6)
