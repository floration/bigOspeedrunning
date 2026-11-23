import json,gzip,sys
from fractions import Fraction
from collections import defaultdict
import numpy as np
p=2147483629
def modq(t):
    q=Fraction(t); return q.numerator%p*pow(q.denominator%p,p-2,p)%p
def load(path):
    w=json.load(gzip.open(path))
    starts,ends,first=w['initial'],w['final'],w['first_output']; n=len(starts)
    moves={k:(a,b) for k,a,b in w['moves']}; forms=dict((k,f) for k,f in w['forms'])
    val={}; chart={}
    for i in range(n):
        v=np.zeros(n,dtype=np.int64); v[i]=1; val[~i]=v; chart[~i]=starts[i]
    src={}
    for k in w['schedule']:
        s=moves[k][0] if k in moves else ends[k-first]; src[k]=s
        v=np.zeros(n,dtype=np.int64)
        for d,c in forms[k]:
            assert chart[d]==s,(k,d)
            v=(v+val[d]*modq(c))%p
        val[k]=v
        chart[k]=moves[k][1] if k in moves else s
    return w,moves,forms,val,chart,src
def rank(vecs):
    if not vecs: return 0
    M=np.array(vecs,dtype=np.int64)%p
    r=0; rows,cols=M.shape
    for c in range(cols):
        piv=None
        for i in range(r,rows):
            if M[i,c]: piv=i;break
        if piv is None: continue
        M[[r,piv]]=M[[piv,r]]
        inv=pow(int(M[r,c]),p-2,p); M[r]=M[r]*inv%p
        nz=np.nonzero(M[:,c])[0]
        for i in nz:
            if i!=r: M[i]=(M[i]-M[i,c]*M[r])%p
        r+=1
        if r==rows: break
    return r

def nullvec(M):
    # right kernel of M (rows x m) mod p, return list of basis vectors
    M=np.array(M,dtype=np.int64)%p; rows,m=M.shape; piv=[]; r=0
    for c in range(m):
        pr=None
        for i in range(r,rows):
            if M[i,c]: pr=i;break
        if pr is None: continue
        M[[r,pr]]=M[[pr,r]]; M[r]=M[r]*pow(int(M[r,c]),p-2,p)%p
        for i in np.nonzero(M[:,c])[0]:
            if i!=r: M[i]=(M[i]-M[i,c]*M[r])%p
        piv.append(c); r+=1
    free=[c for c in range(m) if c not in piv]; out=[]
    for f in free:
        z=np.zeros(m,dtype=np.int64); z[f]=1
        for i,c in enumerate(piv): z[c]=(-M[i,f])%p
        out.append(z)
    return out
