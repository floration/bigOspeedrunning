from model import *
from mpmath import mpf
w,l=load(); R=[len(f) for f in w['frames']]; F=w['frames']
SP=[span(f) for f in F]; NC=len(F)
p,t=hist(w,l); c=root(p,t); dM=(M(p,t,c+mpf('1e-12'))-M(p,t,c))/mpf('1e-12')
f=lambda g: mpf(g)**(1-c)
fld=set(w['initial'])|set(w['final'])
ins=defaultdict(list); outs=defaultdict(list)
for k,a,b in w['moves']: outs[a].append(b); ins[b].append(a)
def nest(x,y): return SP[x]<SP[y] or SP[y]<SP[x]
best=[]
for b in range(NC):
    if b in fld or not (ins[b] or outs[b]): continue
    nb=set(ins[b])|set(outs[b])
    for b2 in range(NC):
        if b2==b: continue
        if b2 in nb: ok=False; continue
        if all(nest(x,b2) for x in nb):
            cur=sum(f(abs(R[b]-R[x])) for x in ins[b]+outs[b])
            new=sum(f(abs(R[b2]-R[x])) for x in ins[b]+outs[b])
            lin=sum(abs(R[b2]-R[x])-abs(R[b]-R[x]) for x in ins[b]+outs[b])
            dc=-48*(new-cur)/dM*0+(48*(new-cur))/(-dM)*(-1)
            best.append((float(48*(cur-new)/(-dM)),lin,b,b2,R[b],R[b2],len(ins[b]),len(outs[b])))
best.sort(reverse=True)
print(len(best)); 
for x in best[:15]: print(x)
