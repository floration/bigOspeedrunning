from fractions import Fraction as Q
import sys
B=Q(4391986206293,2**50); GC=Q(17145637307,2**42); ETA=Q(39,10000)
STOP=Q(5,10**18)
def ord_sup(hs,D):
    booked=Q(0)
    for i,h in enumerate(hs):
        up=min(ETA,(249*(B-D/h)+booked)/250)
        if i+1==len(hs): return up
        booked=Q(int(up*10**21)-1,10**21)
def gauss(G,DG): return GC-DG/G
def kappa(hs,G,D,DG): return min(ord_sup(hs,D),gauss(G,DG))-STOP
def clock(hs,G): return 1731+320*sum(hs)+220*G
def best(D,DG,cap,hmax=524288,Gmax=524288,lo=400000):
    # three stage h1=8192, h3=hmax; scan G
    bestv=None
    a,b=lo,Gmax
    # ternary-ish: scan coarse then fine
    def val(G):
        h2=(cap-1731-220*G)//320-8192-hmax
        if not 8192<=h2<=hmax: return None
        return kappa((8192,h2,hmax),G,D,DG),(8192,h2,hmax),G
    # crossing: gauss increasing in G, ord decreasing
    while b-a>1:
        m=(a+b)//2
        v=val(m)
        if v is None or ord_sup(v[1],D)<gauss(m,DG): b=m
        else: a=m
    cands=[val(g) for g in range(a-3,b+4)]
    return max(c for c in cands if c)
if __name__=="__main__":
    DG=Q(64939,524288)
    for D in (Q(11204,8192),Q(11174,8192),Q(11173,8192)):
        k,hs,G=best(D,DG,318292011)
        print(D, float(k), "%.15f"%float(k), hs,G, clock(hs,G))
