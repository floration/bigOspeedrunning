from fractions import Fraction as Q
from mpmath import mp, mpf, log, power
mp.dps=40
B=Q(4391986206293,2**50); c=mpf(B.numerator)/B.denominator
d=mpf(2)**-128
def F(L,s):
    L=mpf(L)
    return (mpf(47)/20)*(mpf(256)/255)*(mpf(4097)/4096)*(mpf(1028)/1024)*power(1024*134*L,c)*(1+s/L+d)/((1-10/L)*(1-d)**3)
for s in (8, mpf('7.439580926465596639')):
  best=min(range(2000,40000,2), key=lambda L:F(L,s))
  for L in (18960,best):
    v=F(L,s); D=log(v,2)
    print(float(s),L, float(v), float(D), float(D*8192), float(D*2**20))
print('---')
for s in (mpf(8), mpf(15)/2, mpf('7.44')):
  rng=[L for L in range(1100,40000,2) if F(L,s) < power(2,mpf(11173)/8192)]
  rng2=[L for L in range(1100,40000,2) if F(L,s) < power(2,mpf(11174)/8192)]
  best=min(range(1100,40000,2), key=lambda L:F(L,s))
  print(float(s), best, float(log(F(best,s),2)*8192), (rng[0],rng[-1]) if rng else None, (rng2[0],rng2[-1]))
