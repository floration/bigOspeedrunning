import sys, os, itertools, numpy as np
A=float(os.environ.get("TILT_A","1.4142135623730951")); t0=A/(2*np.pi); K0=float(np.sinc(t0))
def k(x): return 0.5*(np.sinc(x-t0)+np.sinc(x+t0))/K0
def dsinc(t):
    out=np.zeros_like(t); nz=np.abs(t)>1e-9; tt=t[nz]; out[nz]=(np.cos(np.pi*tt)-np.sinc(tt))/tt; return out
def dk(x): return 0.5*(dsinc(x-t0)+dsinc(x+t0))/K0
R=int(sys.argv[2]); n=R-1; x=np.load(sys.argv[1])
pairs=[(r,i) for r in range(1,R) for i in range(R-r)]; P=len(pairs)
M=np.zeros((P,n))
for j,(r,i) in enumerate(pairs): M[j,i:i+r]=1
def F(G):
    D=G@M.T; kd=k(D); return G@x[:n]+(kd**2)@x[n:], x[:n]+(2*kd*dk(D)*x[n:])@M
def bmin(G,steps=4000):
    G=G.copy(); lr=np.full(len(G),0.05); f,g=F(G)
    for s in range(steps):
        Gn=np.clip(G-lr[:,None]*g,0.0,80); fn,gn=F(Gn); ok=fn<=f
        G[ok]=Gn[ok]; f[ok]=fn[ok]; g[ok]=gn[ok]; lr=np.where(ok,lr*1.2,lr*0.5)
    return f,G
rng=np.random.default_rng(7)
S=[np.array(w) for w in itertools.product([1.04,1.97],repeat=n)]
S+=[np.array(w) for w in itertools.product([1.04,1.97,3.0],repeat=n) if sum(np.array(w)==3.0)==1]
S=np.array(S); S=np.vstack([S, np.clip(S[rng.integers(0,len(S),4000)]+rng.normal(0,0.15,(4000,n)),0,None), rng.uniform(0,4,(4000,n))])
f,G=bmin(S); i=np.argsort(f)[:5]
for j in i: print(f"{f[j]:.9f}", np.round(G[j],4))
