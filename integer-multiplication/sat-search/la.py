import numpy as np
from fractions import Fraction
P=67108859
def modq(t):
    q=Fraction(t); return q.numerator%P*pow(q.denominator%P,P-2,P)%P
class Basis:
    def __init__(s,n): s.n=n; s.piv=[]; s.M=np.zeros((0,n),dtype=np.int64)
    def reduce(s,v):
        if not s.piv: return v%P
        c=v[s.piv]%P
        return (v - (c@s.M)%P)%P
    def add(s,v):
        r=s.reduce(v); nz=np.flatnonzero(r)
        if len(nz)==0: return False
        j=nz[0]; r=r*pow(int(r[j]),P-2,P)%P
        if s.piv:
            col=s.M[:,j].copy()
            s.M=(s.M - np.outer(col,r)%P)%P
        s.M=np.vstack([s.M,r]); s.piv.append(j); return True
    def contains(s,v): return not s.reduce(v).any()
    def __len__(s): return len(s.piv)
def kernel_combos(R):
    """R: list of vectors (rows). return basis of {x : sum x_i R_i = 0} as list of dict"""
    k=len(R); n=R[0].shape[0] if k else 0
    A=np.array(R,dtype=np.int64).T%P if k else None  # n x k
    # gaussian elimination on A columns
    A=A.copy(); piv_cols=[]; r=0
    rows,cols=A.shape
    for cidx in range(cols):
        nz=np.flatnonzero(A[r:,cidx])
        if len(nz)==0: continue
        i=r+nz[0]; A[[r,i]]=A[[i,r]]
        A[r]=A[r]*pow(int(A[r,cidx]),P-2,P)%P
        f=A[:,cidx].copy(); f[r]=0
        A=(A-np.outer(f,A[r])%P)%P
        piv_cols.append(cidx); r+=1
        if r==rows: break
    free=[c for c in range(cols) if c not in piv_cols]
    out=[]
    for fc in free:
        x=np.zeros(cols,dtype=np.int64); x[fc]=1
        for i,pc in enumerate(piv_cols): x[pc]=(-A[i,fc])%P
        out.append(x)
    return out
