# Verify a tricolored packing: lines "x y" (row-1 pos, row-2 pos); first 5 lines are diagonal tags.
import sys
from fractions import Fraction as F
L=int(sys.argv[2]) if len(sys.argv)>2 else 10
P=[tuple(map(int,l.split())) for l in open(sys.argv[1]) if l.strip()]
tags=P[:5]; norm=P[5:]
assert len(norm)==2916 and all(x==y and x<L for x,y in tags)
assert all(x>=L and y>=L for x,y in norm)
K=max(x+y for x,y in P); k=K+1
I=[x for x,_ in norm]; J=[y for _,y in norm]; Lr=[K-x-y for x,y in norm]
assert len(set(I))==2916 and len(set(J))==2916 and len(set(Lr))==2916
assert all(0<=v<k for v in I+J+Lr)
lidx={v:i for i,v in enumerate(Lr)}
bad=0
for a,ia in enumerate(I):
    for b,jb in enumerate(J):
        c=lidx.get(K-ia-jb)
        if c is not None and not (a==b==c): bad+=1
T=[t for t,_ in tags]
for t in T:
    for v in I+J:
        if (K-t-v) in lidx: bad+=1
    for t2 in T:
        if (K-t-t2) in lidx: bad+=1
print('tags',T,'L',L,'k',k,'violations',bad,'k>=2L',k>=2*L)
eta=F(2,249*k+5); print('eta =',eta,float(eta),'vs Blinov x%.4f'%float(eta*50893237))
