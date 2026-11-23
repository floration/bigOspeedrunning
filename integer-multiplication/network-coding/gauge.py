import sys; sys.path.insert(0,'/tmp/claude-0/w/s')
from load import *
w,moves,forms,val,chart,src=load(sys.argv[1])
F=w['frames']
L=defaultdict(list); D=defaultdict(list); O=defaultdict(list)
for i,s in enumerate(w['initial']): L[s].append(~i)
for k,(a,b) in moves.items(): D[b].append(k); O[a].append(k)
for k in forms:
    if k not in moves: O[src[k]].append(k)
avail=lambda c: [val[x] for x in L[c]+D[c]]
def inter(spaces):
    # basis of intersection of list of spans
    cur=spaces[0]
    for S in spaces[1:]:
        if not cur: return []
        M=np.array(cur+S,dtype=np.int64).T
        ks=nullvec(M)
        cur=[ (sum(int(z[i])*np.array(cur[i]) for i in range(len(cur))))%p for z in ks]
        r=rank(cur)
        if r<len(cur): # reduce
            pass
    return cur
for b in [243,394,470,477,517,518,529,531,541,543,591,595,599,1091]:
    ins=L[b]+D[b]; idx={x:i for i,x in enumerate(ins)}
    C=[]
    for o in O[b]:
        row=np.zeros(len(ins),dtype=np.int64)
        for d,co in forms[o]: row[idx[d]]=(row[idx[d]]+modq(co))%p
        C.append(row)
    z=nullvec(C)[0]
    supp=[ins[i] for i in np.nonzero(z)[0]]
    srcs=sorted({moves[x][0] for x in supp})
    I=inter([avail(a) for a in srcs])
    print(b,'sources',srcs,'dims',[rank(avail(a)) for a in srcs],'common',rank(I) if I else 0)
print('--- 599 detail')
b=599
ins=L[b]+D[b]
spaceD=[val[x] for x in D[b]]
I=inter([avail(3),avail(260)])
M=np.array(spaceD+I,dtype=np.int64).T
print('dim span(D_599)=',rank(spaceD),'common',rank(I),'dim(D+common)',rank(spaceD+I))
for x in D[b]: print(x,moves[x],[(d,c) for d,c in forms[x]][:6])
idx={x:i for i,x in enumerate(ins)}
C=[]
for o in O[b]:
    row=np.zeros(len(ins),dtype=np.int64)
    for d,co in forms[o]: row[idx[d]]=(row[idx[d]]+modq(co))%p
    C.append(row)
z=nullvec(C)[0]
print('z',dict((ins[i],int(z[i])) for i in np.nonzero(z)[0]))
ks=nullvec(np.array(spaceD+[-x%p for x in I],dtype=np.int64).T)
for k in ks:
    y=k[:len(spaceD)]
    print('y',dict((D[b][i],int(y[i])) for i in np.nonzero(y)[0]),'y.z',int(sum(int(y[i])*int(z[idx[D[b][i]]]) for i in range(len(y)))%p))
print('outputs at 599:',O[b])
for o in O[b]: print(o, moves.get(o), forms[o])
