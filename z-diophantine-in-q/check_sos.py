import json,sys
from collections import defaultdict
d=sys.argv[1]
q=json.load(open(d+'/quadrics.json')); p=json.load(open(d+'/polynomial.json'))
def poly(terms):
    r=defaultdict(int)
    for t in terms:
        assert t['parameterPower']==0
        r[tuple(sorted(t['monomial']))]+=int(t['coefficient'])
    return r
S=defaultdict(int); maxdeg=0
for res in q['residuals']:
    f=poly(res['terms']); maxdeg=max(maxdeg,max(len(m) for m in f))
    items=list(f.items())
    for a,ca in items:
        for b,cb in items:
            S[tuple(sorted(a+b))]+=ca*cb
S={k:v for k,v in S.items() if v}
P={k:v for k,v in poly(p['terms']).items() if v}
print('residuals',len(q['residuals']),'max residual deg',maxdeg,'SOS==polynomial:',S==P,'terms',len(P))
