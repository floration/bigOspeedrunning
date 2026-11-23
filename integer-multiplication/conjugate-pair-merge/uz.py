import json,gzip,sys,numpy as np,collections,time
from fractions import Fraction
p=2147483629
def modq(t):
    q=Fraction(t); return q.numerator%p*pow(q.denominator%p,p-2,p)%p
def inv_mod(A):
    n=A.shape[0]; M=np.concatenate([A%p,np.eye(n,dtype=np.int64)],1)
    for c in range(n):
        r=c+np.nonzero(M[c:,c])[0][0]
        if r!=c: M[[c,r]]=M[[r,c]]
        M[c]=M[c]*pow(int(M[c,c]),p-2,p)%p
        f=M[:,c].copy(); f[c]=0
        nz=np.nonzero(f)[0]
        if len(nz): M[nz]=(M[nz]-(f[nz,None]*M[c][None,:])%p)%p
    return M[:,n:]
def compute(w,threechart=3):
    ini,fin,fo=w['initial'],w['final'],w['first_output']; n=len(ini)
    forms={k:[(d,modq(c)) for d,c in f] for k,f in w['forms']}
    sched=w['schedule']; idx={k:i for i,k in enumerate(sched)}
    X=np.array([i for i in range(n) if ini[i]!=threechart])
    U=np.zeros((len(sched),n),dtype=np.int64)
    for t,k in enumerate(sched):
        v=np.zeros(n,dtype=np.int64)
        for d,c in forms[k]:
            if d<0: v[~d]=(v[~d]+c)%p
            else: v=(v+U[idx[d]]*c)%p
        U[t]=v
    M=np.array([U[idx[fo+j]] for j in range(n)])
    Minv=inv_mod(M)
    Z=np.zeros((len(sched),len(X)),dtype=np.int64)
    for j in range(n): Z[idx[fo+j]]=Minv[X,j]
    for t in range(len(sched)-1,-1,-1):
        k=sched[t]
        for d,c in forms[k]:
            if d>=0: Z[idx[d]]=(Z[idx[d]]+Z[t]*c)%p
    return dict(forms=forms,sched=sched,idx=idx,X=X,U=U,Z=Z,M=M,Minv=Minv)
def rank_mod(A):
    A=A.copy()%p; r=0; rows,cols=A.shape
    for c in range(cols):
        if r==rows: break
        nz=np.nonzero(A[r:,c])[0]
        if not len(nz): continue
        q=r+nz[0]; A[[r,q]]=A[[q,r]]
        A[r]=A[r]*pow(int(A[r,c]),p-2,p)%p
        f=A[:,c].copy(); f[r]=0; nz=np.nonzero(f)[0]
        if len(nz): A[nz]=(A[nz]-(f[nz,None]*A[r][None,:])%p)%p
        r+=1
    return r
if __name__=='__main__':
    w=json.load(gzip.open(sys.argv[1])); t0=time.time()
    R=compute(w); print('computed',time.time()-t0)
    np.savez_compressed(sys.argv[2],U=R['U'],Z=R['Z'],X=R['X'],sched=np.array(R['sched']))
