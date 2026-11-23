# Own mod-p checker for a complex word: locality, nesting, map, histograms.
import json,gzip,pickle,sys
import numpy as np
from fractions import Fraction
from collections import Counter
P=2147483629
D='/home/claude/cs/research/p104-live-relative-gain/'
LAY=json.load(gzip.open(D+'LAYOUT.json.gz')); CAL=json.load(open(D+'CALLER-CENSUS.json'))
def fm(q):
    q=Fraction(q); return q.numerator%P*pow(q.denominator%P,P-2,P)%P
def span(b):
    pts={0}
    for v in b: pts|={o^v for o in pts}
    return frozenset(pts)
def expected(n):
    E=[{i:Fraction(1)} for i in range(n)]; main=set(); h=LAY['hosted']
    for port,x in enumerate(LAY['live']):
        y=x+112; main|={x,y}
        if port in h['Dports']: E[x][y]=Fraction(1)
        else: E[x][y]=Fraction(1,2); E[y]={x:Fraction(-1),y:Fraction(1,2)}
    for x,y in zip(h['X2'],h['Y2']): main|={x,y}; E[y][x]=Fraction(-1)
    return E,main   # E[i] = column i: output j coefficient
def check(w,verbose=True):
    n=len(w['initial']); first=w['first_output']; fr=w['frames']
    S=[span(f) for f in fr]; R=[len(f) for f in fr]
    def grade(a,b):
        assert S[a]<S[b] or S[b]<S[a], ('nest',a,b)
        return abs(R[b]-R[a])
    moves={k:(a,b) for k,a,b in w['moves']}; forms=dict(w['forms'])
    E,main=expected(n)
    paid=Counter({int(k):v for k,v in CAL['fixed_caller_paid'].items()})
    tg=Counter({int(k):v for k,v in CAL['fixed_root_targets'].items()})
    for i,(a,b) in enumerate(zip(w['initial'],w['final'])):
        if i not in main: tg[grade(a,b)]+=48
    bank={~i:a for i,a in enumerate(w['initial'])}
    val={}
    rng=np.random.default_rng(1)
    for k in w['schedule']:
        at=moves[k][0] if k in moves else w['final'][k-first]
        v=np.zeros(n,dtype=np.int64)
        for d,q in forms[k]:
            assert bank[d]==at,('locality',k,d,bank[d],at)
            if d<0: v[~d]=(v[~d]+fm(q))%P
            else: v=(v+val[d]*fm(q))%P
        val[k]=v
        if k in moves: paid[grade(*moves[k])]+=48; bank[k]=moves[k][1]
    # map: output j row = sum_i E[i][j] x_i
    bad=0
    for j in range(n):
        want=np.zeros(n,dtype=np.int64)
        for i in range(n):
            pass
    W=np.zeros((n,n),dtype=np.int64)
    for i,col in enumerate(E):
        for j,q in col.items(): W[j,i]=fm(q)
    for j in range(n):
        if not np.array_equal(val[first+j],W[j]): bad+=1
    return dict(paid=dict(sorted(paid.items())),tg=dict(sorted(tg.items())),bad_outputs=bad,moves=len(moves),n=n)
if __name__=='__main__':
    ws=pickle.load(open('/home/claude/work/words.pkl','rb'))
    r=check(ws['final']); print(r)
    rc=json.load(open(D+'BANK-FACTORS-RECEIPT.json'))
    print('paid match',{str(k):v for k,v in r['paid'].items()}==rc['paid'],'tg match',{str(k):v for k,v in r['tg'].items()}==rc['productive'])
