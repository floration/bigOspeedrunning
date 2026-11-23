# Exact (rational) build of the five-shortcut word, chart-3 re-encoding, and full exact map check.
import json,gzip,sys,collections,hashlib
from fractions import Fraction as Q
from graphlib import TopologicalSorter
w=json.load(gzip.open('w5674.json.gz')); G=json.load(open('good5674.json'))
CC=[{'95398':{102404:Q(-1,2),102431:Q(1,2),20004:Q(-1),103164:Q(-1)}},
    {'97628':{20003:Q(-1),100537:Q(-1,2),101073:Q(1,2),103478:Q(1,2)}},
    {'95050':{101281:Q(-1,2),101492:Q(1,2),20005:Q(-1),103066:Q(1,2)}},
    {'95056':{99500:Q(1,2),99503:Q(-1,2),20006:Q(-1),102966:Q(-1)}},
    {'96741':{97288:Q(-1,2),102189:Q(1,2),103277:Q(-1,2)}}]
ini,fin,fo=w['initial'],w['final'],w['first_output']; n=len(ini)
forms={k:{d:Q(c) for d,c in f} for k,f in w['forms']}
moves={k:(a,b) for k,a,b in w['moves']}
newlab=max(moves)+1
for t,g in enumerate(G):
    x,y=g['x'],g['y']; assert not g['dK']; D=newlab+t
    cc=CC[t][str(x)]
    forms[D]=dict(forms[x]); moves[D]=(moves[x][0],moves[y][1])
    del forms[x],forms[y],moves[x],moves[y]
    for k in forms: forms[k].pop(x,None); forms[k].pop(y,None)
    for r,v in cc.items(): forms[r][D]=forms[r].get(D,0)+v
def forward(forms):
    deps={k:tuple(d for d in f if d>=0) for k,f in forms.items()}
    order=list(TopologicalSorter(deps).static_order()); val={}
    for k in order:
        v={}
        for d,c in forms[k].items():
            src={~d:Q(1)} if d<0 else val[d]
            for i,x in src.items():
                s=v.get(i,0)+c*x
                if s: v[i]=s
                else: v.pop(i,None)
        val[k]=v
    return [val[fo+j] for j in range(n)],order
orig={k:{d:Q(c) for d,c in f} for k,f in w['forms']}
M,_=forward(orig); F,_=forward(forms)
T3=[i for i in range(n) if ini[i]==3]; S3=set(T3)
diffcols=collections.Counter()
for j in range(n):
    for i in set(M[j])|set(F[j]):
        if M[j].get(i,0)!=F[j].get(i,0): diffcols[i]+=1
bad=[i for i in diffcols if i not in S3]
print('output rows checked',n,'columns differing',len(diffcols),'non-chart-3 differing',len(bad))

Fcol=collections.defaultdict(dict)
for j in range(n):
    for i,v in F[j].items(): Fcol[i][j]=v
def solve_sparse(M,cols):
    # Solve M e = f for f in cols (dict row->val) exactly; M as list of row dicts. Gaussian elim on augmented.
    rows=[dict(r) for r in M]; rhs=[{c:cols[c].get(j,0) for c in cols if cols[c].get(j,0)} for j in range(n)]
    pivrow={}
    colrows=collections.defaultdict(set)
    for j,r in enumerate(rows):
        for i in r: colrows[i].add(j)
    used=set()
    for i in range(n):
        cand=[j for j in colrows[i] if j not in used and rows[j].get(i,0)]
        j=min(cand,key=lambda j:len(rows[j])); used.add(j); pivrow[i]=j
        pv=rows[j][i]
        for j2 in list(colrows[i]):
            if j2==j or j2 in used and False: pass
            if j2==j: continue
            f=rows[j2].get(i,0)
            if not f: continue
            fac=f/pv
            for k,v in rows[j].items():
                x=rows[j2].get(k,0)-fac*v
                if x: rows[j2][k]=x; colrows[k].add(j2)
                else: rows[j2].pop(k,None)
            for k,v in rhs[j].items():
                x=rhs[j2].get(k,0)-fac*v
                if x: rhs[j2][k]=x
                else: rhs[j2].pop(k,None)
    E={c:{} for c in cols}
    for i,j in pivrow.items():
        assert len(rows[j])==1
        for c,v in rhs[j].items(): E[c][i]=v/rows[j][i]
    return E
Ec=solve_sparse(M,{i:Fcol[i] for i in diffcols})
C=sorted(diffcols); Cs=set(C)
for i in C:
    assert all(k in S3 for k in Ec[i]), 'E[X,3] nonzero'
# N = E33 - I on columns C
N={i:{k:v-(1 if k==i else 0) for k,v in Ec[i].items()} for i in C}
N={i:{k:v for k,v in c.items() if v} for i,c in N.items()}
rowsN=set(k for c in N.values() for k in c)
print('E33-I: columns',len(C),'rows touched',len(rowsN),'rows outside C',len(rowsN-Cs))
# W = (I_C + N[C,C])^{-1}, exact dense on |C|
m=len(C); pos={c:t for t,c in enumerate(C)}
A=[[Q(int(r==c)) + N[C[c]].get(C[r],0) for c in range(m)] for r in range(m)]
Aug=[A[r]+[Q(int(r==c)) for c in range(m)] for r in range(m)]
for c in range(m):
    pr=next(r for r in range(c,m) if Aug[r][c]); Aug[c],Aug[pr]=Aug[pr],Aug[c]
    pv=Aug[c][c]; Aug[c]=[v/pv for v in Aug[c]]
    for r in range(m):
        if r!=c and Aug[r][c]:
            f=Aug[r][c]; Aug[r]=[a-f*b for a,b in zip(Aug[r],Aug[c])]
W=[row[m:] for row in Aug]
# G = I - N[:,C] W P_C ; G[i,k] for k in C: delta - sum_c N[C[c]][i] * W[c][pos k]
Gd=collections.defaultdict(dict)
for i in rowsN:
    for kk in range(m):
        s=sum(N[C[c]].get(i,0)*W[c][kk] for c in range(m) if N[C[c]].get(i,0))
        if s: Gd[i][C[kk]]=-s
# precompose: forms reading ~i get extra coefficient a*Gd[i][k] on ~k
nf={k:dict(f) for k,f in forms.items()}; changed=0
for k,f in nf.items():
    add={}
    for d,a in list(f.items()):
        if d<0 and (~d) in Gd:
            for kk,g in Gd[~d].items(): add[~kk]=add.get(~kk,0)+a*g
    if add:
        changed+=1
        for d,v in add.items():
            x=f.get(d,0)+v
            if x: f[d]=x
            else: f.pop(d,None)
print('chart-3 forms re-encoded',changed)
F2,order=forward(nf)
print('EXACT MAP EQUAL:',all(F2[j]==M[j] for j in range(n)))
out=dict(w,forms=[[k,sorted([[d,str(v)] for d,v in f.items()])] for k,f in sorted(nf.items())],
         moves=[[k,a,b] for k,(a,b) in sorted(moves.items())],
         schedule=list(TopologicalSorter({k:tuple(d for d in f if d>=0) for k,f in sorted(nf.items())}).static_order()))
json.dump(out,gzip.open('w5669_shortcut5.json.gz','wt'))
import hashlib
print('moves',len(out['moves']),'sha256',hashlib.sha256(json.dumps(out,sort_keys=True,separators=(',',':')).encode()).hexdigest())
