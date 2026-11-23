# first-order screen: pairing change at (c2; s2,h2) from a cross edit (c; s0,h0) in the same class
#   Delta = (alpha - s2.h0)(s0.h2) + beta (s2.h0),  alpha = dS2/drho0, beta = dS0/drho2
import sys,pickle; sys.path.insert(0,'/home/claude/work')
from rw_lib import *
w=pickle.load(open('/home/claude/work/words.pkl','rb'))['final']
forms={k:[(d,fm(q)) for d,q in r] for k,r in w['forms']}
def sens(seed):
    J={}
    for k in w['schedule']:
        x=seed.get(k,0)
        for d,q in forms[k]:
            if d>=0 and J.get(d): x=(x+J[d]*q)%P
        if x: J[k]=x
    return J
base=scan(w,want_vectors=True)
bycls=defaultdict(list)
for r in base: bycls[(r['a'],r['z'])].append(r)
tot=0; nz=[]; from collections import Counter; st=Counter()
for cls,rs in bycls.items():
    G=rs[0]['G']
    items=[]  # (c, mu, s, lam, h, Jrho)
    for r in rs:
        for m,sv in r['V']:
            for l,hv in r['Psi']:
                pass
        r['Vs']=[(m,sv) for m,sv in r['V']]
        r['Ps']=[(l,hv,sens(l)) for l,hv in r['Psi']]
    dot=lambda a,b_:sum(v*b_.get(i,0) for i,v in a.items())%P
    for r0 in rs:
        for m0,s0 in r0['Vs']:
            for l0,h0,J0 in r0['Ps']:
                for r2 in rs:
                    if r2 is r0: continue
                    for m2,s2 in r2['Vs']:
                        alpha=sum(q*J0.get(k,0) for k,q in m2.items() if k>=0)%P
                        for l2,h2,J2 in r2['Ps']:
                            beta=sum(q*J2.get(k,0) for k,q in m0.items() if k>=0)%P
                            D=((alpha-dot(s2,h0))*dot(s0,h2)+beta*dot(s2,h0))%P
                            tot+=1; st[(bool(alpha),bool(beta),bool(dot(s2,h0)),bool(dot(s0,h2)))]+=1
                            if D: nz.append((cls,r0['c'],r2['c'],alpha,beta,dot(s2,h0),dot(s0,h2)))
print('combos',tot,'nonzero first-order',len(nz))
for x in nz[:40]: print(x)
pickle.dump(nz,open('/home/claude/work/rw_screen.pkl','wb'))
print(st)
