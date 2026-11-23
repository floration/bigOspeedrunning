# #8027 coordinates: u_X = form on X (inputs not at chart 3), z_X = X-rows of M^-1 applied to the adjoint.
# census: links with >=2 transfers, ranks of U_X and Z_X, and (u_X=0)/(z_X=0) transfers.
import sys,pickle; sys.path.insert(0,'/home/claude/work')
from rw_lib import *
w=pickle.load(open('/home/claude/work/words.pkl','rb'))['final']
n=len(w['initial']); E,main=expected(n)
W=np.zeros((n,n),dtype=np.int64)
for i,col in enumerate(E):
    for j,q in col.items(): W[j,i]=fm(q)
# inverse via elimination on [W | I]
A=np.concatenate([W,np.eye(n,dtype=np.int64)],axis=1)
for c in range(n):
    p=c+np.nonzero(A[c:,c])[0][0]; A[[c,p]]=A[[p,c]]
    A[c]=A[c]*pow(int(A[c,c]),P-2,P)%P
    col=A[:,c].copy(); col[c]=0; nz=np.nonzero(col)[0]
    if len(nz): A[nz]=(A[nz]-mm(col[nz][:,None],A[c][None,:]))%P
Minv=A[:,n:]
assert (mm(Minv,W)==np.eye(n,dtype=np.int64)).all()
X=[i for i in range(n) if w['initial'][i]!=3]; print('X',len(X),'chart3 inputs',n-len(X))
val=forward(w); b=adjoint(w)
moves={k:(a,bb) for k,a,bb in w['moves']}
ks=sorted(moves)
U=np.array([val[k] for k in ks])[:,X]
Z=mm(np.array([b[k] for k in ks]),Minv.T)[:,X]     # recovered x = Minv @ out ; effect = Minv @ b_v
idx={k:i for i,k in enumerate(ks)}
uz=(U!=0).any(1); zz=(Z!=0).any(1)
print('transfers',len(ks),'u_X=0:',int((~uz).sum()),'z_X=0:',int((~zz).sum()),'both 0:',int((~uz&~zz).sum()))
fr=w['frames']; R=[len(f) for f in fr]
from collections import Counter
g=lambda k: abs(R[moves[k][1]]-R[moves[k][0]])
print('grade of u_X=0 transfers',sorted(Counter(g(k) for k in ks if not uz[idx[k]]).items()))
print('grade of z_X=0 transfers',sorted(Counter(g(k) for k in ks if not zz[idx[k]]).items()))
link=defaultdict(list)
for k in ks: link[moves[k]].append(k)
def rank(M_):
    if len(M_)==0: return 0
    return M_.shape[1]-len(nullspace(M_)) if M_.shape[0]<=M_.shape[1] else rank(M_.T)
cand=[]
for l,kk in link.items():
    if len(kk)<2: continue
    I=[idx[k] for k in kk]
    ru=rank(U[I]); rz=rank(Z[I])
    nu=sum(not uz[i] for i in I); nzz=sum(not zz[i] for i in I)
    if nu and nzz: cand.append((l,len(kk),g(kk[0]),ru,rz,nu,nzz))
print('links with both a u_X=0 and a z_X=0 transfer:',len(cand))
for c_ in sorted(cand,key=lambda t:-t[2])[:40]: print(c_)
pickle.dump(dict(X=X,ks=ks,U=U,Z=Z,cand=cand),open('/home/claude/work/rw_xcoords.pkl','wb'))
