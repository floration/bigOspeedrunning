from vals import *
w,l=load(); R=[len(f) for f in w['frames']]
n=len(w['initial']); first=w['first_output']
U,Z,forms,cons=compute(w)
loc={}
for i in range(n): loc[~i]=w['initial'][i]
for k,a,b in w['moves']: pass
print('n',n,'moves',len(w['moves']),'sample move',w['moves'][0])
din=[R[a] for a in w['initial']]; dout=[R[b] for b in w['final']]
from collections import Counter
print('init dims',Counter(din)); print('final dims',Counter(dout))
up=Counter(); dn=Counter()
for k,a,b in w['moves']:
    lo,hi=sorted((R[a],R[b]))
    for L in range(lo,hi):
        (up if R[b]>R[a] else dn)[L]+=1
Mo=np.array([U[first+i] for i in range(n)])  # rows outputs, cols inputs
import sympy
def rk(A):
    from la import Basis
    return rank_dep(list(A))[0]
for L in range(9):
    S=[i for i in range(n) if din[i]<=L]; T=[j for j in range(n) if dout[j]>L]
    S2=[i for i in range(n) if din[i]>L]; T2=[j for j in range(n) if dout[j]<=L]
    rup=rk(Mo[np.ix_(T,S)]) if S and T else 0
    rdn=rk(Mo[np.ix_(T2,S2)]) if S2 and T2 else 0
    print(L,'up',up[L],'rankbound',rup,'| down',dn[L],'bound',rdn,flush=True)
