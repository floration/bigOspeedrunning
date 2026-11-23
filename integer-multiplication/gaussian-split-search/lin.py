import numpy as np
from fractions import Fraction
P=2147483629
def fm(q):
    q=Fraction(q); return q.numerator%P*pow(q.denominator%P,P-2,P)%P
def forward(w):
    n=len(w['initial']); forms=dict(w['forms']); val={}
    for k in w['schedule']:
        v=np.zeros(n,dtype=np.int64)
        for d,q in forms[k]:
            if d<0: v[~d]=(v[~d]+fm(q))%P
            else: v=(v+val[d]*fm(q))%P
        val[k]=v
    return val
def adjoint(w):
    n=len(w['initial']); first=w['first_output']; forms=dict(w['forms'])
    cons={}
    for k,row in forms.items():
        for d,q in row:
            if d>=0: cons.setdefault(d,[]).append((k,fm(q)))
    b={}
    for k in reversed(w['schedule']):
        if first<=k<first+n:
            v=np.zeros(n,dtype=np.int64); v[k-first]=1; b[k]=v; continue
        v=np.zeros(n,dtype=np.int64)
        for c,q in cons.get(k,[]): v=(v+b[c]*q)%P
        b[k]=v
    return b
def nullspace(A):
    """left... returns basis of {x: A x = 0} mod P (A: m x n)."""
    A=A.copy()%P; m,n=A.shape; piv=[]; r=0
    for c in range(n):
        if r==m: break
        nz=np.nonzero(A[r:,c])[0]
        if len(nz)==0: continue
        p=r+nz[0]; A[[r,p]]=A[[p,r]]
        A[r]=A[r]*pow(int(A[r,c]),P-2,P)%P
        col=A[:,c].copy(); col[r]=0
        nzr=np.nonzero(col)[0]
        if len(nzr): A[nzr]=(A[nzr]-np.outer(col[nzr],A[r])%P)%P
        piv.append(c); r+=1
    free=[c for c in range(n) if c not in set(piv)]
    basis=[]
    for f in free:
        x=np.zeros(n,dtype=np.int64); x[f]=1
        for i,c in enumerate(piv): x[c]=(-A[i,f])%P
        basis.append(x)
    return basis
def mm(a,B):
    """(a @ B) mod P without int64 overflow (a: vector or matrix rows)."""
    a=np.asarray(a)%P; B=np.asarray(B)%P
    a0=a&0xFFFF; a1=a>>16
    r0=(a0@B)%P; r1=(a1@B)%P
    return (r1*65536+r0)%P
