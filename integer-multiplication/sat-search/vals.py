# forward values u (on inputs) and adjoint z (on outputs) mod p
import numpy as np
from model import *
p=2147483629
from fractions import Fraction
def modq(t):
    q=Fraction(t); return q.numerator%p*pow(q.denominator%p,p-2,p)%p
def compute(w):
    n=len(w['initial']); first=w['first_output']
    forms={k:[(d,modq(c)) for d,c in r] for k,r in w['forms']}
    U={}
    for i in range(n):
        v=np.zeros(n,dtype=np.int64); v[i]=1; U[~i]=v
    for k in w['schedule']:
        v=np.zeros(n,dtype=np.int64)
        for d,c in forms[k]: v=(v+U[d]*c)%p
        U[k]=v
    Z={}
    cons=defaultdict(list)
    for k,r in forms.items():
        for d,c in r: cons[d].append((k,c))
    for i in range(n):
        v=np.zeros(n,dtype=np.int64); v[i]=1; Z[first+i]=v
    order=[k for k in reversed(w['schedule']) if not (first<=k<first+n)]+[~i for i in range(n)]
    for k in order:
        v=np.zeros(n,dtype=np.int64)
        for j,c in cons[k]: v=(v+Z[j]*c)%p
        Z[k]=v
    return U,Z,forms,cons
def rank_dep(vecs):
    """return list of (index, combination) dependencies via gaussian elimination mod p"""
    basis=[]  # (piv, vec, combo dict)
    deps=[]
    for idx,v in enumerate(vecs):
        v=v.copy(); combo={idx:1}
        for piv,b,cb in basis:
            if v[piv]:
                f=v[piv]; v=(v-b*f)%p
                for j,x in cb.items(): combo[j]=(combo.get(j,0)-f*x)%p
        nz=np.flatnonzero(v)
        if len(nz)==0: deps.append({j:x for j,x in combo.items() if x}); continue
        piv=nz[0]; inv=pow(int(v[piv]),p-2,p)
        basis.append((piv,v*inv%p,{j:x*inv%p for j,x in combo.items()}))
    return len(basis),deps
