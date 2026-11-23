# For each move Y (b->c): could Y be computed at another chart a (nested with c) from values there,
# letting a cascade of upstream moves (now unused) be deleted?  Score with concave prices.
from vals import *
import time,sys
w,l=load(sys.argv[1] if len(sys.argv)>1 else 'final_word.json.gz'); F=w['frames']; R=[len(f) for f in F]; S=[span(f) for f in F]
n=len(w['initial']); first=w['first_output']
U,Z,forms,cons=compute(w)
mv={k:(a,b) for k,a,b in w['moves']}
c0=0.0038984814
pr=lambda g: g**(1-c0)
nested=lambda a,b: a!=b and (S[a]<S[b] or S[b]<S[a])
# values at charts
at=defaultdict(list)
for i in range(n): at[w['initial'][i]].append(~i)
for k,(a,b) in mv.items(): at[b].append(k)
supp={k:int(''.join('1' if x else '0' for x in (U[k]!=0)[::-1]),2) for k in U}
chsupp={a:0 for a in at}
for a,ks in at.items():
    s=0
    for k in ks: s|=supp[k]
    chsupp[a]=s
# descendants bitsets over node index
nodes=list(U.keys()); idx={k:i for i,k in enumerate(nodes)}
desc={}
for k in reversed(w['schedule']):
    d=1<<idx[k]
    for j,_ in cons[k]: d|=desc[j]
    desc[k]=d
def cascade(Y):
    dele=set(); stack=[Y]; usecnt={}
    while stack:
        y=stack.pop()
        for d,_ in forms[y]:
            if d<0 or d in dele: continue
            usecnt[d]=usecnt.get(d,len(cons[d]))-1
            if usecnt[d]==0: dele.add(d); stack.append(d)
    return dele
def inspan(vecs,v):
    basis=[]
    for x in vecs:
        x=x.copy()
        for piv,b in basis:
            if x[piv]: x=(x-b*x[piv])%p
        nz=np.flatnonzero(x)
        if len(nz): basis.append((nz[0],x*pow(int(x[nz[0]]),p-2,p)%p))
    v=v.copy()
    for piv,b in basis:
        if v[piv]: v=(v-b*v[piv])%p
    return not v.any()
hits=[]; tested=0; t0=time.time()
for Y,(b,c) in mv.items():
    dele=cascade(Y)
    gd=sum(pr(abs(R[mv[d][1]]-R[mv[d][0]])) for d in dele)
    base=gd+pr(abs(R[c]-R[b]))
    for a in at:
        if a==b or not nested(a,c): continue
        gain=base-pr(abs(R[c]-R[a]))
        if gain<=1e-9: continue
        if supp[Y] & ~chsupp[a]: continue
        tested+=1
        cand=[k for k in at[a] if k<0 or not (desc[Y]>>idx[k])&1]
        if inspan([U[k] for k in cand],U[Y]):
            hits.append((gain,Y,b,c,a,len(dele),abs(R[c]-R[b]),abs(R[c]-R[a]),sorted(dele)))
print('tested',tested,'hits',len(hits),time.time()-t0)
hits.sort(reverse=True)
for h in hits[:40]: print(h[:8], h[8][:8])
json.dump(hits,open('reroute_hits.json','w'))
