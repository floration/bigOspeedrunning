import numpy as np, json
from decimal import Decimal as Dm
from fl import uv, moments, H2
c=json.load(open('candidate_tight.json')); W=np.load('w.npy'); z=np.load('z_new.npy')
q=lambda v,d: str(Dm(repr(float(v))).quantize(Dm(1).scaleb(-d)))
names=['tau0','eta','mu','a','gamma','l','p','q_m']
vals={k:q(v,10) for k,v in zip(names,z)}; vals['p']=q(z[6],8); vals['q_m']=q(z[7],8)
vals['gamma']=str(Dm(vals['gamma'])-Dm('3e-10'))
kap=q(W[0],10); rc=[q(t,12) for t in W[3:35]]; sc=[q(t,12) for t in W[35:67]]
x,u,v=uv([float(t) for t in rc],[float(t) for t in sc],float(kap),N=16384)
for bump in range(300):
    tv=str(Dm(vals['tau0'])+Dm(bump)*Dm('1e-10')); t=float(tv)
    e,mu,a,g,l,p1,p2=[float(vals[k]) for k in names[1:]]
    D=float(Dm(vals['eta'])-Dm(tv)); G=2*t-e; m1,m2=moments(x,u,v,p1,p2,D,D/G)
    cs=[H2(2*a)/2-g, t-(l+(H2(a)-g)*mu), t-(1-mu-l+(1-g)*mu), t-(1-mu+(H2(a)+H2(.5-a)-g)*mu-e), 2*t-H2(.5-a)*mu-.5]
    ms=[e-1.1e-8-m1, e-1.1e-8-m2]
    if min(cs)>1e-9+1.5e-10 and min(ms)>1e-9: break
vals['tau0']=tv; print(bump,vals,['%.2e'%s for s in cs+ms])
out=dict(c); out.update(vals); out['kappa']=kap; out['rc']=rc; out['sc']=sc
out['construction']=out['construction'].replace('filter unchanged','filter coefficients and kappa re-optimized (12 decimals)')
json.dump(out,open('candidate_final.json','w'),indent=1)
T=Dm(tv)+Dm('2e-9'); print('T',T)
