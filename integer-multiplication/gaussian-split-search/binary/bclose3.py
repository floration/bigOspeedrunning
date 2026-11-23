# For the both-absorbable same-link pairs (merge block singular), search a third absorbable closure term
# z3 u3^T at any chart c (u3 in resident span at c with u3_X=0; b3 in leaving-adjoint span at c with (Minv b3)_X=0)
# making det(I + [u2 u1 u3]^T [z1 z2 z3]) = 1 over GF(2). det is bilinear in (u3,z3), so basis pairs suffice.
import sys,pickle
sys.path.insert(0,'/home/claude/work/binary')
from bscan import *
p=sys.argv[1]
d=load(p); res,w,moves,val,pairs,main=check(d,verbose=False); madj,inadj=adjoint(w); pub=w.pub
X=[i for i in range(pub) if d['start'][i]!=0]; mX=sum(1<<i for i in X); nX=((1<<pub)-1)&~mX
def Minv(bm):
    r=bm
    for x,y in pairs:
        if bm>>x&1: r^=1<<y
    return r
pr=lambda x,y:bin(x&y).count('1')&1
def det3(U,Z):
    M=[[(i==j)^pr(U[i],Z[j]) for j in range(3)] for i in range(3)]
    return (M[0][0]*(M[1][1]*M[2][2]^M[1][2]*M[2][1]) ^ M[0][1]*(M[1][0]*M[2][2]^M[1][2]*M[2][0]) ^ M[0][2]*(M[1][0]*M[2][1]^M[1][1]*M[2][0]))&1
o=pickle.load(open(p.split('/')[-1]+'.bidir2.pkl','rb'))['one']
bt={t:(t,f,a,b,v) for t,f,a,b,v in moves}
inp=defaultdict(list); arr=defaultdict(list); dep=defaultdict(list)
for i in range(pub): inp[d['start'][i]].append(1<<i)
for t,f,a,b,v in moves: arr[b].append(v); dep[a].append(Minv(madj[t]))
for j in range(pub): dep[d['final'][j]].append(Minv(1<<j))
Wc={c:sub_in(inp[c]+arr[c],nX) for c in w.S}
Uc={c:sub_in(dep[c],nX) for c in w.S}   # recovered-coordinate effects with zero X part
print('charts with both absorbable spaces',sum(1 for c in w.S if Wc[c] and Uc[c]))
hits=[]
for l,t1,t2,isboth in o:
    if not isboth: continue
    u1,u2=bt[t1][4],bt[t2][4]; z1,z2=Minv(madj[t1]),Minv(madj[t2])
    cs=[c for c in w.S if any(det3([u2,u1,u3],[z1,z2,z3]) for u3 in Wc[c] for z3 in Uc[c])]
    if cs: hits.append((l,t1,t2,cs))
print('pairs',sum(1 for x in o if x[3]),'with a third-term closure',len(hits))
for h in hits[:20]: print(h[:3],h[3][:12],len(h[3]))
pickle.dump(hits,open(p.split('/')[-1]+'.close3.pkl','wb'))
