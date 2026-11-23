# Crazy idea: if f were a disperser for images of Z(P) (log-size m - lam*q, lam = 2 - log2 3),
# "dimension" a = m - lam*q. Each case: (dm, dq, dW as function of alpha,beta). Need dW <= D*da.
import math
from scipy.optimize import linprog
def solve(lam):
    # variables: alpha, beta, D ; maximize D - alpha
    # constraint rows: coef_alpha*al + coef_beta*be + coef_D*D <= rhs
    cases = {  # name: (dm, dq, gates, dalpha_count, dbeta_count)  dW = -gates + dbeta*beta + dalpha*alpha
      'case4_PC': (0, +1, 2, -2, +1),
      'case1_deg2': (-1, -1, 2, +1, -1),
      'case1_deg0': (-1, -1, 0, 0, -1),
      'case2': (-1, -1, 1, 0, -1),
      'case3': (-1, -1, 2, +1, -1),
      'case5_k1': (-2, -1, 2, -1, -1),
      'case5_k2': (-3, -2, 2, 0, -2),
    }
    A=[];b=[]
    for n,(dm,dq,g,da_,db_) in cases.items():
        da = dm - lam*dq
        # -g + da_*al + db_*be <= D*da  ->  da_*al + db_*be - da*D <= g
        A.append([da_, db_, -da]); b.append(g)
    A.append([-1,0,0]); b.append(0); A.append([0,-1,0]); b.append(0)
    r = linprog([1,0,-1], A_ub=A, b_ub=b, bounds=[(0,100)]*3)
    al,be,D = r.x
    return D-al, al, be, D
for lam in [1, 2-math.log2(3), 0.5, 0]:
    print(round(lam,3), [round(v,3) for v in solve(lam)])
