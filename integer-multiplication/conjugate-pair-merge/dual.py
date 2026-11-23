# Adjoint (transpose) redundancy: transfer t leaving chart a is deletable if its full adjoint
# lies in the span of adjoints of other scalars formed at chart a (fold s_t into them).
import json,gzip,sys,numpy as np,collections
sys.path.insert(0,'/home/claude/cp'); from uz import modq,p,rank_mod
w=json.load(gzip.open(sys.argv[1]))
ini,fin,fo=w['initial'],w['final'],w['first_output']; n=len(ini)
forms={k:[(d,modq(c)) for d,c in f] for k,f in w['forms']}
sched=w['schedule']; idx={k:i for i,k in enumerate(sched)}
mv={k:(a,b) for k,a,b in w['moves']}
Zt=np.zeros((len(sched),n),dtype=np.int64)
for j in range(n): Zt[idx[fo+j],j]=1
for t in range(len(sched)-1,-1,-1):
    k=sched[t]
    for d,c in forms[k]:
        if d>=0: Zt[idx[d]]=(Zt[idx[d]]+Zt[t]*c)%p
src={k:(mv[k][0] if k in mv else fin[k-fo]) for k in sched}
at=collections.defaultdict(list)
for k in sched: at[src[k]].append(k)
dead=[k for k in mv if not Zt[idx[k]].any()]
print('adjoint-dead transfers',len(dead))
def reduce(basis,v):
    v=v.copy()
    for piv,b in basis:
        if v[piv]: v=(v-b*v[piv])%p
    return v
def insert(basis,v):
    v=reduce(basis,v); nz=np.nonzero(v)[0]
    if len(nz)==0: return False
    piv=nz[0]; v=v*pow(int(v[piv]),p-2,p)%p; basis.append((piv,v)); return True

def left_kernel(A):
    # rows of A (k x n) mod p; return basis of {c : c A = 0}
    k=A.shape[0]; M=np.concatenate([A%p,np.eye(k,dtype=np.int64)],1); r=0
    for c in range(A.shape[1]):
        if r==k: break
        nz=np.nonzero(M[r:,c])[0]
        if not len(nz): continue
        q=r+nz[0]; M[[r,q]]=M[[q,r]]; M[r]=M[r]*pow(int(M[r,c]),p-2,p)%p
        f=M[:,c].copy(); f[r]=0; nz=np.nonzero(f)[0]
        if len(nz): M[nz]=(M[nz]-(f[nz,None]*M[r][None,:])%p)%p
        r+=1
    return M[r:,A.shape[1]:]
hits=[]; deps=0
for a,ks in at.items():
    if len(ks)<2: continue
    K=left_kernel(Zt[[idx[j] for j in ks]])
    if len(K)==0: continue
    deps+=len(K)
    sup=np.nonzero(K.any(0))[0]
    for i in sup:
        if ks[i] in mv: hits.append((ks[i],a,mv[ks[i]][1]))
print('charts',len(at),'dependencies',deps,'redundant transfers',len(hits),hits[:30])
json.dump(dict(dead=dead,hits=hits),open(sys.argv[2],'w'))
