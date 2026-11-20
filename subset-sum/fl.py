import numpy as np, json
def H2(x): return -(x*np.log2(x)+(1-x)*np.log2(1-x))
def uv(rc, sc, kap, N=16384, J=16):
    x = 2*np.pi*np.arange(N)/N
    j = np.arange(1,J+1)[:,None]
    rc=np.asarray(rc,float); sc=np.asarray(sc,float)
    r = rc[:J]@np.cos(j*x) + rc[J:]@np.sin(j*x)
    s = sc[:J]@np.cos(j*x) + sc[J:]@np.sin(j*x)
    F=2**r; G=2**s
    Zf=F.mean(); Zg=G.mean(); LZ=np.log2(Zf*Zg)
    H=np.log2((2**(kap*r)).mean())+np.log2((2**(kap*s)).mean())-kap*LZ
    # P(x)=mean_w F(x+w)G(w): correlation
    fF=np.fft.fft(F); fG=np.fft.fft(G)
    P=np.real(np.fft.ifft(fF*np.conj(fG)))/N
    Y=np.real(np.fft.ifft(np.fft.fft(F*r)*np.conj(fG)) + np.fft.ifft(fF*np.conj(np.fft.fft(G*s))))/N
    L=np.log2(P)-LZ; B=Y/P-LZ
    u=L+(kap-1)*B-H; v=(2-kap)*B-2*L+H
    return x,u,v
def moments(x,u,v,p1,p2,D,aG):
    lam=2+2*np.cos(x)
    m1=np.log2(np.mean(lam*2**(p1*(D-u))))
    m2=np.log2(np.mean(lam*2**(p2*(aG*v-u))))
    return m1,m2
if __name__=='__main__':
    c=json.load(open('/home/claude/jv1000/subset-sum/selfcontained-2026/certificates/candidate_base.json'))
    x,u,v=uv([float(t) for t in c['rc']],[float(t) for t in c['sc']],float(c['kappa']))
    t,e=float(c['tau0']),float(c['eta']); D=e-t; G=2*t-e
    print(moments(x,u,v,float(c['p']),float(c['q_m']),D,D/G))
