# Novel: period-L words of distinct recipes at K=14055
import sys,random,time,json; sys.path.insert(0,'.')
from word import *
L=int(sys.argv[1]); seed=int(sys.argv[2]); tmax=float(sys.argv[3]); random.seed(seed)
n=16; st=make_step(14055,24,[24,31,38,44,50,55],22,7027)
base=([7, 8, 8, 8, 8, 9, 10, 10, 10, 11, 11, 12, 13, 14, 15, 15],[15, 15, 15, 8, 8, 8, 8, 8, 8, 8, 7, 6, 5, 4, 3, 1],[0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 5, 4, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0])
def valid(C):
    T,G,A,Q=C
    if any(T[i]>T[i+1] for i in range(n-1)): return False
    if not (A[0]<=A[1]<=A[2]): return False
    for i in range(3,n-1):
        if G[i+1]>G[i] or Q[i+1]>Q[i]: return False
    return all(G[i]<=T[i] and 0<=Q[i]<=5 for i in range(3,n))
cur=[tuple(list(x) for x in base) for _ in range(L)]
sc=lambda w: growth_word([(st,C,14055) for C in w],n,max(60,200//L))
cs=sc(cur); best=(cs,cur); t0=time.time(); temp=0.003
print('start',cs,flush=True)
while time.time()-t0<tmax:
    w=[tuple(list(x) for x in C) for C in cur]; p=random.randrange(L)
    T,G,A,Q=w[p]
    for _ in range(random.randint(1,4)):
        k=random.randrange(4); i=random.randrange(n)
        if k==0: T[i]=max(0,min(n-1,T[i]+random.choice([-1,1])))
        elif k==1: G[i]=max(0,min(n-1,G[i]+random.choice([-1,1,-2,2])))
        elif k==2 and i<3: A[i]=random.randrange(3)
        elif k==3 and i>=3: Q[i]=max(0,min(5,Q[i]+random.choice([-1,1])))
    if not valid(w[p]): continue
    s=sc(w)
    if s>cs or random.random()<exp((s-cs)/temp):
        cur,cs=w,s
        if s>best[0]: best=(s,w); print(round(time.time()-t0),s,flush=True)
    temp=max(2e-5,temp*0.999)
print('BEST',growth_word([(st,C,14055) for C in best[1]],n,400),json.dumps(best[1]),flush=True)
