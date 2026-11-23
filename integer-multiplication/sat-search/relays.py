from model import *
w,l=load()
F=w['frames']; R=[len(f) for f in F]; S=[span(f) for f in F]
mv={k:(a,b) for k,a,b in w['moves']}; forms={k:dict(r) for k,r in w['forms']}
cons=defaultdict(list)
for k,r in forms.items():
    for d in r: cons[d].append(k)
nest=lambda a,b: S[a]<S[b] or S[b]<S[a]
g=lambda a,b: abs(R[a]-R[b])
cnt=Counter(); ex=[]
for y,(b,c) in mv.items():
    r=forms[y]
    if len(r)!=1: cnt['multi-donor']+=1; continue
    x=next(iter(r))
    if x<0: cnt['single input donor']+=1; continue
    a,b2=mv[x]; assert b2==b
    if len(cons[x])>1: cnt['donor fans out']+=1; continue
    cnt['pure relay']+=1
    mono = (S[a]<S[b]<S[c]) or (S[a]>S[b]>S[c])
    ex.append((x,y,a,b,c,g(a,b),g(b,c),nest(a,c) and a!=c, mono, g(a,c) if nest(a,c) else None))
print(cnt)
print(Counter((e[5],e[6],e[7],e[8],e[9]) for e in ex))
for e in ex[:10]: print(e)
