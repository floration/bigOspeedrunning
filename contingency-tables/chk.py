from fractions import Fraction as F
import math
def T(p,U): return F(U*(U+1),2)*(2+F(max(p-1,0)*(U+1)**2,2))
def C(p,U):
    t=T(p,U); return float(t)+(math.sqrt(float(p*p*t))+1)**2
def clog2(n): return (n-1).bit_length()
worst=0;worstunit=0
for m in range(0,60):
  for n in range(0,60):
    d=10+(m+1)*(n+1); U=5*d**3; p=m*n
    beta=F(1,2**clog2(32*d*d))
    gap=2*C(p,U)/float(beta)
    worst=max(worst,gap/d**17)
    assert C(p,U) <= d**3*U**4/4
print("max over m,n<60 of exact 2C/beta / d^17:",worst)
# polynomial lemma check at boundary x=4D^3
for D in [11,12,50,1000]:
    x=4*D**3
    lhs=(D*D+D+1)*(F(x*(x+1),2)*(2+F((D-1)*(x+1)**2,2)))+1+D
    print(D, float(lhs/(F(D**3*x**4,4))))
