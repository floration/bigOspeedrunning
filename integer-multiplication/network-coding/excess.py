import sys; sys.path.insert(0,'/tmp/claude-0/w/s')
from load import *
w,moves,forms,val,chart,src=load(sys.argv[1])
n=len(w['initial'])
L=defaultdict(list); D=defaultdict(list); O=defaultdict(list)
for i,s in enumerate(w['initial']): L[s].append(~i)
for k,(a,b) in moves.items(): D[b].append(k); O[a].append(k)
for k in forms:
    if k not in moves: O[src[k]].append(k)
tot=0; rows=[]
F=w['frames']
for c in sorted(set(L)|set(D)|set(O)):
    l=[val[x] for x in L[c]]; d=[val[x] for x in D[c]]; o=[val[x] for x in O[c]]
    rl=rank(l); rld=rank(l+d); rlo=rank(l+o); rall=rank(l+d+o)
    assert rall==rld,(c,)
    ex=rld-rlo; dep=len(d)-(rld-rl)
    if ex or dep: rows.append((c,len(F[c]),len(l),len(d),len(o),ex,dep)); tot+=ex
print('charts with excess',len(rows),'total excess',tot)
for r in rows[:40]: print(r)
