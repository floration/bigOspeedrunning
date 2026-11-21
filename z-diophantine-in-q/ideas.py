import json,sys
from fractions import Fraction
from collections import defaultdict
q=json.load(open(sys.argv[1]+'/quadrics.json'))
R=[]
for r in q['residuals']:
    f=defaultdict(int)
    for t in r['terms']: f[tuple(sorted(t['monomial']))]+=int(t['coefficient'])
    R.append(dict(f))
n=q['variables']
# Idea 1: for variable v, coefficient form of v in each residual: dict over {(): const, (w,):lin}, plus v^2 flag
def vform(f,v):
    form={}; sq=0
    for m,c in f.items():
        k=m.count(v)
        if k==2: sq+=c
        elif k==1:
            rest=tuple(x for x in m if x!=v); form[rest]=form.get(rest,0)+c
    return form,sq
def rank(vecs):
    keys=sorted({k for v in vecs for k in v}); M=[[Fraction(v.get(k,0)) for k in keys] for v in vecs]
    r=0
    for c in range(len(keys)):
        p=next((i for i in range(r,len(M)) if M[i][c]),None)
        if p is None: continue
        M[r],M[p]=M[p],M[r]
        for i in range(len(M)):
            if i!=r and M[i][c]:
                fac=M[i][c]/M[r][c]; M[i]=[a-fac*b for a,b in zip(M[i],M[r])]
        r+=1
    return r
res=[]
for v in range(2,n+1):
    forms=[];sqany=False
    for f in R:
        fo,sq=vform(f,v)
        if sq: sqany=True
        if fo: forms.append(fo)
    if sqany: continue
    rk=rank(forms)
    if rk==1: res.append((v,forms[0]))
print('Idea1: variables with rank-1 coefficient pattern and no square term:',len(res))
for v,fo in res: print('  x%d'%v, fo)
# Idea 3: duplicate definitions: residuals of form a*v + g(others) with v linear and identical g up to scaling
defs=defaultdict(list)
for i,f in enumerate(R):
    for m,c in f.items():
        if len(m)==1:
            v=m[0]
            if sum(1 for mm in f if v in mm)==1:
                g=tuple(sorted((mm,Fraction(cc,c)) for mm,cc in f.items() if mm!=m))
                defs[g].append((v,i))
dups=[d for d in defs.values() if len(d)>1]
print('Idea3: duplicate definitions:',dups)
