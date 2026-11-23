import json,gzip,sys,pickle
import numpy as np
from collections import defaultdict,Counter
d=json.load(gzip.open(sys.argv[1]))
pub=d['public']; prog=d['program']; F=d['frames']; nf=len(F)
dim=[F[str(i)]['dim'] for i in range(nf)]
P=[]
for i in range(nf):
    B=F[str(i)]['B']; A=F[str(i)]['A']
    M=np.array(B+A,dtype=float).T
    P.append(M@np.diag([1.0]*len(B)+[0.0]*len(A))@np.linalg.inv(M))
nested=defaultdict(set)
for i in range(nf):
    for j in range(nf):
        if dim[i]<dim[j] and np.allclose(P[i]@P[j],P[i],atol=1e-9) and np.allclose(P[j]@P[i],P[i],atol=1e-9):
            nested[i].add(j); nested[j].add(i)
pickle.dump(dict(nested),open('/tmp/claude-0/w/d/k7nested.pkl','wb'))
def basis(vs):
    bs=[]
    for v in vs:
        for b in bs: v=min(v,v^b)
        if v: bs.append(v)
    return bs
def inspan(bs,v):
    for b in bs: v=min(v,v^b)
    return v==0
fr=dict(enumerate(d['start'])); val={i:1<<i for i in range(pub)}
at=defaultdict(set)
for i in range(pub): at[d['start'][i]].add(i)
hits=[]
for t,ins in enumerate(prog):
    op=ins[0]
    if op=='INIT': fr[ins[1]]=ins[2]; val[ins[1]]=0; at[ins[2]].add(ins[1])
    elif op=='ADD': val[ins[1]]^=val[ins[2]]
    elif op=='MOVE':
        f,a,b=ins[1],ins[2],ins[3]; v=val[f]; g=abs(dim[b]-dim[a])
        Wb=[val[r] for r in at[b]]
        for a2 in nested[b]:
            if a2==a: continue
            g2=abs(dim[b]-dim[a2])
            if g2>=g: continue
            V=[val[r] for r in at[a2] if r!=f]
            if inspan(basis(V+Wb),v): hits.append((t,f,a,b,g,a2,g2))
        at[a].discard(f); at[b].add(f); fr[f]=b
    elif op=='SWAP':
        x,y=ins[1],ins[2]; fx,fy=fr[x],fr[y]
        at[fx].discard(x); at[fy].discard(y); at[fx].add(y); at[fy].add(x)
        fr[x],fr[y]=fy,fx; val[x],val[y]=val[y],val[x]
    elif op=='CLEAR': at[fr[ins[1]]].discard(ins[1]); fr.pop(ins[1]); val.pop(ins[1])
print('time-correct re-source hits',len(hits)); print(Counter((h[4],h[6]) for h in hits))
for h in hits[:40]: print(h)
json.dump(hits,open('/tmp/claude-0/w/d/bres2_hits.json','w'))
