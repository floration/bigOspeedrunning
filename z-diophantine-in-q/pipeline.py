import json,sys,random,math
from fractions import Fraction as F
from collections import defaultdict,Counter
d=sys.argv[1]; out=sys.argv[2]; seeds=int(sys.argv[3])
q=json.load(open(d+'/quadrics.json'))
R0=[]
for r in q['residuals']:
    f=defaultdict(int)
    for t in r['terms']: f[tuple(sorted(t['monomial']))]+=int(t['coefficient'])
    R0.append({k:F(v) for k,v in f.items() if v})
def contrib(rows):
    C=defaultdict(dict)
    for i,f in enumerate(rows):
        it=list(f.items())
        for a,ca in it:
            for b,cb in it:
                m=tuple(sorted(a+b)); C[m][i]=C[m].get(i,0)+ca*cb
    for m in C: C[m]={i:v for i,v in C[m].items() if v}
    return C
def count(C,w): return sum(1 for m,dd in C.items() if sum(w[i]*v for i,v in dd.items())!=0)
def sparsify(R,rng):
    rows=[dict(f) for f in R]; n=len(rows)
    changed=True
    while changed:
        changed=False
        order=list(range(n)); rng.shuffle(order)
        for i in order:
            for j in order:
                if i==j: continue
                fi,fj=rows[i],rows[j]; common=set(fi)&set(fj)
                if not common: continue
                best=None
                for m in common:
                    t=fi[m]/fj[m]; g=dict(fi)
                    for k,v in fj.items():
                        g[k]=g.get(k,0)-t*v
                        if g[k]==0: del g[k]
                    if len(g)<len(fi) and (best is None or len(g)<len(best)): best=g
                if best is not None: rows[i]=best; changed=True
    # make primitive integer rows
    outr=[]
    for f in rows:
        L=1
        for v in f.values(): L=L*v.denominator//math.gcd(L,v.denominator)
        g=0
        for v in f.values(): g=math.gcd(g,int(v*L))
        outr.append({k:F(int(v*L)//g) for k,v in f.items()})
    return outr
def weights(C,n):
    cand=Counter()
    for m,dd in C.items():
        if len(dd)==2:
            (i,a),(j,b)=sorted(dd.items())
            if a*b<0: cand[(i,j,F(-a,b))]+=1
    par=list(range(n)); pot=[F(1)]*n
    def find(x):
        if par[x]==x: return x,F(1)
        r,p=find(par[x]); par[x]=r; pot[x]=pot[x]*p; return r,pot[x]
    best=count(C,[F(1)]*n); W=[F(1)]*n
    for (i,j,rt),c in sorted(cand.items(),key=lambda t:-t[1]):
        ri,pi=find(i); rj,pj=find(j)
        if ri==rj: continue
        f=rt*W[i]/W[j]
        W2=[W[x]*f if find(x)[0]==rj else W[x] for x in range(n)]
        c2=count(C,W2)
        if c2<=best:
            best=c2; W=W2; par[rj]=ri; pot[rj]=rt*pi/pj
    return W,best
bestres=None
for s in range(seeds):
    rng=random.Random(s)
    rows=sparsify(R0,rng) if s>0 or True else R0
    C=contrib(rows); n=len(rows)
    W,cnt=weights(C,n)
    print('seed',s,'support',sum(map(len,rows)),'terms unweighted',count(C,[1]*n),'weighted',cnt,flush=True)
    if bestres is None or cnt<bestres[0]: bestres=(cnt,rows,W)
cnt,rows,W=bestres
# build integer P = L * sum W_i f_i^2, primitive
S=defaultdict(F)
for wi,f in zip(W,rows):
    it=list(f.items())
    for a,ca in it:
        for b,cb in it: S[tuple(sorted(a+b))]+=wi*ca*cb
S={k:v for k,v in S.items() if v}
L=1
for v in S.values(): L=L*v.denominator//math.gcd(L,v.denominator)
g=0
for v in S.values(): g=math.gcd(g,int(v*L))
P={k:int(v*L)//g for k,v in S.items()}
vs=set(x for k in P for x in k)
print('FINAL terms',len(P),'deg',max(map(len,P)),'vars',len(vs),'maxbits',max(abs(v) for v in P.values()).bit_length(),'all weights>0',all(w>0 for w in W))
json.dump({'variables':179,'input':1,'weights':[str(w) for w in W],'scale':[L,g],
 'residuals':[[[list(k),str(v)] for k,v in f.items()] for f in rows],
 'polynomial':[[list(k),str(v)] for k,v in sorted(P.items())]},open(out,'w'))
