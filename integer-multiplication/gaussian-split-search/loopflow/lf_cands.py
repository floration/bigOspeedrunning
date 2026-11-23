# Loop-flow merge candidates: links with v1 (u_X!=0, z_X=0) and v2 (u_X=0, z_X!=0).
# Single-third-chart test: chart c (not a,b) where u1 (full form of v1) is in span(resident forms at c)
# and b_v2 (full adjoint of v2) is in span(adjoints of rows computed at c).
import sys,pickle,time; sys.path.insert(0,'/home/claude/work')
from rw_lib import *
w=pickle.load(open('/home/claude/work/words.pkl','rb'))['final']
n=len(w['initial']); first=w['first_output']
d=pickle.load(open('/home/claude/work/rw_xcoords.pkl','rb')); U,Z,ks=d['U'],d['Z'],d['ks']
uz=(U!=0).any(1); zz=(Z!=0).any(1); del U,Z
moves={k:(a,bb) for k,a,bb in w['moves']}; R=[len(f) for f in w['frames']]
link=defaultdict(list)
for i,k in enumerate(ks): link[moves[k]].append(i)
pairs=[]
for l,I in link.items():
    A=[ks[i] for i in I if not uz[i] and zz[i]]; B=[ks[i] for i in I if uz[i] and not zz[i]]
    for v2 in A:
        for v1 in B: pairs.append((l,abs(R[l[1]]-R[l[0]]),v1,v2))
print('pattern links',len({p[0] for p in pairs}),'pairs',len(pairs))
val=forward(w); b=adjoint(w)
def rref(A):
    A=A.copy()%P; m,nn=A.shape; piv=[]; r=0
    for c in range(nn):
        if r==m: break
        nz=np.nonzero(A[r:,c])[0]
        if len(nz)==0: continue
        p=r+nz[0]; A[[r,p]]=A[[p,r]]
        A[r]=A[r]*pow(int(A[r,c]),P-2,P)%P
        col=A[:,c].copy(); col[r]=0; nzr=np.nonzero(col)[0]
        if len(nzr): A[nzr]=(A[nzr]-mm(col[nzr][:,None],A[r][None,:]))%P
        piv.append(c); r+=1
    return A[:r],piv
def inspan(Rr,piv,Vs):
    if len(piv)==0: return ~(Vs!=0).any(1)
    co=Vs[:,piv]; res=(Vs-mm(co,Rr))%P
    return ~(res!=0).any(1)
EYE=np.eye(n,dtype=np.int64)
inn=defaultdict(list); out=defaultdict(list)
for k,(a,bb) in moves.items(): inn[bb].append(val[k]); out[a].append(b[k])
for i in range(n): inn[w['initial'][i]].append(EYE[i])
for j in range(n): out[w['final'][j]].append(b[first+j])
U1=np.array([val[p[2]] for p in pairs]); B2=np.array([b[p[3]] for p in pairs])
hitU=defaultdict(set); hitB=defaultdict(set)
t=time.time()
for c in range(len(w['frames'])):
    if not inn[c] or not out[c]: continue
    Rr,piv=rref(np.array(inn[c])); okU=inspan(Rr,piv,U1)
    if not okU.any(): continue
    Rb,pb=rref(np.array(out[c])); okB=inspan(Rb,pb,B2)
    for i in np.nonzero(okU&okB)[0]:
        l=pairs[i][0]
        if c not in l: hitU[i].add(c)
    for i in np.nonzero(okU)[0]: hitB[i].add(c)
print('time',time.time()-t)
print('pairs with u1 in span at some chart (incl a,b):',len(hitB))
print('pairs with a third chart having both:',len(hitU))
for i,cs in hitU.items(): print(pairs[i],sorted(cs))
pickle.dump(dict(pairs=pairs,hit=dict(hitU),uspan={i:sorted(s) for i,s in hitB.items()}),open('/home/claude/work/lf/cands.pkl','wb'))
