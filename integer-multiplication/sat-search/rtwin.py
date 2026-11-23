from win import *
import sys
hops=int(sys.argv[1]); tl=int(sys.argv[2])
down=[(k,u,v) for k,u,v in edges if R[label[u]]>R[label[v]]]
print('down edges',len(down))
W=set()
for k,u,v in down:
    for x in (u,v):
        if not fixed[x]: W.add(x)
fr=set(W)
for _ in range(hops):
    nf=set()
    for x in fr:
        for k,y in adj[x]:
            if not fixed[y] and y not in W: nf.add(y)
    W|=nf; fr=nf
print('window',len(W),flush=True)
r=solve(sorted(W),cur,tl)
print('result gain',r[0] if r else None,'optimal',r[2] if r else None)
if r and r[0]>0:
    print({v:(cur[v],L) for v,L in r[1].items() if cur[v]!=L})
    pickle.dump(r,open(f'rt_{hops}.pkl','wb'))
