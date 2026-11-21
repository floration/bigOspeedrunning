import sys,os; sys.path.insert(0,'.')
import fastp as F
from math import log2,ceil,log
p=F.PD
C=([7, 8, 8, 8, 8, 9, 10, 10, 10, 11, 11, 12, 13, 14, 15, 15],[15, 15, 15, 8, 8, 8, 8, 8, 8, 8, 7, 6, 5, 4, 3, 1],[0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 5, 4, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0])
K=14055
cut=[ceil(c/p) for c in [24,31,38,44,50,55]]; w=ceil(22/p); t=cut[0]; d=int(p*(K-1)/2)
st=F.make_step(K,t,cut,w,d)
print('p=%.2f'%p, F.growth(st,[C],16,250,K=K)[0])
