import json, math
from fractions import Fraction as F
E=json.load(open('encl.json')); P=10**24; Q=10**20
c=F(502,25); th=F(225677,1996332); w=1-th; cm1=c-1; s=cm1+th; r=s/cm1
I={k:(F(v[2],P),F(v[3],P)) for k,v in E.items()}
L2=I['Two']
def add(*ts):  # ts: (coef, interval)
    lo=sum(cf*(iv[0] if cf>0 else iv[1]) for cf,iv in ts); hi=sum(cf*(iv[1] if cf>0 else iv[0]) for cf,iv in ts); return lo,hi
def grid(iv):
    a=math.floor(iv[0]*Q); b=math.ceil(iv[1]*Q)
    if F(a,Q)==iv[0]: pass
    return (a,b)
D={}
D['a']=grid(add((1,I['W2']),(-1,L2)))       # ln w
D['b']=grid(I['R'])                          # ln r
D['c']=grid(add((1,I['S16']),(4,L2)))        # ln s
D['3']=grid(add((1,I['ThreeHalf']),(1,L2)))
D['theta']=grid(add((1,I['Theta16']),(-4,L2)))
D['cc']=grid(add((1,I['C16']),(4,L2)))       # ln c
D['cm1']=grid(add((1,I['Cm116']),(4,L2)))    # ln(c-1)
D['9']=(2*D['3'][0],2*D['3'][1]); D['4']=grid(add((2,L2)))
D['4']=(D['4'][0],D['4'][1])
iv={k:(F(a,Q),F(b,Q)) for k,(a,b) in D.items()}
for k,v in D.items(): print(k,v, v[1]-v[0])
# Gamma*ln4 = w ln w + cm1 ln r + th ln s - th ln9
Gl4=add((w,iv['a']),(cm1,iv['b']),(th,iv['c']),(-th,iv['9']))
Gl=F(663089654688,10**13); Qh=F(4336910345308,10**13); Bh=F(1512054225688,10**11)
print("Gamma lo/ln4hi", float(Gl4[0]/iv['4'][1]), "need >",float(Gl), Gl4[0] > Gl*iv['4'][1])
print("Gamma < 0.0661:", Gl4[1] < F(661,10000)*iv['4'][0])
# q*ln4 = -th ln th - w ln w + th ln9 < Qh ln4
q4=add((-th,iv['theta']),(-w,iv['a']),(th,iv['9']))
print("q ok", q4[1] < Qh*iv['4'][0], float(q4[1]/iv['4'][0]))
b4=add((cm1,iv['3'])); print("B ok", b4[1] < Bh*iv['4'][0])
k4=add((c,iv['cc']),(-cm1,iv['cm1'])); print("kappa ok", k4[1] < F(29,10)*iv['4'][0])
json.dump({k:list(v) for k,v in D.items()},open('derived.json','w'))
