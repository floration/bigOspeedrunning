from vals import *
import time
w,l=load(); t=time.time()
U,Z,forms,cons=compute(w); print('vals',time.time()-t)
mv={k:(a,b) for k,a,b in w['moves']}
R=[len(f) for f in w['frames']]
src=defaultdict(list); dst=defaultdict(list)
for k,(a,b) in mv.items(): src[a].append(k); dst[b].append(k)
tot=0
for a,ks in src.items():
    r,deps=rank_dep([Z[k] for k in ks])
    if deps: tot+=len(deps); print('BACK chart',a,'moves',len(ks),'rank',r,[{ks[j]:x for j,x in d.items()} for d in deps][:3])
# forward per destination including inputs starting there
n=len(w['initial'])
for b,ks in dst.items():
    ins=[~i for i in range(n) if w['initial'][i]==b]
    r,deps=rank_dep([U[k] for k in ins+ks])
    if deps: tot+=len(deps); print('FWD chart',b,'n',len(ins+ks),'rank',r)
print('total deps',tot)
