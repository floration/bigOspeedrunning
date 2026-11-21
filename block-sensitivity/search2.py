import sys,random,time,json; sys.path.insert(0,'.')
from fast import *
from math import exp
cfg=sys.argv[1]; seed=int(sys.argv[2]); n=int(sys.argv[3]); tmax=float(sys.argv[4])
random.seed(seed)
CFG={'k14055':(14055,24,[24,31,38,44,50,55],22,7027),
     'k5591':(5591,21,[21,29,35,41,47,52,57,63,68],19,2795)}
K,t,cut,w,d=CFG[cfg]; QMAX=len(cut)-1
st=make_step(K,t,cut,w,d)
def valid(C):
    T,G,A,Q=C
    if any(T[i]>T[i+1] for i in range(n-1)): return False
    if not (A[0]<=A[1]<=A[2]): return False
    for i in range(3,n-1):
        if G[i+1]>G[i] or Q[i+1]>Q[i]: return False
    for i in range(3,n):
        if G[i]>T[i] or not (0<=Q[i]<=QMAX): return False
    return True
base=([7, 8, 8, 8, 8, 9, 10, 10, 10, 11, 11, 12, 13, 14, 15, 15],[15, 15, 15, 8, 8, 8, 8, 8, 8, 8, 7, 6, 5, 4, 3, 1],[0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 5, 4, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0])
def grow(C,extra):
    # insert `extra` ordinary states by duplicating a random ordinary state and reindexing
    T,G,A,Q=[list(x) for x in C]
    for _ in range(extra):
        m=len(T); p=random.randrange(3,m)
        f=lambda x: x+1 if x>p else x   # new state p+1 copy of p
        T=[f(x) for x in T]; G=[f(x) for x in G]
        T.insert(p+1,T[p]); G.insert(p+1,G[p]); A.insert(p+1,A[p]); Q.insert(p+1,Q[p])
    return (T,G,A,Q)
cur=grow(base,n-16)
assert valid(cur),cur
def score(C,it=100):
    return growth(st,[C],n,it,K=K)[0]
cs=score(cur); best=(cs,cur); t0=time.time(); temp=0.003
print("start",cs,flush=True)
while time.time()-t0<tmax:
    T,G,A,Q=[list(x) for x in cur]
    for _ in range(random.randint(1,4)):
        k=random.randrange(4); i=random.randrange(n)
        if k==0: T[i]=max(0,min(n-1,T[i]+random.choice([-1,1])))
        elif k==1: G[i]=max(0,min(n-1,G[i]+random.choice([-1,1,-2,2])))
        elif k==2 and i<3: A[i]=random.randrange(3)
        elif k==3 and i>=3: Q[i]=max(0,min(QMAX,Q[i]+random.choice([-1,1])))
    C=(T,G,A,Q)
    if not valid(C): continue
    s=score(C)
    if s>cs or random.random()<exp((s-cs)/temp):
        cur,cs=C,s
        if s>best[0]:
            best=(s,C); print(round(time.time()-t0),s,json.dumps(C),flush=True)
    temp=max(2e-5,temp*0.9993)
print("BEST",score(best[1],400),json.dumps(best[1]),flush=True)
