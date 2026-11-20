import numpy as np, json
from decimal import Decimal as Dm, ROUND_HALF_EVEN
from fl import uv, moments, H2
c=json.load(open('/home/claude/jv1000/subset-sum/selfcontained-2026/certificates/candidate_base.json'))
z=np.load('z1.npy'); names=['tau0','eta','mu','a','gamma','l','p','q_m']
q=lambda v,d: str(Dm(repr(float(v))).quantize(Dm(1).scaleb(-d)))
vals={k:q(v,10) for k,v in zip(names,z)}
vals['gamma']=str(Dm(vals['gamma'])-Dm('3e-10')); vals['p']=q(z[6],8); vals['q_m']=q(z[7],8)
x,u,v=uv([float(t) for t in c['rc']],[float(t) for t in c['sc']],float(c['kappa']))
EPS0=1e-9
for bump in range(0,200):
    t=float(Dm(vals['tau0']))+bump*1e-10
    tv=str(Dm(vals['tau0'])+Dm(bump)*Dm('1e-10'))
    e,mu,a,g,l,p1,p2=[float(vals[k]) for k in names[1:]]
    D=e-float(Dm(vals['eta'])-Dm(tv)) and float(Dm(vals['eta'])-Dm(tv)); G=2*t-e
    m1,m2=moments(x,u,v,p1,p2,D,D/G)
    cs=[H2(2*a)/2-g, t-(l+(H2(a)-g)*mu), t-(1-mu-l+(1-g)*mu), t-(1-mu+(H2(a)+H2(.5-a)-g)*mu-e), 2*t-H2(.5-a)*mu-.5]
    ms=[e-1.1e-8-m1, e-1.1e-8-m2]
    if min(cs)>EPS0+1.5e-10 and min(ms)>1e-9: break
    # note: raising tau0 lowers Delta -> moments improve too
vals['tau0']=tv
print(bump, vals, ['%.3e'%s for s in cs], ['%.3e'%s for s in ms])
out=dict(c); out.update(vals)
out['construction']=c['construction']+'; slack constants tightened (eps=zeta=1e-10, G0=1e10, eps0=1e-9, rho_f=eta-1e-8, rho_c=rho_f-1e-9), scalars re-optimized, filter unchanged'
out['epsilon']='0.0000000001'; out['zeta']='0.0000000001'; out['input_guard_coefficient']='10000000000'
out['rho_f_rule']='eta - 1e-8'; out['rho_c_rule']='rho_f - 1e-9'
for k in ('floating_margins','floating_T'): out.pop(k,None)
json.dump(out,open('candidate_tight.json','w'),indent=1)
print('T =', Dm(tv)+20*Dm('1e-10'))
