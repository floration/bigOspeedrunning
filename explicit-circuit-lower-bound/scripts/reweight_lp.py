# Potential W = s + beta*q + alpha*I; need dW <= -D per unit of a; bound c = D - alpha.
# g1 = gates removed in Case 1(deg>=2)/Case 3, g4 = gates removed in tight Case 4.
import itertools
def best(g1,g4,g5=2):
    b=(-99,0,0)
    for a10 in range(0,301):
        for b10 in range(0,301):
            al,be=a10/10,b10/10
            if al-be>g1: continue          # Case 1/3: -g1-beta+alpha<=0
            D=min(2*al-be+g4,               # Case 4 (PC)
                  2*be+g5,                  # Case 5 k=2
                  al+be+2)                  # Case 5 k=1
            if be<0: continue
            b=max(b,(D-al,al,be))
    return b
for g in [(2,2),(3,2),(2,3),(2.5,2),(2,2.5)]:
    print(g,best(*g))
