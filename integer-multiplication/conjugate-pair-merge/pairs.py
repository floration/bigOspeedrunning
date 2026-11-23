import json,gzip,sys,numpy as np
exec(open('relaxed2.py').read().split('good=[];bad=0')[0])
E=[];Uv=[];H=[]
for t,a,b in hits:
    D=desc(t); ks=[k for k in sched if src[k]==a and k!=t and k not in D]
    sol=solve(Z[[idx[k] for k in ks]].T.copy(),Z[idx[t]].copy())
    if sol is None: continue
    c0,K=sol
    e=(-Z3[idx[t]])%p
    for i,k in enumerate(ks):
        if c0[i]: e=(e+int(c0[i])*Z3[idx[k]])%p
    E.append(e); Uv.append(U[idx[t]][T3]); H.append((t,a,b))
E=np.array(E,dtype=object); Uv=np.array(Uv,dtype=object)
C=(Uv.dot(E.T))%p
print('n',len(H),'diag nonzero',sum(1 for i in range(len(H)) if (1+C[i,i])%p))
pairs=[(H[i],H[k]) for i in range(len(H)) for k in range(i+1,len(H)) if C[i,k]%p and C[k,i]%p]
print('pairs with both cross terms',len(pairs),pairs[:20])
json.dump(pairs,open('pairs5676.json','w'))
