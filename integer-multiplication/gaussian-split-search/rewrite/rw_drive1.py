# brute force: single cross edits (output- or input-compensated) at each (class,chart) with V,Psi; rescan the class.
import sys,pickle,time; sys.path.insert(0,'/home/claude/work')
from rw_lib import *
w=pickle.load(open('/home/claude/work/words.pkl','rb'))['final']
base=scan(w,want_vectors=True)
val=forward(w); b=adjoint(w)
log=[]; hits=[]
delta=Fraction(3,7)
for r in base:
    cls=(r['a'],r['z'])
    for vi,(m,_) in enumerate(r['V']):
        for pi,(l,_) in enumerate(r['Psi']):
            try: mu=ratvec(m); lam=ratvec(l)
            except AssertionError: log.append((cls,r["c"],vi,pi,"ratvec")); continue
            try: s,h=realize(w,mu,lam,val,b)
            except AssertionError: log.append((cls,r['c'],vi,pi,'ratrec')); continue
            for kind,fn in (('O',cross_edit),('I',input_edit)):
                try: w2=fn(w,mu,lam,s,h,delta)
                except AssertionError as e: log.append((cls,r['c'],vi,pi,kind,'cycle')); continue
                new=[x for x in scan(w2,classes={cls}) if x['pair']]
                log.append((cls,r['c'],vi,pi,kind,len(new),[x['c'] for x in new]))
                print(log[-1],flush=True)
                if new: hits.append((cls,r['c'],mu,lam,kind,new)); pickle.dump(hits,open('/home/claude/work/rw_hits1.pkl','wb'))
pickle.dump(log,open('/home/claude/work/rw_log1.pkl','wb'))
print('done',len(log),'hits',len(hits))
