# Binary (GF(2)) port of the Gaussian relay bypass: X: a->b and pure relay Y: b->c (Y = X), both
# carrying only frame-0 inputs; replace by D: a->c, re-read D at c, re-encode the frame-0 inputs.
import json,gzip,sys,collections
sys.path.insert(0,'/home/claude/bin'); from parse import parse,evaluate
P='/home/claude/k7/research/p104-k7-retimed-binary/strong-bit-k7.json.gz'
w,n,moves,forms,outs,clears,lf,nl=parse(P)
fr=w['frames']; dim={int(k):v['dim'] for k,v in fr.items()}
def span(B):
    s={0}
    for row in B:
        v=int(''.join(str(x&1) for x in row),2); s|={o^v for o in s}
    return frozenset(s)
SP={int(k):span(v['B']) for k,v in fr.items()}
mv={t:(a,b) for t,a,b,r in moves}
order=[t for t,_,_,_ in moves]
O,_,val=evaluate(n,forms,order,[o[1] for o in outs],[])
# output scalars as labels nl+j with forms = outs sets
OUT=[nl+j for j in range(n)]
allforms=dict(forms); 
for j in range(n): allforms[OUT[j]]=outs[j][1]
src={t:mv[t][0] for t in mv}; 
for j in range(n): src[OUT[j]]=outs[j][0]
def bits(s):
    while s:
        l=(s&-s).bit_length()-1; yield l; s&=s-1
# GF(2) inverse of M (rows = outputs, bitmask over inputs)
def inv(rows):
    m=len(rows); A=[(rows[i],1<<i) for i in range(m)]
    for c in range(m):
        piv=next(i for i in range(c,m) if A[i][0]>>c&1); A[c],A[piv]=A[piv],A[c]
        for i in range(m):
            if i!=c and A[i][0]>>c&1: A[i]=(A[i][0]^A[c][0],A[i][1]^A[c][1])
    return [A[i][1] for i in range(m)]  # row i of Minv: bitmask over outputs
Minv=inv(O)
Xl=[i for i in range(n) if w['start'][i]!=0]; T0=[i for i in range(n) if w['start'][i]==0]
Xmask=sum(1<<i for i in Xl)
# z over X rows: z_out_j bit k set if Minv[Xl[k]] has bit j
zo=[0]*n
for k,i in enumerate(Xl):
    for j in bits(Minv[i]): zo[j]|=1<<k
Z=collections.defaultdict(int)
for j in range(n): Z[OUT[j]]=zo[j]
readers=collections.defaultdict(list)
for k,f in allforms.items():
    for d in bits(f): readers[d].append(k)
for t in reversed(order):
    z=0
    for r in readers[t]: z^=Z[r]
    Z[t]=z
uX0={t for t in mv if not val[t]&Xmask}
at=collections.defaultdict(list)
for k in allforms: at[src[k]].append(k)
def insolve(vecs,target):
    basis={}  # pivot bit -> (vec, combo)
    for idx,v in enumerate(vecs):
        c=1<<idx
        while v:
            h=v.bit_length()-1
            if h in basis: v^=basis[h][0]; c^=basis[h][1]
            else: basis[h]=(v,c); break
    v=target; c=0
    while v:
        h=v.bit_length()-1
        if h not in basis: return None
        v^=basis[h][0]; c^=basis[h][1]
    return c
pairs=[]
for y in uX0:
    f=allforms[y]
    if f&(f-1): continue  # pure relay: single donor
    x=f.bit_length()-1
    if x in uX0 and x in mv and mv[x][1]==mv[y][0]:
        a,b=mv[x]; c=mv[y][1]
        if SP[a]<SP[b]<SP[c]: pairs.append((x,y,a,b,c))
print('uX0',len(uX0),'pure nested frame-0 relay pairs',len(pairs),flush=True)
def check(nf):
    from graphlib import TopologicalSorter, CycleError
    deps={k:tuple(bits(f)) for k,f in nf.items()}
    try: od=[k for k in TopologicalSorter(deps).static_order() if k in nf]
    except CycleError: return 'cycle',None
    v={i:1<<i for i in range(n)}
    for k in od:
        s=0
        for d in bits(nf[k]): s^=v[d]
        v[k]=s
    F=[v[OUT[j]] for j in range(n)]
    # E = Minv F : row i = XOR of F[j] for j in Minv[i]
    E=[]
    for i in range(n):
        s=0
        for j in bits(Minv[i]): s^=F[j]
        E.append(s)
    for i in Xl:
        if E[i]!=1<<i: return 'X rows',None
    T0mask=sum(1<<i for i in T0)
    for i in T0:
        if E[i]&Xmask: return '0X',None
    # rank of E00
    rows=[E[i] for i in T0]; r=0; basis={}
    for v_ in rows:
        while v_:
            h=v_.bit_length()-1
            if h in basis: v_^=basis[h]
            else: basis[h]=v_; r+=1; break
    return ('OK' if r==len(T0) else f'00 rank {r}'),E
if __name__=='__main__':
    stat=collections.Counter(); good=[]
    newlab=nl+n
    for x,y,a,b,c in pairs:
        Oc=at[c]
        cc=insolve([Z[r] for r in Oc],Z[x])
        if cc is None: stat['c span']+=1; continue
        nf=dict(allforms); D=newlab
        nf[D]=allforms[x]; del nf[x],nf[y]
        for k in at[b]:
            if k in nf and nf[k]>>x&1: nf[k]^=1<<x
        for k in Oc:
            if k in nf and nf[k]>>y&1: nf[k]^=1<<y
        for idx in bits(cc): nf[Oc[idx]]^=1<<D
        msg,_=check(nf); stat[msg.split(' rank')[0]]+=1
        if msg=='OK': good.append(dict(x=x,y=y,a=a,b=b,c=c,g=[dim[b]-dim[a],dim[c]-dim[b]],cc=[Oc[i] for i in bits(cc)])); print('PASS',good[-1],flush=True)
    print(dict(stat)); json.dump(good,open('bgood.json','w'))
