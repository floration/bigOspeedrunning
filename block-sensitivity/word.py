import sys,random,time,json; sys.path.insert(0,'.')
from fast import *
from math import exp,log
def growth_word(steps,n,iters=150):
    # steps: list of (stepfn, C, K)
    Z=[[1.0 if i<=j else 0.0 for j in range(n)] for i in range(n)]; Y=[r[:] for r in Z]
    tot=0.0;cnt=0
    for it in range(iters):
        for (st,C,K) in steps: Z,Y=st(C,Z,Y,n)
        h=max(max(max(r) for r in Z),max(max(r) for r in Y))
        if it>=iters//2: tot+=log(h);cnt+=1
        Z=[[x/h for x in r] for r in Z];Y=[[x/h for x in r] for r in Y]
    return sum(log(K) for _,_,K in steps)/(tot/cnt)
