# For each relaxed-deletion hit, test whether some fold choice keeps the chart-3 block invertible.
import json,gzip,sys,numpy as np,collections
sys.path.insert(0,'/home/claude/cp'); from uz import compute,p
w=json.load(gzip.open(sys.argv[1])); hits=json.load(open(sys.argv[2]))['hits']
R=compute(w); U,Z,X,idx,sched,forms,Minv,M=R['U'],R['Z'],R['X'],R['idx'],R['sched'],R['forms'],R['Minv'],R['M']
ini,fin,fo=w['initial'],w['final'],w['first_output']; n=len(ini)
Xs=set(X.tolist()); T3=np.array([i for i in range(n) if i not in Xs])
# full adjoint for recovered chart-3 coords
Z3=np.zeros((len(sched),len(T3)),dtype=np.int64)
for j in range(n): Z3[idx[fo+j]]=Minv[T3,j]
for t in range(len(sched)-1,-1,-1):
    k=sched[t]
    for d,c in forms[k]:
        if d>=0: Z3[idx[d]]=(Z3[idx[d]]+Z3[t]*c)%p
mv={k:(a,b) for k,a,b in w['moves']}
src={k:(mv[k][0] if k in mv else fin[k-fo]) for k in sched}
readers=collections.defaultdict(list)
for k in sched:
    for d,c in forms[k]:
        if d>=0: readers[d].append(k)
def desc(t):
    s=set(); st=[t]
    while st:
        x=st.pop()
        for r in readers[x]:
            if r not in s: s.add(r); st.append(r)
    return s
def solve(A,b):
    # returns particular solution and kernel basis of A c = b (mod p), or None
    m=A.shape[1]; Mx=np.concatenate([A,b[:,None]],1)%p; r=0; piv=[]
    for c in range(m):
        if r==Mx.shape[0]: break
        nz=np.nonzero(Mx[r:,c])[0]
        if not len(nz): continue
        q=r+nz[0]; Mx[[r,q]]=Mx[[q,r]]; Mx[r]=Mx[r]*pow(int(Mx[r,c]),p-2,p)%p
        f=Mx[:,c].copy(); f[r]=0; nz=np.nonzero(f)[0]
        if len(nz): Mx[nz]=(Mx[nz]-(f[nz,None]*Mx[r][None,:])%p)%p
        piv.append(c); r+=1
    if Mx[r:,m].any(): return None
    c0=np.zeros(m,dtype=np.int64)
    for i,c in enumerate(piv): c0[c]=Mx[i,m]
    free=[c for c in range(m) if c not in piv]; K=[]
    for fcol in free:
        v=np.zeros(m,dtype=np.int64); v[fcol]=1
        for i,c in enumerate(piv): v[c]=(-Mx[i,fcol])%p
        K.append(v)
    return c0,K
good=[];bad=0
for t,a,b in hits:
    D=desc(t); ks=[k for k in sched if src[k]==a and k!=t and k not in D]
    if not ks: bad+=1; continue
    sol=solve(Z[[idx[k] for k in ks]].T.copy(),Z[idx[t]].copy())
    if sol is None: bad+=1; continue
    c0,K=sol; u=U[idx[t]][T3]
    g=np.array([int((u*Z3[idx[k]]%p).sum()%p) for k in ks],dtype=object)
    ut=int((u*Z3[idx[t]]%p).sum()%p)
    val=(1+int(sum(int(c0[i])*int(g[i]) for i in range(len(ks))))-ut)%p
    vary=any(int(sum(int(v[i])*int(g[i]) for i in range(len(ks))))%p for v in K)
    if val or vary: good.append((t,a,b,val!=0,vary,len(K)))
    else: bad+=1
print('hits',len(hits),'invertible-fold possible',len(good),'blocked',bad)
print(good[:40])
json.dump(good,open(sys.argv[3],'w'))
