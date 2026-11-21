"""Cutting-plane LP for window weights, with batched vectorised local minimisation (own reimplementation of checks/weights_lp.py)."""
import itertools, sys, time, numpy as np
from scipy.optimize import linprog
import os; A=float(os.environ.get("TILT_A","1.4142135623730951")); t0=A/(2*np.pi); K0=float(np.sinc(t0)); s2=None
from scipy.integrate import quad
def Hval(a):
    W=lambda t: np.cos(a*t)
    I1=quad(W,-.5,.5)[0]; I2=quad(lambda t:W(t)**2,-.5,.5)[0]
    inner=lambda s: quad(lambda t:W(t)*(s-t),-.5,s)[0]
    I3=2*quad(lambda s:W(s)*inner(s),-.5,.5,epsabs=1e-13,epsrel=1e-13)[0]
    return 2-(I2+I3)/I1**2
H=Hval(A)
print("A",A,"H",H,flush=True)
def k(x): return 0.5*(np.sinc(x-t0)+np.sinc(x+t0))/K0
def dsinc(t):
    out=np.zeros_like(t); nz=np.abs(t)>1e-9; tt=t[nz]
    out[nz]=(np.cos(np.pi*tt)-np.sinc(tt))/tt; return out
def dk(x): return 0.5*(dsinc(x-t0)+dsinc(x+t0))/K0
R=int(sys.argv[1]); mu=float(sys.argv[2]); iters=int(sys.argv[3]); bmin=float(sys.argv[4]); n=R-1
out=f"my_R{R}_mu{mu}_a{A:.4f}.npz"
pairs=[(r,i) for r in range(1,R) for i in range(R-r)]; P=len(pairs); pr=np.array([p[0] for p in pairs])
M=np.zeros((P,n))
for j,(r,i) in enumerate(pairs): M[j,i:i+r]=1
perm=list(range(n))[::-1]+[n+pairs.index((r,R-1-r-i)) for r,i in pairs]
def F(G,x):  # G: (B,n)
    D=G@M.T; kd=k(D); f=G@x[:n]+(kd**2)@x[n:]
    g=x[:n]+(2*kd*dk(D)*x[n:])@M
    return f,g
def batch_min(G,x,steps=3000):
    G=G.copy(); lr=np.full(len(G),0.05)
    f,g=F(G,x)
    for s in range(steps):
        Gn=np.clip(G-lr[:,None]*g,0.3,60); fn,gn=F(Gn,x)
        ok=fn<=f
        G[ok]=Gn[ok]; f[ok]=fn[ok]; g[ok]=gn[ok]
        lr=np.where(ok,lr*1.2,lr*0.5)
        if s%200==199 and np.all(lr<1e-9): break
    return f,G
starts=[np.array(w) for w in itertools.product([1.04,1.98],repeat=n)]
starts+=[np.array(w) for w in itertools.product([1.04,1.98,3.0],repeat=n) if sum(np.array(w)==3.0)==1]
starts=np.array(starts); rng=np.random.default_rng(1)
def search(x,extra=None):
    S=starts if extra is None else np.vstack([starts,extra])
    f,G=batch_min(S,x)
    best={}
    for fi,gi in zip(f,G):
        key=tuple(np.round(gi,4)); best[key]=min(best.get(key,1e9),fi)
    return sorted(((v,np.array(kk)) for kk,v in best.items()),key=lambda p:p[0])
x0=np.concatenate([np.full(n,mu/n),2.0/(R-pr)]); nv=n+P
t=time.time(); b=search(x0)
print(f"uniform: c0={b[0][0]:.7f} bound={(H-mu)/(1-b[0][0]):.7f} t={time.time()-t:.0f}s",flush=True)
cuts=[g for _,g in b[:60]]; cuts+=[g[::-1] for g in cuts]; best=(b[0][0],x0)
for it in range(iters):
    feats=lambda g: np.concatenate([g,k(M@g)**2])
    A=[np.concatenate([-feats(g),[1.0]]) for g in cuts]
    for r in range(1,R): A.append(np.concatenate([np.zeros(n),(pr==r).astype(float),[0.0]]))
    bub=[0.0]*len(cuts)+[2.0]*(R-1)
    Aeq=[np.concatenate([np.ones(n),np.zeros(P),[0.0]])]; beq=[mu]
    for j in range(nv):
        if perm[j]>j:
            e=np.zeros(nv+1); e[j]=1; e[perm[j]]=-1; Aeq.append(e); beq.append(0.0)
    res=linprog(np.concatenate([np.zeros(nv),[-1.0]]),A_ub=A,b_ub=bub,A_eq=Aeq,b_eq=beq,
                bounds=[(bmin*mu/n,None)]*n+[(0,None)]*P+[(None,None)],method="highs")
    x=res.x[:nv]; c_lp=res.x[-1]
    extra=np.array([np.clip(g+rng.normal(0,0.08,n),0.4,50) for g in cuts[-30:]])
    b=search(x,extra)
    if b[0][0]>best[0]: best=(b[0][0],x.copy())
    print(f"it {it}: LP c={c_lp:.7f} true min={b[0][0]:.7f} bound={(H-mu)/(1-b[0][0]):.7f} best={(H-mu)/(1-best[0]):.7f} t={time.time()-t:.0f}s",flush=True)
    new=[g for f,g in b[:40] if f<c_lp-1e-10]
    cuts+=new+[g[::-1] for g in new]
    np.savez(out,cuts=np.array(cuts),c=best[0],x=best[1])
    if not new: break
c,x=best
print(f"best: c={c:.8f} bound={(H-mu)/(1-c):.8f}")
