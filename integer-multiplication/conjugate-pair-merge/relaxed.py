# Gauge-relaxed deletion scan (input gauge on chart-3 fields):
# delete transfer t (a->b) if u_t has no X component and its X-adjoint z_t lies in span{z_j : j formed at a, j!=t}.
import json,gzip,sys,numpy as np,collections
sys.path.insert(0,'/home/claude/cp'); from uz import compute,p
w=json.load(gzip.open(sys.argv[1])); R=compute(w)
U,Z,X,idx,sched=R['U'],R['Z'],R['X'],R['idx'],R['sched']
fin,fo=w['final'],w['first_output']; mv={k:(a,b) for k,a,b in w['moves']}
src={k:(mv[k][0] if k in mv else fin[k-fo]) for k in sched}
at=collections.defaultdict(list)
for k in sched: at[src[k]].append(k)
def left_kernel(A):
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
uX0={k for k in mv if not U[idx[k]][X].any()}
z0={k for k in mv if not Z[idx[k]].any()}
print('transfers',len(mv),'uX0',len(uX0),'z0',len(z0),'both',len(uX0&z0))
hits=[]
for a,ks in at.items():
    if len(ks)<2: continue
    K=left_kernel(Z[[idx[j] for j in ks]])
    for vec in K:
        for i in np.nonzero(vec)[0]:
            t=ks[i]
            if t in mv and t in uX0 and t not in z0: hits.append((t,a,mv[t][1]))
hits=sorted(set(hits))
print('z-dependent charts',sum(1 for a,ks in at.items() if len(ks)>1 and len(left_kernel(Z[[idx[j] for j in ks]]))),'relaxed-deletable (uX0, z!=0)',len(hits),hits[:30])
json.dump(dict(hits=hits,uX0=sorted(uX0),z0=sorted(z0)),open(sys.argv[2],'w'))
