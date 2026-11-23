from fractions import Fraction as Q
import sys
C=Q(4391986206293,2**50); D=Q(1420718,2**20); eta=Q(1,256); TOP=2**25-1
def up(hs):
    r=Q(0)
    for i,h in enumerate(hs):
        u=min(eta,(249*(C-D/h)+r)/250)
        r=u if i==len(hs)-1 else Q((u*10**21).__floor__()-1,10**21)
    return r
def cuts(hs):
    c=[];p=0
    for h in hs:
        x=max(-(-250*(h+64)//249), h+64+p); c.append(x); p=x
    return c
def ok(hs):
    c=cuts(hs); return all(c[i-1]+2<hs[i] for i in range(1,len(hs)))
def maxnext(prefix,limit):
    lo,hi=8192,limit
    while lo<hi:
        m=(lo+hi+1)//2
        if ok(prefix+[m,TOP]): lo=m
        else: hi=m-1
    return lo
best=(0,)
for h1 in [8192*k for k in range(1,40)]:
    for f in [x/100 for x in range(2,80,3)]:
        pass
# 4-stage: h1,h2 free, h3 = max given prefix
import itertools
for h1 in range(8192,400000,8192):
    for h2 in range(h1*4, 8000000, 131072):
        if not ok([h1,h2]): continue
        h3=maxnext([h1,h2],TOP)
        if h3<=h2: continue
        v=up((h1,h2,h3,TOP))
        if v>best[0]: best=(v,h1,h2,h3)
print(float(best[0]),best[1:])
