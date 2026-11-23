# per chart: rank of outgoing adjoints vs count, rank of incoming forms vs count; per link: dependence among transfers
import sys,pickle; sys.path.insert(0,'/home/claude/work')
from rw_lib import *
def rank(rows):
    if not rows: return 0
    A=np.array(rows); return A.shape[1]-len(nullspace(A))
w=pickle.load(open(sys.argv[1] if len(sys.argv)>1 else '/home/claude/work/words.pkl','rb'))
if 'final' in w and isinstance(w['final'],dict): w=w['final']
n=len(w['initial']); first=w['first_output']
val=forward(w); b=adjoint(w)
moves={k:(a,bb) for k,a,bb in w['moves']}
out=defaultdict(list); inn=defaultdict(list); link=defaultdict(list)
for k,(a,bb) in moves.items(): out[a].append(b[k]); inn[bb].append(val[k]); link[(a,bb)].append(k)
for j in range(n): out[w['final'][j]].append(b[first+j])
EYE=np.eye(n,dtype=np.int64)
for i in range(n): inn[w["initial"][i]].append(EYE[i])
dO=dI=0
for c in range(len(w['frames'])):
    ro=rank(out[c]); ri=rank(inn[c])
    if ro<len(out[c]) or ri<len(inn[c]): print('chart',c,'out',len(out[c]),ro,'in',len(inn[c]),ri)
    dO+=len(out[c])-ro; dI+=len(inn[c])-ri
print('deficiency out',dO,'in',dI)
multi={l:ks for l,ks in link.items() if len(ks)>1}
print('links with >1 transfer',len(multi),'transfers on them',sum(len(v) for v in multi.values()))
dl=0
for l,ks in multi.items():
    fu=rank([val[k] for k in ks]); fz=rank([b[k] for k in ks])
    if fu<len(ks) or fz<len(ks): dl+=1; print('link',l,len(ks),fu,fz)
print('dependent links',dl)
