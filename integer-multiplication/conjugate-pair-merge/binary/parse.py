# Parse the binary K7 register program into a GF(2) scalar DAG (transfers + outputs + clear-zero rows).
import json,gzip,sys,collections
def parse(path):
    w=json.load(gzip.open(path)); n=w['public']; prog=w['program']
    reg={}  # reg -> [frame, labelset(int)]
    for i in range(n): reg[i]=[w['start'][i],1<<i]
    lab_frame={i:w['start'][i] for i in range(n)}
    moves=[]; forms={}; nl=n; clears=[]
    for op in prog:
        o=op[0]
        if o=='INIT': r,f=op[1],op[2]; assert r not in reg; reg[r]=[f,0]
        elif o=='ADD':
            d,s,f=op[1],op[2],op[3]; assert reg[d][0]==f==reg[s][0],op; reg[d][1]^=reg[s][1]
        elif o=='MOVE':
            r,a,b=op[1],op[2],op[3]; assert reg[r][0]==a
            t=nl; nl+=1; forms[t]=reg[r][1]; moves.append((t,a,b,r)); lab_frame[t]=b; reg[r]=[b,1<<t]
        elif o=='SWAP':
            a,b=op[1],op[2]; reg[a],reg[b]=reg[b],reg[a]
        elif o=='CLEAR':
            r,f=op[1],op[2]; assert reg[r][0]==f; clears.append((r,f,reg[r][1])); del reg[r]
        else: raise ValueError(o)
    outs=[reg[i] for i in range(n)]
    assert all(outs[i][0]==w['final'][i] for i in range(n))
    return w,n,moves,forms,outs,clears,lab_frame,nl
def evaluate(n,forms,order,outs_sets,clears_sets):
    val={i:1<<i for i in range(n)}
    def ev(s):
        v=0; t=s
        while t:
            l=(t&-t).bit_length()-1; v^=val[l]; t&=t-1
        return v
    for t in order: val[t]=ev(forms[t])
    return [ev(s) for s in outs_sets],[ev(s) for s in clears_sets],val
if __name__=='__main__':
    w,n,moves,forms,outs,clears,lf,nl=parse(sys.argv[1])
    order=[m[0] for m in moves]
    O,Cz,val=evaluate(n,forms,order,[o[1] for o in outs],[c[2] for c in clears])
    print('public',n,'moves',len(moves),'clears',len(clears),'nonzero clears',sum(1 for v in Cz if v))
    # map check: outputs as GF(2) rows
    ident=sum(1 for i in range(n) if O[i]==1<<i); print('identity outputs',ident,'others',n-ident)
    fr=w['frames']; dim={int(k):v['dim'] for k,v in fr.items()}
    hist=collections.Counter(abs(dim[b]-dim[a]) for t,a,b,r in moves); print('grade hist per call',sorted(hist.items()))
