"""Round LP weights down to rationals (a: 1e-5, b: 1e-7) and report mu_eff and the numerical min of F with the rounded weights.
usage: TILT_A=.. python3 -I roundw.py npz R out.txt"""
import sys, os, itertools, numpy as np
from fractions import Fraction
z=np.load(sys.argv[1]); R=int(sys.argv[2]); n=R-1; x=z["x"]
pairs=[(r,i) for r in range(1,R) for i in range(R-r)]
DA,DB=10**5,10**7; lines=[]; mu=Fraction(0); tot={}; xr=np.zeros_like(x)
for i in range(n):
    num=int(np.floor(x[i]*DB)); lines.append(f"b {i+1} {num} {DB}"); mu+=Fraction(num,DB); xr[i]=num/DB
for j,(r,i) in enumerate(pairs):
    num=int(np.floor(x[n+j]*DA+1e-9)); num=min(num,int(x[n+j]*DA)) if x[n+j]*DA<1e-9 else num
    num=max(0,int(np.floor(x[n+j]*DA))); lines.append(f"a {r} {i} {num} {DA}"); tot[r]=tot.get(r,0)+num; xr[n+j]=num/DA
assert all(v<=2*DA for v in tot.values()), tot
open(sys.argv[3],"w").write("\n".join(lines)+"\n")
print("mu_eff =",mu,"=",float(mu)," LP c =",float(z["c"]))
np.save(sys.argv[3]+".npy",xr)
