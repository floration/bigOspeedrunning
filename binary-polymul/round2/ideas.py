import math
T0={8:18910,22:240,36:240}
P0={1:27445,2:10400,3:2200,4:4340,5:7760,6:8120,7:765}
def f(s,T,P): return sum(v*k**s for k,v in T.items())-sum(v*r**s for r,v in P.items())
def root(T,P):
    lo,hi=0.0,1.0
    if f(1,T,P)<=0: return None
    for _ in range(200):
        m=(lo+hi)/2
        if f(m,T,P)>0: hi=m
        else: lo=m
    return hi
def kap(T,P):
    s=root(T,P); return None if s is None else (2-s)/(1-s)
print("baseline 1/kappa", kap(T0,P0))
# tensor square: ranks multiply
from collections import Counter
def sq(A):
    C=Counter()
    for a,x in A.items():
        for b,y in A.items(): C[a*b]+=x*y
    return dict(C)
# tensor: target T⊗T, paid? (heuristic) -> same root since f_T^2 - f_P^2 = (f_T-f_P)(f_T+f_P)
# reverse: sensitivity d(1/kappa)/d(count) per paid rank, removing 100 calls
for r in P0:
    P=dict(P0); P[r]-=100; print("remove 100 paid rank",r,"->1/kappa",round(kap(T0,P),2))
for k in T0:
    T=dict(T0); T[k]+=10; print("add 10 target rank",k,"->1/kappa",round(kap(T,P0),2))
# breaking: owned queries free
P=dict(P0); P[1]-=45; P[7]-=45; print("owned free", kap(T0,P))
P=dict(P0); P[7]-=720; print("all 720 inactive rank-7 removed", kap(T0,P))
P=dict(P0); P[7]=0; P[1]-=45; print("both", kap(T0,P))
# what targets for kappa=1/1000 and 1/100: required mass gap
for K in [1000,100]:
    s=1-1/(K-1)
    print("kappa=1/%d needs s*<=%.6f; current f there = %.2f, paid rank-1 calls to remove ~ %.0f"%(K,s,f(s,T0,P0),-f(s,T0,P0)))
print("--- partial-bank hypotheticals")
def K(T,P): 
    k=kap(T,P); return "none" if k is None else round(k,2)
P=dict(P0)
# undo the paper's trick: all 4 banks at all 5 stages -> all 480 outputs rank 36, P7 +480
P=dict(P0); P[7]+=480; print("no partial trick:", K({8:18910,36:480},P))
P=dict(P0); P[7]-=240; print("stage3 also 2 banks:", K({8:18910,15:240,36:240},P))
P=dict(P0); P[7]-=480; print("stages2,3 also 2 banks:", K({8:18910,8.0001:240,36:240},P))
