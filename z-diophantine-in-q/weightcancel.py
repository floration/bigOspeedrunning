import json,sys
from fractions import Fraction as F
from collections import defaultdict,Counter
d=sys.argv[1]
q=json.load(open(d+'/quadrics.json'))['residuals']
R=[]
for r in q:
    f=defaultdict(int)
    for t in r['terms']: f[tuple(sorted(t['monomial']))]+=int(t['coefficient'])
    R.append(dict(f))
C=defaultdict(dict)
for i,f in enumerate(R):
    it=list(f.items())
    for a,ca in it:
        for b,cb in it:
            m=tuple(sorted(a+b)); C[m][i]=C[m].get(i,0)+ca*cb
for m in C: C[m]={i:v for i,v in C[m].items() if v}
def count(w):
    return sum(1 for m,dd in C.items() if sum(w[i]*v for i,v in dd.items())!=0)
n=len(R); w=[F(1)]*n
base=count(w); print('unweighted terms',base)
# candidate ratios from two-row mixed monomials: w_j/w_i = -c_i/c_j
cand=Counter()
for m,dd in C.items():
    if len(dd)==2:
        (i,a),(j,b)=sorted(dd.items())
        if a*b<0: cand[(i,j,F(-a,b))]+=1
# union-find with potentials: w_j = ratio * w_i
par=list(range(n)); pot=[F(1)]*n   # w_x = pot[x]*w_root
def find(x):
    if par[x]==x: return x,F(1)
    r,p=find(par[x]); par[x]=r; pot[x]=pot[x]*p; return r,pot[x]
for (i,j,rt),c in sorted(cand.items(),key=lambda t:-t[1]):
    ri,pi=find(i); rj,pj=find(j)
    if ri==rj: continue
    # want w_j = rt*w_i : pj*w_rj = rt*pi*w_ri -> w_rj = rt*pi/pj * w_ri
    par[rj]=ri; pot[rj]=rt*pi/pj
W=[find(x)[1] for x in range(n)]
print('greedy weighted terms',count(W))
# local improvement: try each candidate ratio set individually on top (accept if better)
best=count(W)
import itertools
improved=True
while improved:
    improved=False
    for (i,j,rt),c in cand.items():
        # set group of j to match: scale all rows sharing root with j
        rj=find(j)[0]; ri=find(i)[0]
        if ri==rj: continue
        f=rt*W[i]/W[j]
        W2=[W[x]*f if find(x)[0]==rj else W[x] for x in range(n)]
        c2=count(W2)
        if c2<best:
            best=c2; W=W2; par[rj]=ri; improved=True
print('final weighted terms',best)
json.dump([str(x) for x in W],open(sys.argv[2],'w'))
