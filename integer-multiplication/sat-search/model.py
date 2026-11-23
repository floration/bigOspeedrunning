import json,gzip
from collections import Counter,defaultdict
from mpmath import mp,mpf,log
mp.dps=40
CALL=json.load(open('/home/claude/w/repo/research/p104-live-relative-gain/CALLER-CENSUS.json'))
def load(path='final_word.json.gz',lay='final_layout.json.gz'):
    return json.load(gzip.open(path)),json.load(gzip.open(lay))
def span(basis):
    pts={0}
    for v in basis: pts|={o^v for o in pts}
    return frozenset(pts)
def main_roles(layout):
    main=set(); h=layout['hosted']
    for port,x in enumerate(layout['live']): main.update((x,x+112))
    for x,y in zip(h['X2'],h['Y2']): main.update((x,y))
    return main
def hist(word,layout):
    R=[len(f) for f in word['frames']]
    calls=CALL['calls']
    paid=Counter({int(k):v for k,v in CALL['fixed_caller_paid'].items()})
    tg=Counter({int(k):v for k,v in CALL['fixed_root_targets'].items()})
    main=main_roles(layout)
    for i,(a,b) in enumerate(zip(word['initial'],word['final'])):
        if i not in main: tg[abs(R[b]-R[a])]+=calls
    for k,a,b in word['moves']: paid[abs(R[b]-R[a])]+=calls
    return paid,tg
def M(paid,tg,c):
    c=mpf(c); return sum(v*mpf(r)**(1-c) for r,v in tg.items())-sum(v*mpf(r)**(1-c) for r,v in paid.items())
def root(paid,tg,lo='0.0035',hi='0.0045'):
    lo,hi=mpf(lo),mpf(hi)
    for _ in range(140):
        m=(lo+hi)/2
        if M(paid,tg,m)>0: lo=m
        else: hi=m
    return lo
if __name__=='__main__':
    w,l=load(); p,t=hist(w,l)
    print(sorted(p.items())); print(sorted(t.items()))
    c=root(p,t); print('root',mp.nstr(c,15))
    dM=(M(p,t,c+mpf('1e-9'))-M(p,t,c))/mpf('1e-9'); print('dM/dc',dM)
    for g1,g2 in [(1,1),(1,2),(2,2),(1,3),(1,4),(4,4)]:
        d=48*(mpf(g1)**(1-c)+mpf(g2)**(1-c)-mpf(g1+g2)**(1-c))
        print('merge',g1,g2,'dMargin',mp.nstr(d,6),'dc',mp.nstr(-d/dM,6))
    print('remove grade1 per call dc', mp.nstr(-48*(1)/dM,6))
