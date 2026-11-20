"""Checks for the 29-edge witness: 6x5 minus edge (p6,r5) forces the contradiction on 8 locus pairs; no 28-edge subgraph of 6x5 does (plane/plane). Numerical sanity check, not a proof."""
import numpy as np, itertools, sys
sys.argv=['x']; import os; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'check_grid.py')).read().split("if __name__")[0])
def matrix_e(rng,P,Q,edges):
    N,j=len(P),len(Q); V=3*(N+j); rows=[]
    for (i,l) in edges:
        d=P[i]-Q[l]; L=d@d; R=np.sqrt(complex(L*(L-4)))*rng.choice([-1,1])
        row=np.zeros(V,complex); row[3*i:3*i+2]=2*d; row[3*i+2]=-R
        o=3*N+3*l; row[o:o+2]=-2*d; row[o+2]=R; rows.append(row)
    return np.array(rows)
def test(N,j,missing,loci,seed):
    rng=np.random.default_rng(seed)
    edges=[(i,l) for i in range(N) for l in range(j) if (i,l) not in missing]
    P=sample(rng,loci[0],N); Q=sample(rng,loci[1],j)
    d,K=kernel(matrix_e(rng,P,Q,edges))
    f=[e for e in edges if forced(K,N,*e)]
    return d,len(f),len(edges)
for loci in LOCI:
  for seed in range(5):
    r=test(6,5,{(5,4)},loci,seed)
    if seed==0 or r[1]==0: print('29 edges',loci,seed,'kerdim,forced,E=',r)
# all 28-edge subgraphs of 6x5 (remove 2 edges) on plane/plane
cnt=0;bad=0
for m in itertools.combinations([(i,l) for i in range(6) for l in range(5)],2):
    d,f,E=test(6,5,set(m),('plane','plane'),cnt); cnt+=1
    if f>0: bad+=1
print('28-edge subgraphs of 6x5 with a forced contradiction:',bad,'of',cnt)
# 5x6 minus one edge too
print('5x6 minus edge', test(5,6,{(4,5)},('plane','plane'),3))
