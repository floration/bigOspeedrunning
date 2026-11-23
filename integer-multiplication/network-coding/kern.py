import sys; sys.path.insert(0,'/tmp/claude-0/w/s')
from load import *
w,moves,forms,val,chart,src=load(sys.argv[1])
F=w['frames']
L=defaultdict(list); D=defaultdict(list); O=defaultdict(list)
for i,s in enumerate(w['initial']): L[s].append(~i)
for k,(a,b) in moves.items(): D[b].append(k); O[a].append(k)
for k in forms:
    if k not in moves: O[src[k]].append(k)
def nullvec(M):
    # right kernel of M (rows x m) mod p, return list of basis vectors
    M=np.array(M,dtype=np.int64)%p; rows,m=M.shape; piv=[]; r=0
    for c in range(m):
        pr=None
        for i in range(r,rows):
            if M[i,c]: pr=i;break
        if pr is None: continue
        M[[r,pr]]=M[[pr,r]]; M[r]=M[r]*pow(int(M[r,c]),p-2,p)%p
        for i in np.nonzero(M[:,c])[0]:
            if i!=r: M[i]=(M[i]-M[i,c]*M[r])%p
        piv.append(c); r+=1
    free=[c for c in range(m) if c not in piv]; out=[]
    for f in free:
        z=np.zeros(m,dtype=np.int64); z[f]=1
        for i,c in enumerate(piv): z[c]=(-M[i,f])%p
        out.append(z)
    return out
# the 14 charts
for c in [243,394,470,477,517,518,529,531,541,543,591,595,599,1091]:
    # express outputs in terms of forms directly: each output form references values at chart c
    ins=L[c]+D[c]; idx={x:i for i,x in enumerate(ins)}
    C=[]
    for o in O[c]:
        row=np.zeros(len(ins),dtype=np.int64)
        for d,co in forms[o]: row[idx[d]]=(row[idx[d]]+modq(co))%p
        C.append(row)
    ks=nullvec(C)
    # kernel restricted: directions of inputs unused by every form
    for z in ks:
        S=[ins[i] for i in np.nonzero(z)[0]]
        print('chart',c,'dim',len(F[c]),'support',[(x, 'in' if x<0 else moves[x], len(F[moves[x][0]]) if x>=0 else None) for x in S])
