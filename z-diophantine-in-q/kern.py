import json,sys
q=json.load(open(sys.argv[1]+'/quadrics.json'))
n=q['variables']; P=(1<<61)-1
R=[]
for r in q['residuals']:
    f={}
    for t in r['terms']:
        m=tuple(sorted(t['monomial'])); f[m]=f.get(m,0)+int(t['coefficient'])
    R.append(f)
# rows: for each residual, A_i d =0 (n rows) ; also b_i.d=0 optionally
def rows(include_lin):
    out=[]
    for f in R:
        A={}
        for m,c in f.items():
            if len(m)==2:
                a,b=m[0]-1,m[1]-1
                if a==b: A.setdefault(a,{})[a]=(A.get(a,{}).get(a,0)+2*c)
                else:
                    A.setdefault(a,{})[b]=A.get(a,{}).get(b,0)+c
                    A.setdefault(b,{})[a]=A.get(b,{}).get(a,0)+c
        for a,row in A.items(): out.append(row)
        if include_lin:
            out.append({m[0]-1:c for m,c in f.items() if len(m)==1})
    out.append({0:1})  # d1=0
    return out
def rank(rs):
    piv={}
    for r in rs:
        r={k:v%P for k,v in r.items() if v%P}
        while r:
            k=min(r)
            if k in piv:
                pr=piv[k]; c=r[k]
                for kk,vv in pr.items(): r[kk]=(r.get(kk,0)-c*vv)%P
                r={a:b for a,b in r.items() if b}
            else:
                inv=pow(r[k],P-2,P); r={a:b*inv%P for a,b in r.items()}; piv[k]=r; break
    return len(piv)
print('n',n,'nullity (quadratic only, d1=0):',n-rank(rows(False)),' nullity incl linear:',n-rank(rows(True)))
