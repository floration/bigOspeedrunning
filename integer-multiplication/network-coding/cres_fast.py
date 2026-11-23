import json,gzip,sys
from fractions import Fraction
from collections import defaultdict,Counter
import numpy as np
p=32749
w=json.load(gzip.open(sys.argv[1]))
starts,ends,first=w['initial'],w['final'],w['first_output']; n=len(starts)
moves={k:(a,b) for k,a,b in w['moves']}; forms=dict((k,f) for k,f in w['forms'])
def modq(t):
    q=Fraction(t); assert q.denominator%p; return q.numerator%p*pow(q.denominator%p,p-2,p)%p
val={}; chart={}; pos={}
for i in range(n):
    v=np.zeros(n,dtype=np.int64); v[i]=1; val[~i]=v; chart[~i]=starts[i]; pos[~i]=-1
firstuse={}
for t,k in enumerate(w['schedule']):
    s=moves[k][0] if k in moves else ends[k-first]
    v=np.zeros(n,dtype=np.int64)
    for d,c in forms[k]:
        v=(v+val[d]*modq(c))%p; firstuse.setdefault(d,t)
    val[k]=v; pos[k]=t; chart[k]=moves[k][1] if k in moves else s
frames=w['frames']
def span(basis):
    pts={0}
    for v in basis: pts|={o^v for o in pts}
    return frozenset(pts)
S=[span(f) for f in frames]; R=[len(f) for f in frames]; nf=len(frames)
AV=defaultdict(list)
for x,c in chart.items():
    if x<0 or x in moves: AV[c].append(x)
def echelon(vecs):
    rows=[];piv=[]
    for v in vecs:
        v=v.copy()
        if rows: 
            Rm=np.array(rows); v=(v-(v[piv][None,:]@Rm)[0])%p if False else reduce(rows,piv,v)
        nz=np.nonzero(v)[0]
        if len(nz)==0: continue
        c=nz[0]; v=v*pow(int(v[c]),p-2,p)%p
        # keep fully reduced
        for i in range(len(rows)):
            if rows[i][c]: rows[i]=(rows[i]-rows[i][c]*v)%p
        rows.append(v); piv.append(c)
    return rows,piv
def reduce(rows,piv,v):
    if not rows: return v%p
    Rm=np.array(rows); co=v[piv]
    return (v-(co@Rm))%p
def reduce_many(rows,piv,M):
    if not rows: return M%p
    Rm=np.array(rows); return (M-(M[:,piv]@Rm)%p)%p
EV={}
order=sorted(AV,key=lambda c:len(AV[c]))
for c in AV: EV[c]=echelon([val[x] for x in AV[c]])
print('echelons done',flush=True)
def leftnull(Wm):
    # vectors z with z@Wm=0
    M=(Wm.T.copy())%p; rows,m=M.shape; piv=[]; r=0
    for c in range(m):
        nz=np.nonzero(M[r:,c])[0]
        if len(nz)==0: continue
        pr=r+nz[0]; M[[r,pr]]=M[[pr,r]]; M[r]=M[r]*pow(int(M[r,c]),p-2,p)%p
        col=M[:,c].copy(); col[r]=0
        M=(M-np.outer(col,M[r]))%p
        piv.append(c); r+=1
        if r==rows: break
    out=[]
    for f in range(m):
        if f in piv: continue
        z=np.zeros(m,dtype=np.int64); z[f]=1
        for i,c in enumerate(piv): z[c]=(-M[i,f])%p
        out.append(z)
    return out
hits=[]
for b in range(nf):
    Db=[x for x in AV[b] if x>=0]
    if not Db: continue
    gmax=max(abs(R[b]-R[moves[k][0]]) for k in Db)
    Wall=[x for x in AV[b]]
    for a2 in list(EV):
        if a2==b or not (S[a2]<S[b] or S[b]<S[a2]): continue
        g2=abs(R[b]-R[a2])
        if g2>=gmax: continue
        rows,piv=EV[a2]
        cands=[e for e in Db if abs(R[b]-R[moves[e][0]])>g2 and moves[e][0]!=a2]
        if not cands: continue
        Wm=reduce_many(rows,piv,np.array([val[x] for x in Wall]))
        ks=leftnull(Wm)
        for e in cands:
            i=Wall.index(e)
            if any(int(z[i]) for z in ks): hits.append((e,moves[e],abs(R[b]-R[moves[e][0]]),a2,g2))
    if b%100==0: print('chart',b,len(hits),flush=True)
print('hits (time ignored)',len(hits)); print(Counter((h[2],h[4]) for h in hits))
for h in hits[:40]: print(h)
json.dump(hits,open('/tmp/claude-0/w/d/cres_fast.json','w'))
