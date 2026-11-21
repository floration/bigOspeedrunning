from fractions import Fraction as F
import math
def T(p,U): return F(U*(U+1),2)*(2+F(max(p-1,0)*(U+1)**2,2))
def C(p,U):
    t=T(p,U); return float(t)+(math.sqrt(float(p*p*t))+1)**2
def clog2(n): return (n-1).bit_length()
worst=0; minslack=9
for m in range(0,60):
  for n in range(0,60):
    d=10+(m+1)*(n+1); U=30000*d**3//6931; L=3*d
    q=m*n*L; e=max(m-1,0)*max(n-1,0)
    assert 10000*q*e <= 6931*(U+1) and 4*d**3<=U
    # actual growth factor (1+e/(U+1))^q must be <= 2
    g=(1+e/(U+1))**q; assert g<=2, (m,n,g)
    worst=max(worst,2*C(m*n,U)*2**clog2(32*d*d)/d**17)
print("log-scale: max exact/d^17 =",worst," proven A =",32*30000**4/6931**4)
