"""Independent check that a gamed 179-variable quartic has the same rational zero-set projection as Brox's.
Checks: (1) new residuals span exactly the same Q-vector space as the original residuals (so same common zero set);
(2) weights > 0; (3) P_final(x) = kappa * sum w_i f_i(s*x)^2 with s_j nonzero, s_1 = 1; (4) integer, content 1, degree 4."""
import json,sys,math
from fractions import Fraction as F
from collections import defaultdict
orig=json.load(open(sys.argv[1]+'/quadrics.json'))['residuals']; G=json.load(open(sys.argv[2]))
O=[]
for r in orig:
    f=defaultdict(int)
    for t in r['terms']: f[tuple(sorted(t['monomial']))]+=int(t['coefficient'])
    O.append({k:F(v) for k,v in f.items() if v})
N=[{tuple(k):F(v) for k,v in f} for f in G['residuals']]
def rank(rows):
    piv={}
    for f in rows:
        r=dict(f)
        while r:
            k=min(r)
            if k in piv:
                c=r[k]
                for kk,vv in piv[k].items():
                    r[kk]=r.get(kk,0)-c*vv
                    if r[kk]==0: del r[kk]
            else:
                inv=1/r[k]; piv[k]={a:b*inv for a,b in r.items()}; break
    return len(piv)
ro,rn,rb=rank(O),rank(N),rank(O+N)
print('rank orig',ro,'rank new',rn,'rank union',rb,'-> same span:',ro==rn==rb==len(O)==len(N))
W=[F(w) for w in G['weights']]; print('weights positive:',all(w>0 for w in W))
s={int(j):F(v) for j,v in G.get('variable_scalings',{}).items()}
print('x1 unscaled:', 1 not in s, 'scalings nonzero:', all(v!=0 for v in s.values()))
S=defaultdict(F)
for w,f in zip(W,N):
    it=[(k,v*math.prod(s.get(x,F(1)) for x in k)) for k,v in f.items()]
    for a,ca in it:
        for b,cb in it: S[tuple(sorted(a+b))]+=w*ca*cb
S={k:v for k,v in S.items() if v}
Pf={tuple(k):int(v) for k,v in G['polynomial']}
kappa=F(next(iter(Pf.values())))/S[next(iter(Pf))]
print('P_final == kappa*sum w f^2:', kappa>0 and all(F(Pf.get(k,0))==kappa*S.get(k,0) for k in set(S)|set(Pf)))
g=0
for v in Pf.values(): g=math.gcd(g,v)
print('terms',len(Pf),'degree',max(map(len,Pf)),'vars',len({x for k in Pf for x in k}),'content',g,'height bits',max(abs(v) for v in Pf.values()).bit_length())
