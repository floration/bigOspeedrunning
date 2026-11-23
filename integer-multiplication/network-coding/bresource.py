import json,gzip,sys
import numpy as np
from collections import defaultdict,Counter
d=json.load(gzip.open(sys.argv[1]))
pub=d['public']; prog=d['program']; F=d['frames']; nf=len(F)
dim=[F[str(i)]['dim'] for i in range(nf)]
P=[]
for i in range(nf):
    B=F[str(i)]['B']; A=F[str(i)]['A']
    M=np.array(B+A,dtype=float).T
    Dg=np.diag([1.0]*len(B)+[0.0]*len(A))
    P.append(M@Dg@np.linalg.inv(M))
P=np.array(P)
nested=defaultdict(set)  # nested[t] = frames nested with t (either way)
for i in range(nf):
    for j in range(nf):
        if dim[i]<dim[j]:
            pi,pj=P[i],P[j]
            if np.allclose(pi@pj,pi,atol=1e-9) and np.allclose(pj@pi,pi,atol=1e-9):
                nested[i].add(j); nested[j].add(i)
print('nested pairs',sum(len(v) for v in nested.values())//2)
fr=dict(enumerate(d['start'])); val={i:1<<i for i in range(pub)}
L=defaultdict(list)
for i in range(pub): L[d['start'][i]].append(1<<i)
Dl=defaultdict(list); moves=[]
for t,ins in enumerate(prog):
    op=ins[0]
    if op=='INIT': fr[ins[1]]=ins[2]; val[ins[1]]=0
    elif op=='ADD': val[ins[1]]^=val[ins[2]]
    elif op=='MOVE':
        f,a,b=ins[1],ins[2],ins[3]; moves.append((t,f,a,b,val[f])); Dl[b].append((t,val[f])); fr[f]=b
    elif op=='SWAP':
        a,b=ins[1],ins[2]; fr[a],fr[b]=fr[b],fr[a]; val[a],val[b]=val[b],val[a]
    elif op=='CLEAR': fr.pop(ins[1]); val.pop(ins[1])
def basis(vs):
    bs=[]
    for v in vs:
        for b in bs: v=min(v,v^b)
        if v: bs.append(v)
    return bs
def inspan(bs,v):
    for b in bs: v=min(v,v^b)
    return v==0
V={c: L[c]+[x[1] for x in Dl[c]] for c in range(nf)}
hits=[]
for (t0,f,a,b,v) in moves:
    g=abs(dim[b]-dim[a])
    W=L[b]+[x[1] for x in Dl[b] if x[0]!=t0]
    for a2 in nested[b]:
        if a2==a: continue
        g2=abs(dim[b]-dim[a2])
        if g2>=g: continue
        if inspan(basis(V[a2]+W),v): hits.append((t0,f,a,b,g,a2,g2))
print('re-source hits (time ignored)',len(hits)); print(Counter((h[4],h[6]) for h in hits))
for h in hits[:20]: print(h)
json.dump(hits,open('/tmp/claude-0/w/d/bres_hits.json','w'))
