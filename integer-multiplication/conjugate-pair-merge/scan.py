import json,gzip,sys,numpy as np,collections
sys.path.insert(0,'/home/claude/cp'); from uz import *
w=json.load(gzip.open(sys.argv[1])); R=compute(w)
M,Minv=R['M'],R['Minv']; n=M.shape[0]
print('M Minv ok', np.array_equal((M@Minv)%p if False else None,None) or 'skip')
I=np.zeros((n,n),dtype=np.int64)
for j in range(n): I[j]=(sum(((M[j,i]*Minv[i]) %p) for i in np.nonzero(M[j])[0]))%p
print('identity', np.array_equal(I,np.eye(n,dtype=np.int64)), 'M nnz',np.count_nonzero(M))
U,Z,X,idx=R['U'],R['Z'],R['X'],R['idx']
F=w['frames']
def rk(masks):
    b=[]
    for v in masks:
        for x in b: v=min(v,v^x)
        if v: b.append(v)
    return len(b)
D=[rk(f) for f in F]
def dist(a,b): return rk(F[a]+F[b])-min(D[a],D[b])
mv=w['moves']
uX0=[];z0=[]
for k,a,b in mv:
    u=U[idx[k]][X]; z=Z[idx[k]]
    if not u.any(): uX0.append(k)
    if not z.any(): z0.append(k)
print('moves',len(mv),'uX=0',len(uX0),'z=0',len(z0),'both',len(set(uX0)&set(z0)))
links=collections.defaultdict(list)
for k,a,b in mv: links[(a,b)].append(k)
defU=[];defZ=[]
for (a,b),ks in links.items():
    if len(ks)<2: continue
    Um=U[[idx[k] for k in ks]]; Zm=Z[[idx[k] for k in ks]]
    ru=rank_mod(Um); rz=rank_mod(Zm)
    if ru<len(ks): defU.append(((a,b),ks,ru))
    if rz<len(ks): defZ.append(((a,b),ks,rz,dist(a,b)))
print('links with U-deficit',len(defU),'Z-deficit',len(defZ))
# pairs (u,0)+(0,z) on same link
pair=[]
for (a,b),ks in links.items():
    A=[k for k in ks if k in set(z0)]; B=[k for k in ks if k in set(uX0)]
    if A and B and set(A)!=set(B): pair.append(((a,b),A,B,dist(a,b)))
print('links with z0 and uX0 transfers',len(pair))
json.dump(dict(uX0=uX0,z0=z0,defU=defU,defZ=defZ,pair=pair),open(sys.argv[2],'w'))
