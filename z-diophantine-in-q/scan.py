import json,sys
from collections import defaultdict
q=json.load(open(sys.argv[1]+'/quadrics.json'))
R=[{tuple(sorted(t['monomial'])):int(t['coefficient']) for t in r['terms']} for r in q['residuals']]
occ=defaultdict(list)
for i,f in enumerate(R):
    for m in f:
        for v in set(m): occ[v].append((i,m))
cand=[]
for v,l in occ.items():
    if v==1: continue
    onlylin=all(m==(v,) for i,m in l)
    rows=sorted(set(i for i,m in l))
    if onlylin: cand.append((v,rows))
print('vars appearing only as pure linear term:',len(cand))
for v,rows in cand[:40]: print(v,[q['residuals'][i]['name'] for i in rows])
# variables appearing in only one residual
one=[v for v,l in occ.items() if len(set(i for i,m in l))==1]
print('vars in exactly one residual:',len(one), one[:30])
