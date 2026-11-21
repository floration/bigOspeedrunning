# fast float evaluator of the growth rate for the ProfileCycle recurrence
import sys; sys.path.insert(0,'.')
from model import sub,ch2,auxCost,ordinaryLimit,effCut,externalSlots,positiveResidual,dedupLimit,dedupChoice
from math import log
import functools

@functools.lru_cache(None)
def forms_coupled(q,v):
    out=[]
    for n in range(2*q+2):
        for m in range(2*q+4):
            if ch2(n+m)<=q*n+(q+1)*m:
                out.append((n,sub(sub(v,1),n),sub(m*(q+1),ch2(m)),ch2(m)))
    return prune(out)
@functools.lru_cache(None)
def forms_ordinary(q,v):
    out=[]
    for n in range(2*q+2):
        for m in range(2*q+4):
            if ch2(n+m)>q*n+(q+1)*m: continue
            for u in range(2*q+4):
                if n+u<=sub(v,1) and u<=m and u<=ordinaryLimit(q,m,u):
                    L=ordinaryLimit(q,m,u)
                    out.append((n,sub(sub(sub(v,1),u),n),L,sub(m*(q+1),L)))
    return prune(out)
@functools.lru_cache(None)
def forms_source(v,w):
    out=[]
    for n in range(2):
        for m in range(4):
            for u in range(4):
                ec=effCut(v,w,n,u)
                if ch2(n+m)<=m and n+u<=sub(ec,1) and u<=m and u<=ordinaryLimit(0,m,u):
                    L=ordinaryLimit(0,m,u)
                    out.append((n,sub(sub(sub(ec,1),u),n),L,sub(m,L)))
    return prune(out)
@functools.lru_cache(None)
def forms_dedup(q,v):
    out=[]
    for n in range(2*q+2):
        for m in range(2*q+4):
            if ch2(n+m)>q*n+(q+1)*m: continue
            pr=positiveResidual(q,n,m)
            for u in range(2*q+4):
                if n+u<=sub(v,1) and u<=m and u<=dedupLimit(q,n,m,u):
                    dc=dedupChoice(q,n,m,u)
                    out.append((n,sub(sub(sub(v,1),u),n),min(dc,pr+n),sub(externalSlots(q,m),dc)+min(ch2(m),2*m)))
    return prune(out)
def prune(fs):
    fs=list(set(fs))
    keep=[f for f in fs if not any(g!=f and all(g[k]>=f[k] for k in range(4)) for g in fs)]
    return tuple(keep)
def ev(forms,a,b,c,e):
    return max((f[0]*a+f[1]*b+f[2]*c+f[3]*e for f in forms),default=0)

def make_step(K,t,cut,w,d):
    V=lambda q: cut[q] if q<len(cut) else 0
    def coupled(C,Z,Y,i,j):
        T,G,A,Q=C
        a=Z[T[i]][T[j]]; b=Z[G[j]][T[j]]; c=Y[G[j]][G[i]]; e=Y[G[j]][T[j]]
        if j<3: return K*(auxCost(A[i],A[j],False)*a)
        if i<3:
            if A[i]==0: return 0
            mz=Z[min(T[i],G[j])][T[j]]
            if Q[j]==0: return max(a+(t-2)*mz,(t-1)*mz)
            q=Q[j]; v=V(q); m=min(v-1,2*q+1)
            return m*a+(v-1-m)*min(a,mz)
        if Q[j]==0:
            if Q[i]==0:
                return max(a+c+(t-3)*b,a+e+(t-2)*b,c+e+(t-3)*b,2*e+(t-2)*b,3*e+(t-4)*b)
            return max(a+(t-2)*b,(t-1)*b)
        if Q[i]==Q[j]: return ev(forms_coupled(Q[j],V(Q[j])),a,b,c,e)
        q=Q[j]; v=V(q); m=min(v-1,2*q+1)
        return m*a+(v-1-m)*b
    def zero(C,Z,Y,i,j):
        T,G,A,Q=C
        a=Z[T[i]][T[j]]; b=Z[G[j]][T[j]]; c=Y[G[j]][G[i]]; e=Y[G[j]][T[j]]
        cp=coupled(C,Z,Y,i,j)
        # ordinary
        if i>=3 and Q[i]==Q[j]:
            ordv=min(cp,ev(forms_ordinary(Q[j],V(Q[j])),a,b,c,e))
            dd=min(cp,ev(forms_dedup(Q[j],V(Q[j])),a,b,c,e))
        else:
            ordv=cp; dd=cp
        # source
        if i>=3 and Q[i]==0 and Q[j]==0:
            src=min(ordv,ev(forms_source(t,w),a,b,c,e))
        else: src=ordv
        # full
        if j<3: full=src
        elif i<3:
            if A[i]==0: full=src
            elif Q[j]==0:
                mz=Z[min(T[i],G[j])][T[j]]
                full=max(a+(w-2)*mz,(t-1)*mz)
            else: full=src
        elif Q[j]==0:
            if Q[i]==0:
                full=min(src,max(a+c+(w-3)*b,a+e+(w-2)*b,c+e+(w-3)*b,2*e+(w-2)*b,3*e+(w-3)*b,(t-1)*b))
            else: full=max(a+(w-2)*b,(t-1)*b)
        else: full=src
        return min(full,dd)
    def one(C,Z,Y,i,j):
        T,G,A,Q=C
        if j<3: return auxCost(A[i],A[j],True)*Y[T[i]][T[j]]
        if i<3: return auxCost(A[i],2,True)*Y[T[i]][T[j]]
        r=2*Y[T[i]][T[j]]
        if Q[i]==Q[j]: r+=max(d-Q[j],0)*Z[G[j]][G[i]]
        return r
    def env(A,n):
        E=[[0]*n for _ in range(n)]
        for i in range(n-1,-1,-1):
            for j in range(i,n):
                x=A[i][j]
                if j>i: x=min(x,E[i][j-1],E[i+1][j])
                E[i][j]=x
        return E
    def step(C,Z,Y,n):
        rz=[[0]*n for _ in range(n)]; ry=[[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i,n):
                rz[i][j]=zero(C,Z,Y,i,j); ry[i][j]=one(C,Z,Y,i,j)
        return env(rz,n),env(ry,n)
    return step

def growth(step,word,n,iters=300,K=14055):
    Z=[[1.0 if i<=j else 0.0 for j in range(n)] for i in range(n)]; Y=[r[:] for r in Z]
    L=len(word); tot=0.0; cnt=0
    for it in range(iters):
        for C in word:
            Z,Y=step(C,Z,Y,n)
        h=max(max(max(r) for r in Z),max(max(r) for r in Y))
        if it>=iters//2: tot+=log(h); cnt+=1
        Z=[[x/h for x in r] for r in Z]; Y=[[x/h for x in r] for r in Y]
    lam=(tot/cnt)/L
    return log(K)/lam, lam
