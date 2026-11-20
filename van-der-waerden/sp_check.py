# Re-implementation of the short-period-runs margins from DaysSky audit_math.py @987c96c
from fractions import Fraction as F
def sp_margins(p):
    a,m,b,d,e,er,g,c,ds=(p[k] for k in "a m b delta eps eps_reg gamma c delta_s".split())
    h=F(1,2)
    return {'short_period_cutoff_below_M':m-a,'global_entropy_less_than_M':m-2*a,'M_sublinear':1-m,
     'flip_probability_decays':b,'run_code_entropy_gap':1-a-b,'affine_norm_entropy_gap':a-b,
     'balance_tolerance_positive':e,'balance_tolerance_below_half':h-e,'nonregular_fraction_positive':er,
     'nonregular_fraction_at_most_half':h-er,'light_threshold_positive':d,'run_light_threshold_positive':ds,
     'run_light_threshold_below_one':1-ds,'outer_color_margin':(h-e)*(1-er)*(1-d)-g,
     'digit_rank_rich_gap':g*b/2-c,'drift_less_than_eta_gap':3-m-a}
def sp_valid(p):
    return all((v>=0 if k=='nonregular_fraction_at_most_half' else v>0) for k,v in sp_margins(p).items())
def check(p,name):
    ok=sp_valid(p); assert 1-p['b']-2*p['a']<0
    print(name,'valid' if ok else 'INVALID','c=',p['c'],float(p['c']),'gb/2=',float(p['gamma']*p['b']/2))
    for k,v in sp_margins(p).items():
        if v<=0: print('  fails',k,v)
    return ok
t=F(1,10**5)
base=dict(a=F(1,2)-t,m=1-t,b=F(1,2)-2*t,delta=t,eps=t,eps_reg=t,delta_s=F(1,2))
base['gamma']=F(49997,100000)
P1=dict(base,c=F(31,250)); P2=dict(base,c=F(1249,10000)); P3=dict(base,c=F(12499,100000))
DS=dict(a=F(49,100),m=F(99,100),b=F(97,200),delta=F(1,200),eps=F(1,200),eps_reg=F(1,200),delta_s=F(1,2),gamma=F(97,200),c=F(1,9))
for p,n in [(DS,'DaysSky 1/9'),(P1,'c=31/250'),(P2,'c=1249/10000'),(P3,'c=12499/100000')]: check(p,n)
# rejection controls on P2
for n,q in [('b=a',dict(P2,b=P2['a'])),('m=2a',dict(P2,m=2*P2['a'])),('c=gb/2',dict(P2,c=P2['gamma']*P2['b']/2)),
            ('gamma at bound',dict(P2,gamma=(F(1,2)-P2['eps'])*(1-P2['eps_reg'])*(1-P2['delta']))),('c=1/8',dict(P2,c=F(1,8)))]:
    assert not sp_valid(q); print('control rejected:',n)
print('params P2:',{k:str(v) for k,v in P2.items()})
