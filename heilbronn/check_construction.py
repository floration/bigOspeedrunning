# Independent check of the mod-37 product construction (run: python3 -I check_construction.py)
A1=[0,2,3,5,9,19,26,27,30,31]; A2=[0,1,3,7,17,24,25,28,29,35]
C=[0,1,3,4,9,10,12,13,28,29,31,35,36,38,51,65,78,80,81,85,87,88,103,104,106,107,112,113,115,116]
def cyc_free(A,W):
    return all((a+b-2*c)%W or a==b==c for a in A for b in A for c in A)
assert cyc_free(A1,37) and cyc_free(A2,37)
assert all(a+b!=2*c or a==b==c for a in C for b in C for c in C) and len(C)==30
S=sorted(a+37*b+1369*c for a in A1 for b in A2 for c in C)[:2921]
assert S==sorted(map(int,open('packing_2921.txt').read().split()))
print('A1,A2 3AP-free mod 37; C 3AP-free in [0,117); S matches packing_2921.txt; max',S[-1])
