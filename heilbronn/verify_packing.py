import sys
from fractions import Fraction as F
S=sorted(map(int,open(sys.argv[1]).read().split()))
assert len(S)==2921 and len(set(S))==2921 and S[0]==0
tags=[x for x in S if x<10]; U=[x for x in S if x>=10]
assert len(tags)==5 and len(U)==2916
k=2*S[-1]+1
V=[k-1-2*u for u in U]; vidx={v:i for i,v in enumerate(V)}
assert all(0<=v<k for v in V) and all(u<k for u in U) and len(vidx)==2916
bad=0
for a,ua in enumerate(U):
    for b,ub in enumerate(U):
        c=vidx.get(k-1-ua-ub)
        if c is not None and not (a==b==c): bad+=1
for t in tags:
    for ua in U:
        if (k-1-t-ua) in vidx: bad+=1
    for t2 in tags:
        if (k-1-t-t2) in vidx: bad+=1
print('tags',tags,'k',k,'violations',bad)
eta=F(2,249*k+5); print('eta =',eta,float(eta),'ratio vs 1/50893237:',float(eta*50893237),'vs 2/100866719:',float(eta/F(2,100866719)))
