# Relay-pair shortcut test: X: a->b, Y: b->c (both chart-3-only, Y reads X, a<b<c nested).
# Replace by D: a->c (D takes X's form), re-solve chart b's local map, extend chart c to read D.
import json,gzip,sys,numpy as np,collections,random
sys.path.insert(0,'/home/claude/cp'); from uz import compute,p,rank_mod
from graphlib import TopologicalSorter, CycleError
rng=np.random.default_rng(int(sys.argv[3]) if len(sys.argv)>3 else 1)
RANDOM=len(sys.argv)>3
ONLY=set(json.load(open(sys.argv[4]))) if len(sys.argv)>4 else None
def solve(A,b):
    m=A.shape[1]; Mx=np.concatenate([A%p,(b%p)[:,None]],1); r=0; piv=[]
    for c in range(m):
        if r==Mx.shape[0]: break
        nz=np.nonzero(Mx[r:,c])[0]
        if not len(nz): continue
        q=r+nz[0]; Mx[[r,q]]=Mx[[q,r]]; Mx[r]=Mx[r]*pow(int(Mx[r,c]),p-2,p)%p
        f=Mx[:,c].copy(); f[r]=0; nz=np.nonzero(f)[0]
        if len(nz): Mx[nz]=(Mx[nz]-(f[nz,None]*Mx[r][None,:])%p)%p
        piv.append(c); r+=1
    if Mx[r:,m].any(): return None
    x=np.zeros(m,dtype=np.int64)
    free=[c for c in range(m) if c not in set(piv)]
    if RANDOM and free:
        x[free]=rng.integers(0,p,size=len(free),dtype=np.int64)
    for i,c in enumerate(piv):
        x[c]=(int(Mx[i,m])-sum(int(Mx[i,f])*int(x[f]) for f in free if Mx[i,f]))%p if RANDOM else Mx[i,m]
    return x
def proj(V,P): # V: k x d  -> k x m
    out=np.zeros((V.shape[0],P.shape[1]),dtype=np.int64)
    for j in range(V.shape[1]):
        nz=np.nonzero(V[:,j])[0]
        if len(nz): out[nz]=(out[nz]+V[nz,j][:,None]*P[j][None,:])%p
    return out
w=json.load(gzip.open(sys.argv[1])); R=compute(w)
U,Z,X,idx,sched,forms,Minv=R['U'],R['Z'],R['X'],R['idx'],R['sched'],R['forms'],R['Minv']
ini,fin,fo=w['initial'],w['final'],w['first_output']; n=len(ini)
mv={k:(a,b) for k,a,b in w['moves']}; Fr=w['frames']; rk=[len(f) for f in Fr]
def span(B):
    s={0}
    for v in B: s|={o^v for o in s}
    return frozenset(s)
S=[span(f) for f in Fr]
src={k:(mv[k][0] if k in mv else fin[k-fo]) for k in sched}
outs=collections.defaultdict(list)
for k in sched: outs[src[k]].append(k)
ins=collections.defaultdict(list)
for i in range(n): ins[ini[i]].append(~i)
for k,(a,b) in mv.items(): ins[b].append(k)
UX=lambda d: (np.eye(n,dtype=np.int64)[~d][X] if d<0 else U[idx[d]][X])
def ZZ(d):
    if d>=0: return Z[idx[d]]
    i=~d; v=np.zeros(len(X),dtype=np.int64)
    pos=np.nonzero(X==i)[0]
    if len(pos): v[pos[0]]=1
    return v
uX0={k for k in mv if not U[idx[k]][X].any()}
pairs=[]
for y in uX0:
    for x,_ in forms[y]:
        if x in uX0 and x in mv and mv[x][1]==mv[y][0]:
            a,b=mv[x]; c=mv[y][1]
            if (S[a]<S[b]<S[c]) : pairs.append((x,y,a,b,c))
print('nested chart-3 relay pairs',len(pairs),flush=True)
res=[]; stat=collections.Counter()
for x,y,a,b,c in pairs:
    if ONLY is not None and x not in ONLY: continue
    # chart c: z_X in span of z of outs at c (excluding y's descendants handled later)
    Oc=[r for r in outs[c]]
    if not Oc: stat['c: no outs']+=1; continue
    cc=solve(np.array([Z[idx[r]] for r in Oc]).T.copy(), Z[idx[x]].copy())
    if cc is None: stat['c: z_X not in span']+=1; continue
    # chart b: delta K over outs(b)\{y} x ins(b)\{x}
    Rb=[r for r in outs[b] if r!=y]; Ib=[i for i in ins[b] if i!=x]
    Kold_y={d:v for d,v in forms[y]}
    rhs_i=[i for i in Ib if Kold_y.get(i,0)]
    if not Rb or not Ib: stat['b: empty']+=1; continue
    m=min(len(X),len(Ib)+len(Rb)+8); P=rng.integers(0,p,size=(len(X),m),dtype=np.int64)
    Ui=proj(np.array([UX(i) for i in Ib]),P); Zr=proj(np.array([ZZ(r) for r in Rb]),P); zy=proj(Z[idx[y]][None,:],P)[0]
    nr,ni=len(Rb),len(Ib); N=nr*ni
    if N>40000: stat['b: too big']+=1; continue
    A=np.zeros((nr*m+ni*m,N),dtype=np.int64); bb=np.zeros(nr*m+ni*m,dtype=np.int64)
    for r in range(nr):
        for i in range(ni): A[r*m:(r+1)*m, r*ni+i]=Ui[i]
    off=nr*m
    for i in range(ni):
        for r in range(nr): A[off+i*m:off+(i+1)*m, r*ni+i]=Zr[r]
        bb[off+i*m:off+(i+1)*m]=(Kold_y.get(Ib[i],0)*zy)%p
    sol=solve(A,bb)
    if sol is None: stat['b: no local solution']+=1; continue
    stat['local OK']+=1
    res.append(dict(x=x,y=y,a=a,b=b,c=c,g=[rk[b]-rk[a],rk[c]-rk[b]],dK={f'{Rb[r]},{Ib[i]}':int(sol[r*ni+i]) for r in range(nr) for i in range(ni) if sol[r*ni+i]},cc={str(Oc[j]):int(cc[j]) for j in range(len(Oc)) if cc[j]}))
print(dict(stat))
json.dump(res,open(sys.argv[2],'w'))
