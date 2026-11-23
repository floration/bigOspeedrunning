from model import *
from mpmath import mpf
w,l=load(); R=[len(f) for f in w['frames']]; F=w['frames']
SP=[span(f) for f in F]; NC=len(F)
p,t=hist(w,l); c=root(p,t); dM=(M(p,t,c+mpf('1e-12'))-M(p,t,c))/mpf('1e-12')
f=lambda g: mpf(g)**(1-c)
n=len(w['initial']); first=w['first_output']
forms=dict((k,r) for k,r in w['forms'])
loc={}  # value -> chart where it is located
for i in range(n): loc[~i]=w['initial'][i]
src={}
for k,a,b in w['moves']: loc[k]=b; src[k]=a
# outputs located where computed
for i in range(n): src[first+i]=w['final'][i]
par={}
def find(x):
    while par.setdefault(x,x)!=x: par[x]=par[par[x]]; x=par[x]
    return x
def uni(a,b): par[find(a)]=find(b)
for k,r in forms.items():
    for d,_ in r: uni(('v',d),('v',k)) if False else None
# component per (chart, consumer k computed at chart src[k]) join with donors
for k,r in forms.items():
    for d,_ in r:
        uni(('c',k),('d',d))
# map: donor d belongs at chart loc[d], consumer k at chart src[k]; same chart necessarily
comp=defaultdict(lambda:{'in':[], 'out':[], 'fixed':False})
for k,r in forms.items():
    ch=src[k]; root_=find(('c',k)); C=comp[(ch,root_)]
    if k>=first and k<first+n: C['fixed']=True
    elif k in loc: C['out'].append(loc[k])
for d in loc:
    ch=loc[d]
    if ('d',d) not in par: continue
    C=comp[(ch,find(('d',d)))]
    if d<0: C['fixed']=True
    else: C['in'].append(src[d])
def nest(x,y): return SP[x]<SP[y] or SP[y]<SP[x]
res=[]; nonfixed=0
from collections import Counter
cnt=Counter(len([1 for (ch,_) in comp if ch==b]) for b in range(NC))
print('components per chart',sorted(cnt.items())[:10])
for (b,_),C in comp.items():
    if C['fixed']: continue
    nonfixed+=1
    nb=C['in']+C['out']; S=set(nb)
    cur=sum(f(abs(R[b]-R[x])) for x in nb); curl=sum(abs(R[b]-R[x]) for x in nb)
    for b2 in range(NC):
        if b2==b or b2 in S: continue
        if all(nest(x,b2) for x in S):
            new=sum(f(abs(R[b2]-R[x])) for x in nb)
            res.append((float(48*(cur-new)/(-dM)),sum(abs(R[b2]-R[x]) for x in nb)-curl,b,b2,R[b],R[b2],len(C['in']),len(C['out'])))
res.sort(reverse=True); print('nonfixed comps',nonfixed,'cands',len(res))
for x in res[:15]: print(x)
imb=Counter()
ex=[]
for (b,_),C in comp.items():
    if C['fixed']: continue
    d=len(C['out'])-len(C['in']); imb[d]+=1
    if d!=0 and len(ex)<10: ex.append((b,R[b],[(x,R[x]) for x in C['in']],[(x,R[x]) for x in C['out']]))
print(imb); 
for e in ex: print(e)
