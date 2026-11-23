# Exact root change of replacing one target grade g by (a, g-a) in each of the 36 calls (K7 base).
import sys; sys.path.insert(0,'/home/claude/work/binary')
from bchk import *
d=load('data/strong-bit-k7.json.gz'); res,w,moves,val,pairs,main=check(d,verbose=False)
paid,tg=histograms(w,moves,main); P,T=allcalls(paid,tg); r0,_=root(P,T)
print('base',r0)
for g,a in [(8,4),(8,3),(8,2),(8,1),(4,2),(4,1)]:
    t=Counter(tg); t[g]-=1; t[a]+=1; t[g-a]+=1
    P2,T2=allcalls(paid,t); r,_=root(P2,T2); print(f'split {g}->{a}+{g-a}: root {r:.13f} gain {r-r0:+.4e}')
# reference: one extra rank-1 paid move per call
p=Counter(paid); p[1]+=1; P2,T2=allcalls(p,tg); print('extra rank-1 move per call', root(P2,T2)[0]-r0)
