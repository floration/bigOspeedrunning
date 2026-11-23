from fractions import Fraction as Q
import sys
C=Q(4391986206293,2**50); D=Q(1420718,2**20); eta=Q(1,256)
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
def maxnext(prefix,TOP):
    lo,hi=8192,TOP
    while lo<hi:
        m=(lo+hi+1)//2
        if ok(prefix+[m,TOP]): lo=m
        else: hi=m-1
    return lo
def opt(bits,stages):
    TOP=2**bits-1
    # free heights: stages-2 of them; geometric init
    free=[max(8192,int(TOP/16**(stages-1-i))) for i in range(stages-2)]
    def ev(f):
        if any(x<8192 for x in f) or not ok(f): return Q(0)
        h=maxnext(list(f),TOP)
        if h<=f[-1] if f else False: return Q(0)
        return up(tuple(f)+(h,TOP))
    best=ev(free)
    step=max(1,TOP//64)
    while step>=1:
        imp=True
        while imp:
            imp=False
            for k in range(len(free)):
                for s in (-step,step):
                    t=free[:];t[k]+=s;v=ev(t)
                    if v>best: best,free,imp=v,t,True
        step//=2
    # polish: exhaustive +-s on single coordinates, s in 1..64 powers, until stable
    imp=True
    while imp:
        imp=False
        for s in (64,32,16,8,4,2,1):
            for k in range(len(free)):
                for d in (-s,s):
                    t=free[:];t[k]+=d;v=ev(t)
                    if v>best: best,free,imp=v,t,True
    return best,free
for bits in map(int,sys.argv[1:]):
    for st in (3,4,5):
        b,f=opt(bits,st); print(bits,st,float(b),f,flush=True)
