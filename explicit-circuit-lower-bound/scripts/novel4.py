# Same model, more degree classes w1..w4 (w4 = deg>=4). Case 4 deg (i,j): fix x kills i+1 gates (XOR children),
# y drops one degree; pairing then Case 1 gives 4 gates for i>=3. Reroute: any w_k' - w_k <= 1 for k'>k.
import itertools
R=[x/2 for x in range(0,31)]
best=(-1,)
for w1,w2,w3,w4,be in itertools.product(R,R,R,R,R):
    w=[0,w1,w2,w3,w4]
    W=lambda k: w[min(k,4)]
    if any(w[b]-w[a]>1 for a in range(1,5) for b in range(a+1,5)): continue   # reroute up
    if any(w[a-1]-w[a]>1 for a in range(2,5)): continue                      # deletion lowers degree
    if -2-be+w1>0: continue   # Case 1 / 3, partner deg 1
    if -2-be+max(w2,w3,w4)>0: continue  # Case 1, high-degree partner (via reroute; no surcharge)
    D=99
    for i in range(1,6):
        for j in range(1,6):
            if j>i: continue
            fix = (i+1) + W(i) + W(j)-W(j-1)            # fix x (deg i): G,H,i-1 others; y drops a degree
            if i==1: fix = 2 + W(1) + W(j)-W(j-1)
            pair = 2 - be + W(i) + W(j)
            if i>=3: pair = 4 + W(i) + W(j) - W(j-1)   # pair then Case 1 on x
            D=min(D,max(fix,pair))
    D=min(D, 2+be+w1, 3+be+w2, 2+2*be)
    c=D-max(w)
    if c>best[0]+1e-9: best=(c,w[1:],be,D)
print(best)
