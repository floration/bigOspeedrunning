# Python port of SensitivityProfileCycle recurrences (Def_SensitivityProfileCycle.lean)
from math import comb
def sub(a,b): return a-b if a>b else 0
def ch2(x): return x*(x-1)//2

def auxCost(s,t,b):
    if s==0 and t==2: return 0
    if b: return 2 if s==2 else 1
    return 2 if t==0 else 1

def rawOne(h,C,Z,Y,i,j):
    T,G,A,Q=C
    if j<3: return auxCost(A[i],A[j],True)*Y[T[i]][T[j]]
    if i<3: return auxCost(A[i],2,True)*Y[T[i]][T[j]]
    r=2*Y[T[i]][T[j]]
    if Q[i]==Q[j]: r+=sub(h,Q[j])*Z[G[j]][G[i]]
    return r

def targetCost(q,v,a,b):
    m=min(sub(v,1),2*q+1)
    return m*a+sub(sub(v,1),m)*b

def coupledCost(q,v,a,b,c,e):
    best=0
    for n in range(2*q+2):
        for m in range(2*q+4):
            if ch2(n+m)<=q*n+(q+1)*m:
                val=n*a+sub(sub(v,1),n)*b+(sub(m*(q+1),ch2(m))*c+ch2(m)*e)
                if val>best: best=val
    return best

def rawZeroCoupled(k,t,v,C,Z,Y,i,j):
    T,G,A,Q=C
    a=Z[T[i]][T[j]]; b=Z[G[j]][T[j]]; c=Y[G[j]][G[i]]; e=Y[G[j]][T[j]]
    if j<3: return k*(auxCost(A[i],A[j],False)*a)
    if i<3:
        if A[i]==0: return 0
        mz=Z[min(T[i],G[j])][T[j]]
        if Q[j]==0: return max(a+sub(t,2)*mz, sub(t,1)*mz)
        return targetCost(Q[j],v(Q[j]),a,min(a,mz))
    if Q[j]==0:
        if Q[i]==0:
            return max(a+c+sub(t,3)*b, a+e+sub(t,2)*b, c+e+sub(t,3)*b, 2*e+sub(t,2)*b, 3*e+sub(t,4)*b)
        return max(a+sub(t,2)*b, sub(t,1)*b)
    if Q[i]==Q[j]: return coupledCost(Q[j],v(Q[j]),a,b,c,e)
    return targetCost(Q[j],v(Q[j]),a,b)

def ordinaryLimit(q,m,u): return min(sub(u*(q+1),ch2(u)), sub(m*(q+1),ch2(m)))

def ordinaryCost(q,v,a,b,c,e):
    best=0
    for n in range(2*q+2):
        for m in range(2*q+4):
            if ch2(n+m)>q*n+(q+1)*m: continue
            for u in range(2*q+4):
                if n+u<=sub(v,1) and u<=m and u<=ordinaryLimit(q,m,u):
                    L=ordinaryLimit(q,m,u)
                    val=n*a+sub(sub(sub(v,1),u),n)*b+L*c+sub(m*(q+1),L)*e
                    if val>best: best=val
    return best

def effCut(v,w,n,u): return v if n+u==0 else w

def sourceCost(v,w,a,b,c,e):
    best=0
    for n in range(2):
        for m in range(4):
            for u in range(4):
                ec=effCut(v,w,n,u)
                if ch2(n+m)<=m and n+u<=sub(ec,1) and u<=m and u<=ordinaryLimit(0,m,u):
                    L=ordinaryLimit(0,m,u)
                    val=n*a+sub(sub(sub(ec,1),u),n)*b+L*c+sub(m,L)*e
                    if val>best: best=val
    return best

def strictSourceCost(t,w,a,b,c,e):
    return max(a+c+sub(w,3)*b, a+e+sub(w,2)*b, c+e+sub(w,3)*b, 2*e+sub(w,2)*b, 3*e+sub(w,3)*b, sub(t,1)*b)

def rawZeroOrdinary(k,t,v,C,Z,Y,i,j):
    T,G,A,Q=C
    if i>=3 and Q[i]==Q[j]:
        return min(rawZeroCoupled(k,t,v,C,Z,Y,i,j),
                   ordinaryCost(Q[j],v(Q[j]),Z[T[i]][T[j]],Z[G[j]][T[j]],Y[G[j]][G[i]],Y[G[j]][T[j]]))
    return rawZeroCoupled(k,t,v,C,Z,Y,i,j)

