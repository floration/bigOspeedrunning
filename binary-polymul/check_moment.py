from decimal import Decimal as D, getcontext
from fractions import Fraction as F
getcontext().prec=100
T={8:18910,22:240,36:240}
P={1:27445,2:10400,3:2200,4:4340,5:7760,6:8120,7:765}
def pw(k,s): return (D(k).ln()*s).exp()
def f(s):
    s=D(s.numerator)/D(s.denominator)
    return sum(v*pw(k,s) for k,v in T.items())-sum(v*pw(r,s) for r,v in P.items())
for name,s0 in [("paper 1-1/1300",F(1)-F(1,1300)),("new 1-2/2597",F(1)-F(2,2597)),("1-1/1299",F(1)-F(1,1299))]:
    print(name, "target-paid =", f(s0))
s0=F(1)-F(2,2597); u0=F(1)-F(1,1299)
z=(s0+u0)/2; d=1-z; t=z+d**3
print("u0-z =",u0-z, "d^3 =",float(d**3), "t<u0:", t<u0)
g=1/(2-t); print("g < 1/(2-u0) = ",1/(2-u0), g<1/(2-u0), "=1-1/1300:", 1/(2-u0)==F(1299,1300))
