# Rigorous-ish interval check of the finite moment inequality using correctly rounded Decimal ln/exp
from decimal import Decimal as D, getcontext, ROUND_FLOOR, ROUND_CEILING, localcontext
from fractions import Fraction as F
T={8:18910,22:240,36:240}
P={1:27445,2:10400,3:2200,4:4340,5:7760,6:8120,7:765}
PREC=60
def pw_bounds(k,c):  # k^(1-c), c=1-s0 rational
    if k==1: return D(1),D(1)
    with localcontext() as ctx:
        ctx.prec=PREC
        ulp=D(10)**(-(PREC-5))
        lk=D(k).ln(); lo_l, hi_l = lk-ulp, lk+ulp
        cc=D(c.numerator)/D(c.denominator)  # exact enough? add slack
        x_hi=-(cc*lo_l)+ulp; x_lo=-(cc*hi_l)-ulp
        e_hi=x_hi.exp()*(1+ulp); e_lo=x_lo.exp()*(1-ulp)
        return k*e_lo, k*e_hi
def margin(c):
    tl=sum(v*pw_bounds(k,c)[0] for k,v in T.items())
    ph=sum(v*pw_bounds(r,c)[1] for r,v in P.items())
    return tl-ph
for label,c in [("paper s0=1-1/1300",F(1,1300)),("v1 s0=1-2/2597",F(2,2597)),("v2 s0=1-5/6491",F(5,6491)),("v3 s0=1-10/12981",F(10,12981))]:
    print(label, "lower bound of target-paid:", margin(c))
# parameter chain for final choice
s0=1-F(5,6491); u0=1-F(2,2597)
z=(s0+u0)/2; d=1-z; t=z+d**3
print("u0-z",float(u0-z),"d^3",float(d**3),"t<u0",t<u0,"1/(2-u0)=",1/(2-u0),"kappa=",1-1/(2-u0), float(1/(1-1/(2-u0))))