def rawZeroSource(k,t,v,w,C,Z,Y,i,j):
    T,G,A,Q=C
    if i>=3 and Q[i]==0 and Q[j]==0:
        # NOTE: Lean passes t (ordinaryCutoff) as sourceCost's v argument
        return min(rawZeroOrdinary(k,t,v,C,Z,Y,i,j),
                   sourceCost(t,w,Z[T[i]][T[j]],Z[G[j]][T[j]],Y[G[j]][G[i]],Y[G[j]][T[j]]))
    return rawZeroOrdinary(k,t,v,C,Z,Y,i,j)

def rawZeroSourceFull(k,t,v,w,C,Z,Y,i,j):
    T,G,A,Q=C
    a=Z[T[i]][T[j]]; b=Z[G[j]][T[j]]; c=Y[G[j]][G[i]]; e=Y[G[j]][T[j]]
    if j<3: return rawZeroSource(k,t,v,w,C,Z,Y,i,j)
    if i<3:
        if A[i]==0: return rawZeroSource(k,t,v,w,C,Z,Y,i,j)
        if Q[j]==0:
            mz=Z[min(T[i],G[j])][T[j]]
            return max(a+sub(w,2)*mz, sub(t,1)*mz)
        return rawZeroSource(k,t,v,w,C,Z,Y,i,j)
    if Q[j]==0:
        if Q[i]==0:
            return min(rawZeroSource(k,t,v,w,C,Z,Y,i,j), strictSourceCost(t,w,a,b,c,e))
        return max(a+sub(w,2)*b, sub(t,1)*b)
    return rawZeroSource(k,t,v,w,C,Z,Y,i,j)

def externalSlots(q,m): return sub(m*(q+1),ch2(m))
def positiveResidual(q,n,m): return min(externalSlots(q,m), sub(q*n+(q+1)*m,ch2(n+m)))
def dedupLimit(q,n,m,u): return min(ordinaryLimit(q,m,u), positiveResidual(q,n,m)+u*n)
def dedupChoice(q,n,m,u): return max(u, min(dedupLimit(q,n,m,u), positiveResidual(q,n,m)+n))
def dedupCost(internal,q,v,a,b,c,e):
    best=0
    for n in range(2*q+2):
        for m in range(2*q+4):
            if ch2(n+m)>q*n+(q+1)*m: continue
            pr=positiveResidual(q,n,m)
            for u in range(2*q+4):
                if n+u<=sub(v,1) and u<=m and u<=dedupLimit(q,n,m,u):
                    dc=dedupChoice(q,n,m,u)
                    val=n*a+sub(sub(sub(v,1),u),n)*b+min(dc,pr+n)*c+(sub(externalSlots(q,m),dc)+internal(m))*e
                    if val>best: best=val
    return best

def rawZeroDedupBoth(k,t,v,C,Z,Y,i,j):
    T,G,A,Q=C
    if i>=3 and Q[i]==Q[j]:
        return min(rawZeroCoupled(k,t,v,C,Z,Y,i,j),
                   dedupCost(lambda m: min(ch2(m),2*m),Q[j],v(Q[j]),Z[T[i]][T[j]],Z[G[j]][T[j]],Y[G[j]][G[i]],Y[G[j]][T[j]]))
    return rawZeroCoupled(k,t,v,C,Z,Y,i,j)

def rawZeroSourceCombined(k,t,v,w,C,Z,Y,i,j):
    return min(rawZeroSourceFull(k,t,v,w,C,Z,Y,i,j), rawZeroDedupBoth(k,t,v,C,Z,Y,i,j))

def envelope(A,n):
    E=[[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i,n):
            E[i][j]=min(A[a][b] for a in range(i,j+1) for b in range(a,j+1))
    return E

class Params:
    def __init__(s,K,t,cut,w,d):
        s.K,s.t,s.cut,s.w,s.d=K,t,cut,w,d
    def v(s,q): return s.cut[q] if q<len(s.cut) else 0

def step(P,C,Z,Y,n):
    rz=[[0]*n for _ in range(n)]; ry=[[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i,n):
            rz[i][j]=rawZeroSourceCombined(P.K,P.t,P.v,P.w,C,Z,Y,i,j)
            ry[i][j]=rawOne(P.d,C,Z,Y,i,j)
    return envelope(rz,n),envelope(ry,n)

P14055=Params(14055,24,[24,31,38,44,50,55],22,7027)
