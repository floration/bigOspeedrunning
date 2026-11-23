# Degree-split weights + both-constants trick for high-degree inputs in Case 4 + pair degree surcharge sg.
import itertools
def run(R, S):
    best=(-1,)
    for w1,w2,be,sg in itertools.product(R,R,R,S):
        c0 = [w2-w1-1, w1-w2-1,           # reroute 1->2 / deletion 2->1, one gate deleted
              sg-1,                       # reroute raises a paired param to deg>=2
              -2-be-sg+w1,                # Case 1: p deg>=2, partner deg 1
              -2-be-2*sg+w2,              # Case 1: both deg>=2
              -2-be+w1]                   # Case 3
        if max(c0)>1e-9: continue
        D=min(2+2*w1,                       # Case 4 (1,1): fix x, y unused
              3+w1+w2,                      # Case 4 (1,>=2): fix y, x unused
              max(2-be+2*w2, 3+w2+(w2-w1)), # Case 4 (2,2): pair, or fix x (y drops to deg 1)
              5+w2+min(0,w2-w1),            # Case 4 (>=3, y): better of x<-alpha / x<-alpha+1
              2+be+w1, 3+be+w2, 2+2*be)     # Case 5
        c=D-max(w1,w2)
        if c>best[0]+1e-9: best=(round(c,3),w1,w2,be,sg,D)
    return best
print(run([x/4 for x in range(0,61)], [x/4 for x in range(0,5)]))
