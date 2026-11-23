# Delete a set S of transfers, fold each into scalars at its source chart (excluding S and descendants),
# then check M^{-1}F block structure mod p. Returns new forms if OK.
import json,gzip,sys,numpy as np,collections
sys.path.insert(0,'/home/claude/cp'); from uz import compute,p,inv_mod,rank_mod
from graphlib import TopologicalSorter, CycleError
def solve(A,b):
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
    return c0
class W:
    def __init__(s,w):
        s.w=w; s.R=compute(w); R=s.R
        s.U,s.Z,s.X,s.idx,s.sched,s.forms,s.Minv=R['U'],R['Z'],R['X'],R['idx'],R['sched'],R['forms'],R['Minv']
        s.fin,s.fo=w['final'],w['first_output']; s.n=len(w['initial'])
        s.mv={k:(a,b) for k,a,b in w['moves']}
        s.src={k:(s.mv[k][0] if k in s.mv else s.fin[k-s.fo]) for k in s.sched}
        s.readers=collections.defaultdict(list)
        for k in s.sched:
            for d,c in s.forms[k]:
                if d>=0: s.readers[d].append(k)
        Xs=set(s.X.tolist()); s.T3=[i for i in range(s.n) if i not in Xs]
    def desc(s,t):
        o=set(); st=[t]
        while st:
            x=st.pop()
            for r in s.readers[x]:
                if r not in o: o.add(r); st.append(r)
        return o
    def try_delete(s,S):
        S=list(S); bad=set(S)
        for t in S: bad|=s.desc(t)
        nf={k:dict(v) for k,v in s.forms.items()}
        for t in S:
            a=s.src[t]; ks=[k for k in s.sched if s.src[k]==a and k not in bad]
            c0=solve(s.Z[[s.idx[k] for k in ks]].T.copy(),s.Z[s.idx[t]].copy())
            if c0 is None: return None,'not in span'
            tf=dict(s.forms[t])
            for i,j in enumerate(ks):
                if c0[i]:
                    for d,v in tf.items(): nf[j][d]=(nf[j].get(d,0)+int(c0[i])*v)%p
        for t in S:
            del nf[t]
            for r_ in s.readers[t]:
                if r_ in nf: nf[r_].pop(t,None)
        deps={k:tuple(d for d in f if d>=0) for k,f in nf.items()}
        try: order=list(TopologicalSorter(deps).static_order())
        except CycleError: return None,'cycle'
        n=s.n; idx2={k:i for i,k in enumerate(order)}; V=np.zeros((len(order),n),dtype=np.int64)
        for i,k in enumerate(order):
            v=np.zeros(n,dtype=np.int64)
            for d,c in nf[k].items():
                if d<0: v[~d]=(v[~d]+c)%p
                else: v=(v+V[idx2[d]]*c)%p
            V[i]=v
        F=np.array([V[idx2[s.fo+j]] for j in range(n)])
        E=np.zeros((n,n),dtype=np.int64)
        for i in range(n):
            for j in np.nonzero(s.Minv[i])[0]: E[i]=(E[i]+s.Minv[i,j]*F[j])%p
        X,T3=s.X,s.T3
        ok=(np.array_equal(E[np.ix_(X,X)],np.eye(len(X),dtype=np.int64)) and not E[np.ix_(X,T3)].any() and not E[np.ix_(T3,X)].any())
        if not ok: return None,'X blocks broken'
        r=rank_mod(E[np.ix_(T3,T3)])
        if r<len(T3): return None,f'33 rank {r}/{len(T3)}'
        return nf,'OK'
if __name__=='__main__':
    w=json.load(gzip.open(sys.argv[1])); s=W(w); pairs=json.load(open(sys.argv[2]))
    res=[]
    for (t1,a1,b1),(t2,a2,b2) in pairs[:int(sys.argv[3])]:
        nf,msg=s.try_delete([t1,t2]); print(t1,t2,a1,b1,b2,msg,flush=True); res.append((t1,t2,msg))
    json.dump(res,open(sys.argv[4],'w'))
