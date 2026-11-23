import json,gzip,sys,collections
from fractions import Fraction as Q
from decimal import Decimal as Dm, getcontext
getcontext().prec=40
D='/home/claude/w27/research/p104-live-relative-gain/'
w=json.load(gzip.open(sys.argv[1])); cen=json.load(open(D+'CALLER-CENSUS.json'))
F=w['frames']; rank=[len(f) for f in F]
def span(B):
    s={0}
    for v in B: s|={o^v for o in s}
    return frozenset(s)
S=[span(f) for f in F]
def grade(a,b):
    assert S[a]<S[b] or S[b]<S[a]; return abs(rank[b]-rank[a])
calls=cen['calls']
paid=collections.Counter({int(k):v for k,v in cen['fixed_caller_paid'].items()})
for k,a,b in w['moves']: paid[grade(a,b)]+=calls
bits=0
for k,f in w['forms']:
    for d,c in f:
        q=Q(c); bits=max(bits,q.numerator.bit_length(),q.denominator.bit_length())
print('paid',dict(sorted(paid.items())),'literal peak bits',bits)
r=json.load(open(D+'BANK-FACTORS-RECEIPT.json'))
T={int(k):v for k,v in r['productive'].items()}
def f(c,P,T): return sum(n*(Dm(k).ln()*(1-c)).exp() for k,n in T.items())-sum(n*(Dm(k).ln()*(1-c)).exp() for k,n in P.items())
def root(P,T):
    lo,hi=Dm('0.0035'),Dm('0.0045')
    for _ in range(110):
        m=(lo+hi)/2
        if f(m,P,T)>0: lo=m
        else: hi=m
    return lo
print('raw root',root(paid,T),'old',root({int(k):v for k,v in r['paid'].items()},T))
json.dump({'paid':{str(k):v for k,v in sorted(paid.items())},'productive':r['productive']},open('hist5669.json','w'))
