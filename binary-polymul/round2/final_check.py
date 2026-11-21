import json,sys
from fractions import Fraction as F
from decimal import Decimal as D, localcontext
d=json.load(open(sys.argv[1])); T={int(k):v for k,v in d['T'].items()}; P={int(k):v for k,v in d['P'].items()}
print("rank mass T,P:",sum(k*v for k,v in T.items()),sum(k*v for k,v in P.items()))
PREC=60
def pw(k,c,up):
    if k==1: return D(1)
    with localcontext() as ctx:
        ctx.prec=PREC; ulp=D(10)**(-(PREC-5))
        lk=D(k).ln(); cc=D(c.numerator)/D(c.denominator)
        x=-(cc*(lk-ulp))+ulp if up else -(cc*(lk+ulp))-ulp
        return k*x.exp()*((1+ulp) if up else (1-ulp))
def margin(c): return sum(v*pw(k,c,False) for k,v in T.items())-sum(v*pw(r,c,True) for r,v in P.items())
f=lambda s: sum(v*k**s for k,v in T.items())-sum(v*r**s for r,v in P.items())
lo,hi=0.99,1.0
for _ in range(100):
    m=(lo+hi)/2; (hi:=m) if f(m)>0 else (lo:=m)
print("s* = 1 - 1/%.5f ; kappa limit 1/%.5f"%(1/(1-hi),(2-hi)/(1-hi)))
def chain(s0,u0,label):
    m=margin(1-s0); z=(s0+u0)/2; dd=1-z; t=z+dd**3; g=1/(2-u0)
    ok = m>0 and t<u0 and s0<u0
    print(label,"s0=1-",1-s0," margin_lower=",float(m)," u0-z=",float(u0-z)," d^3=",float(dd**3)," t<u0:",t<u0," g<",g," kappa=",1-g,"=1/%.4f"%float(1/(1-g)),"OK" if ok else "FAIL")
for a in sys.argv[2:]:
    s0c,u0c,lab=a.split(':'); chain(1-F(s0c),1-F(u0c),lab)
