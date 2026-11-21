import json,sys,random
from fractions import Fraction as F
from collections import defaultdict
d=sys.argv[1]
q=json.load(open(d+'/quadrics.json'))['residuals']
R=[]
for r in q:
    f=defaultdict(int)
    for t in r['terms']: f[tuple(sorted(t['monomial']))]+=int(t['coefficient'])
    R.append({k:F(v) for k,v in f.items() if v})
def P_of(rows,w=None):
    S=defaultdict(F)
    for idx,f in enumerate(rows):
        wt=w[idx] if w else 1
        it=list(f.items())
        for a,ca in it:
            for b,cb in it:
                S[tuple(sorted(a+b))]+=wt*ca*cb
    return {k:v for k,v in S.items() if v}
print('orig',len(P_of(R)), 'residual support',sum(map(len,R)))
# greedy pairwise sparsification: replace f_i by f_i - t f_j if it reduces |supp f_i|
rows=[dict(f) for f in R]
changed=True; it=0
while changed and it<20:
    changed=False; it+=1
    for i in range(len(rows)):
        for j in range(len(rows)):
            if i==j: continue
            fi,fj=rows[i],rows[j]
            common=set(fi)&set(fj)
            if not common: continue
            best=None
            for m in common:
                t=fi[m]/fj[m]
                g=dict(fi)
                for k,v in fj.items():
                    g[k]=g.get(k,0)-t*v
                    if g[k]==0: del g[k]
                if len(g)<len(fi) and (best is None or len(g)<len(best)): best=g
            if best is not None: rows[i]=best; changed=True
print('sparsified residual support',sum(map(len,rows)),'P terms',len(P_of(rows)))
json.dump([[ [list(k),str(v)] for k,v in f.items()] for f in rows],open(sys.argv[2],'w'))
