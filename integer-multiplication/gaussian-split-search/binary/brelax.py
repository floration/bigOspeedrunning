# Over-counting variants of the split scan: (R1) s on inputs starting at a, h on outputs ending at z;
# (R2) cross-chart pairing of G-supported resident forms and G-supported departing adjoints.
import sys
sys.path.insert(0,'/home/claude/work/binary')
from bscan import *
for p in sys.argv[1:]:
    d=load(p); res,w,moves,val,pairs,main=check(d,verbose=False); madj,inadj=adjoint(w); pub=w.pub
    groups=defaultdict(list)
    for i in range(pub):
        if i not in main: groups[(d['start'][i],d['final'][i])].append(i)
    inp=defaultdict(list); arr=defaultdict(list); dep=defaultdict(list)
    for i in range(pub): inp[d['start'][i]].append(1<<i)
    for t,f,a,b,v in moves: arr[b].append(v); dep[a].append(madj[t])
    r1=r1hit=0; cross=crosshit=0
    for (a,z),G in groups.items():
        mA=sum(1<<i for i in range(pub) if d['start'][i]==a); mZ=sum(1<<i for i in range(pub) if d['final'][i]==z)
        mG=sum(1<<i for i in G)
        Wall=[];Uall=[]
        for c in w.S:
            if not (w.S[a]<w.S[c]<w.S[z]): continue
            W=sub_in(inp[c]+arr[c],mA) if (inp[c] or arr[c]) else []
            U=sub_in(dep[c],mZ) if dep[c] else []
            if W and U:
                r1+=1
                if any(bin(x&y).count('1')&1 for x in W for y in U): r1hit+=1
            Wall+=sub_in(inp[c]+arr[c],mG) if (inp[c] or arr[c]) else []
            Uall+=sub_in(dep[c],mG) if dep[c] else []
        for x in Wall:
            for y in Uall:
                cross+=1; crosshit+=bin(x&y).count('1')&1
    print(p,'R1 (class,chart) with both spaces',r1,'nonzero pairing',r1hit,'| R2 cross-chart pairs',cross,'nonzero',crosshit)
