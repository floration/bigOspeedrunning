import json,sys,math
from fractions import Fraction as F
src=sys.argv[1]; out=sys.argv[2]
D=json.load(open(src))
P={tuple(k):int(v) for k,v in D['polynomial']}
def prim(P):
    # P has Fraction values -> primitive integers
    L=1
    for v in P.values(): L=L*v.denominator//math.gcd(L,v.denominator)
    g=0
    for v in P.values(): g=math.gcd(g,int(v*L))
    return {k:int(v*L)//g for k,v in P.items()}
def height(P): return max(abs(v) for v in P.values()).bit_length()
def scale(P,j,lam):
    return prim({k:F(v)*lam**k.count(j) for k,v in P.items()})
primes=[2,3,5,7,11,13,17,149]
# add primes of the anchor
primes+= [23,263,337,631,1063,1093,1171,1439,2161,2437,2837,2851,3187,3343,3793]
vars_=sorted(set(x for k in P for x in k)-{1})
log={}
h=height(P); print('start',h,flush=True)
improved=True; rounds=0
while improved and rounds<6:
    improved=False; rounds+=1
    for j in vars_:
        for p in primes:
            for lam in (F(p),F(1,p)):
                Q=scale(P,j,lam); hq=height(Q)
                if hq<h:
                    P,h=Q,hq; improved=True; log.setdefault(j,F(1)); log[j]*=lam
    print('round',rounds,'height bits',h,flush=True)
D['polynomial']=[[list(k),str(v)] for k,v in sorted(P.items())]
D['variable_scalings']={str(j):str(v) for j,v in log.items()}
json.dump(D,open(out,'w'))
print('terms',len(P),'height',h)
