import sys; sys.path.insert(0,'.')
from word import *
from math import log2,ceil
n=16
C=([7, 8, 8, 8, 8, 9, 10, 10, 10, 11, 11, 12, 13, 14, 15, 15],[15, 15, 15, 8, 8, 8, 8, 8, 8, 8, 7, 6, 5, 4, 3, 1],[0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 5, 4, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0])
A=make_step(14055,24,[24,31,38,44,50,55],22,7027)
B=make_step(5591,21,[21,29,35,41,47,52],19,2795)
print('idea2 mixed tournaments')
print(' all-14055', growth_word([(A,C,14055)],n,300))
print(' all-5591 ', growth_word([(B,C,5591)],n,300))
print(' alt A,B  ', growth_word([(A,C,14055),(B,C,5591)],n,300))
print(' A,A,B    ', growth_word([(A,C,14055),(A,C,14055),(B,C,5591)],n,300))
def params(K,slope=2.26,dens=1.0):
    sh=slope*log2(K/14055)
    cut=[ceil((c+sh)/dens) for c in [24,31,38,44,50,55]]
    t=cut[0]; w=ceil((22+sh)/dens)
    d=int(dens*(K-1)/2)
    return K,t,cut,w,d
print('idea3 scan K with predicted cutoffs')
for K in [1000,2000,3000,5591,8000,14055,30000,100000,1000000,10**8]:
    K_,t,cut,w,d=params(K)
    if w<4 or t<4: continue
    st=make_step(K_,t,cut,w,d)
    print(' K=%d t=%d w=%d -> %.5f'%(K,t,w,growth_word([(st,C,K)],n,250)))
print('idea5 sparser oriented graphs (density p, cutoffs scale 1/p)')
for p in [1.0,0.8,0.6,0.4]:
    K,t,cut,w,d=params(14055,dens=p)
    st=make_step(K,t,cut,w,d)
    print(' p=%.1f d=%d t=%d w=%d -> %.5f'%(p,d,t,w,growth_word([(st,C,K)],n,250)))
