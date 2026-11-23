import sys,pickle; sys.path.insert(0,'/home/claude/work')
from rw_lib import *
w=pickle.load(open('/home/claude/work/words.pkl','rb'))['final']
res=scan(w,classes={(3,1091)},want_vectors=True)
r=[r for r in res if r['c']==599][0]
mu=ratvec(r['V'][1][0]); lam=ratvec(r['Psi'][0][0])
s,h=realize(w,mu,lam); print(mu,lam,s,h)
for delta in [Fraction(1),Fraction(1,3)]:
    w2=cross_edit(w,mu,lam,s,h,delta)
    rc=check(w2); print('delta',delta,'bad',rc['bad_outputs'],kappa(rc))
    for x in scan(w2):
        if x['pair']: print('  PAIR',x)
    pickle.dump(w2,open('/home/claude/work/rw_cross599.pkl','wb'))
