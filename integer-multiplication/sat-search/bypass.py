# Two-hop bypass test: remove one transfer from edge a->b and one from b->c, add one a->c.
from model import *
from la import *
import time,sys
w,l=load(); F=w['frames']; R=[len(f) for f in F]; S=[span(f) for f in F]
n=len(w['initial']); first=w['first_output']
forms={k:[(d,modq(c)) for d,c in r] for k,r in w['forms']}
U={}
for i in range(n):
    v=np.zeros(n,dtype=np.int64); v[i]=1; U[~i]=v
for k in w['schedule']:
    v=np.zeros(n,dtype=np.int64)
    for d,c in forms[k]: v=(v+U[d]*c)%P
    U[k]=v
mv={k:(a,b) for k,a,b in w['moves']}
cons=defaultdict(list)
for k,r in forms.items():
    for d,c in r: cons[d].append(k)
at=defaultdict(list)        # values available at chart
for i in range(n): at[w['initial'][i]].append(~i)
for k,(a,b) in mv.items(): at[b].append(k)
outof=defaultdict(list)     # computed at chart (moves leaving + outputs)
for k,(a,b) in mv.items(): outof[a].append(k)
for i in range(n): outof[w['final'][i]].append(first+i)
edge=defaultdict(list)
for k,(a,b) in mv.items(): edge[(a,b)].append(k)
nodes=list(U.keys()); idx={k:i for i,k in enumerate(nodes)}
desc={}
for k in reversed(w['schedule']):
    d=1<<idx[k]
    for j in cons[k]: d|=desc[j]
    desc[k]=d
for i in range(n):
    d=1<<idx[~i]
    for j in cons[~i]: d|=desc[j]
    desc[~i]=d
c0=0.0038984814; pr=lambda g: g**(1-c0)
nested=lambda a,b: a!=b and (S[a]<S[b] or S[b]<S[a])
spanA={}
def span_at(a):
    if a not in spanA:
        B=Basis(n)
        for k in at[a]: B.add(U[k])
        spanA[a]=B
    return spanA[a]
inn=defaultdict(list)
for (a,b) in edge: inn[b].append(a)
CNT=Counter(); hits=[]; t0=time.time(); tested=0
for (b,c),bc in edge.items():
    for a in inn[b]:
        if not nested(a,c): continue
        gain=pr(abs(R[b]-R[a]))+pr(abs(R[c]-R[b]))-pr(abs(R[c]-R[a]))
        if gain<=1e-9: continue
        tested+=1
        SA=span_at(a)
        res=[SA.reduce(U[k]) for k in bc]
        ker=kernel_combos(res) if any(r.any() for r in res) else [np.eye(len(bc),dtype=np.int64)[i] for i in range(len(bc))]
        if not ker: continue
        CNT["I"]+=1
        I=[sum((U[k]*int(x[t]))%P for t,k in enumerate(bc))%P for x in ker]
        ab=set(edge[(a,b)])
        Q=Basis(n)
        for k in at[b]:
            if k not in ab: Q.add(U[k])
        for k in outof[b]:
            if k not in bc: Q.add(U[k])
        free=[u for u in I if not Q.contains(u)]
        if free:
            hits.append((gain,a,b,c,len(edge[(a,b)]),len(bc),len(I),len(free)))
            print('HIT',hits[-1],flush=True)
print(CNT); print('tested',tested,'hits',len(hits),time.time()-t0)
json.dump(hits,open('bypass_hits.json','w'))
