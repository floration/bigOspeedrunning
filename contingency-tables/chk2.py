from fractions import Fraction as F
import math
def T(p,U): return F(U*(U+1),2)*(2+F(max(p-1,0)*(U+1)**2,2))
def C(p,U):
    t=T(p,U); return float(t)+(math.sqrt(float(p*p*t))+1)**2
def clog2(n): return (n-1).bit_length()
worst=0
for m in range(0,60):
  for n in range(0,60):
    d=10+(m+1)*(n+1); U=141*d**3//32; L=3*d
    assert 47*(m*n*L)*max(m-1,0)*max(n-1,0) <= 32*(U+1)
    assert 4*d**3<=U
    gap=2*C(m*n,U)*2**clog2(32*d*d)
    assert C(m*n,U) <= d**3*U**4/4
    worst=max(worst,gap/d**17)
print("tuned: max exact 2C/beta / d^17 =",worst, " proven A =",141**4/32**3)
