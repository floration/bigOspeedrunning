# Independent check of the mod-37 product construction (run: python3 -I check_construction.py)
A1=[0,2,3,5,9,19,26,27,30,31]; A2=[0,1,3,7,17,24,25,28,29,35]
def cyc_free(A,W):
    return all((a+b-2*c)%W or a==b==c for a in A for b in A for c in A)
assert cyc_free(A1,37) and cyc_free(A2,37)
def tern01(c):
    while c:
        if c%3==2: return False
        c//=3
    return True
C=[c for c in range(119) if tern01(c)]; assert len(C)==30
S=sorted(a+37*b+1369*c for a in A1 for b in A2 for c in C)[:2921]
assert S==sorted(map(int,open('packing_2921.txt').read().split()))
print('A1,A2 3AP-free mod 37; C = 30 binary-ternary words; S matches packing_2921.txt; max',S[-1])
