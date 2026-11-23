import json,sys
exec(open('/tmp/claude-0/w/s/cres_fast.py').read().split('hits=[]')[0])
hits=json.load(open('/tmp/claude-0/w/d/cres_fast.json'))
from collections import defaultdict
grp=defaultdict(list)
for e,m,g,a2,g2 in hits: grp[(e,a2)].append(g2)
real=[]
for (e,a2),_ in grp.items():
    b=moves[e][1]; T=firstuse.get(e)
    if T is None: continue
    Va=[x for x in AV[a2] if pos[x]<T]
    rows,piv=echelon([val[x] for x in Va])
    Wall=[x for x in AV[b] if pos[x]<T]
    if e not in Wall: continue
    Wm=reduce_many(rows,piv,np.array([val[x] for x in Wall]))
    i=Wall.index(e)
    if any(int(z[i]) for z in leftnull(Wm)):
        real.append((e,moves[e],abs(R[b]-R[moves[e][0]]),a2,abs(R[b]-R[a2])))
print('pairs',len(grp),'time-correct',len(real))
for r in real[:50]: print(r)
json.dump(real,open('/tmp/claude-0/w/d/cres_time.json','w'))
