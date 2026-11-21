import json,sys
from sympy import Matrix, zeros
q=json.load(open(sys.argv[1]+'/quadrics.json'))
n=q['variables']
rows=[]
for r in q['residuals']:
    ms=[t['monomial'] for t in r['terms']]
    def vec(m):
        v=[0]*n
        for x in m: v[x-1]+=1
        return v
    v0=vec(ms[0])
    for m in ms[1:]:
        v=vec(m); rows.append([a-b for a,b in zip(v,v0)])
e=[0]*n; e[0]=1; rows.append(e)
M=Matrix(rows)
ns=M.nullspace()
print('dimension of weight space with w1=0:',len(ns))
for v in ns:
    nz={i+1:v[i] for i in range(n) if v[i]!=0}
    print(len(nz), dict(list(nz.items())[:60]))
