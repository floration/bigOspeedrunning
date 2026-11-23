// For admissible k-tuples in [0,D] (0 and D included), with gap target G:
// minimize the number of pairs at distance > G. Exhaustive over residue choices for primes <= k.
#include <stdio.h>
#include <stdlib.h>
typedef unsigned __int128 u128;
int K,D,G,n; int primes[]={3,5,7,11,13,17,19,23,29,31,37,41,43,47}; int np;
u128 cls[16][64]; long long leaves=0; int best=1<<30; int bestT[128],bestn;
static int pc(u128 x){return __builtin_popcountll((unsigned long long)x)+__builtin_popcountll((unsigned long long)(x>>64));}
void evalS(u128 S){
  int el[128],m=0; for(int j=0;j<n;j++) if((S>>j)&1) el[m++]=2*j;
  // must include 0 and D (they are forced in S); choose K elements including 0 and D
  // middle: [D-G, G]; left zone (0..D-G) exclusive; right zone (G..D]
  int L[128],nl=0,M[128],nm=0,R[128],nr=0;
  for(int i=0;i<m;i++){int x=el[i]; if(x==0||x==D) continue; if(x<D-G) L[nl++]=x; else if(x>G) R[nr++]=x; else M[nm++]=x;}
  int need=K-2; // besides 0 and D
  // take all middle if possible; else any K-2 of middle -> 1 bad pair (0,D) only... 
  for(int useM=(nm<need?nm:need); useM>=0 && useM>=nm-0-1000; useM--){
    int rest=need-useM; if(rest<0) continue;
    for(int a=0;a<=rest;a++){int b=rest-a; if(a>nl||b>nr) continue;
      // chosen: 0, D, middle(any useM: they create no bad pairs beyond with 0/D? check), L top a, R bottom b
      int T[128],t=0; T[t++]=0; for(int i=nl-a;i<nl;i++) T[t++]=L[i]; for(int i=0;i<useM;i++) T[t++]=M[i]; for(int i=0;i<b;i++) T[t++]=R[i]; T[t++]=D;
      int bad=0; for(int i=0;i<t;i++) for(int j=i+1;j<t;j++) if(T[j]-T[i]>G) bad++;
      if(bad<best){best=bad; bestn=t; for(int i=0;i<t;i++) bestT[i]=T[i];}
    }
    break; // using max middle is always best (middle elements: pairs with 0 or D? x in [D-G,G] => x-0<=G, D-x<=G)
  }
}
void dfs(int i,u128 S){
  if(pc(S)<K) return;
  if(i==np){leaves++; evalS(S); return;}
  int p=primes[i];
  for(int r=0;r<p;r++){ if(r==0||r==D%p) continue; dfs(i+1,S&~cls[i][r]); }
}
int main(int c,char**v){K=atoi(v[1]);D=atoi(v[2]);G=atoi(v[3]);n=D/2+1;
  np=0; while(np<14 && primes[np]<=K) np++;
  for(int i=0;i<np;i++){int p=primes[i];for(int r=0;r<p;r++){cls[i][r]=0;for(int j=0;j<n;j++) if((2*j)%p==r) cls[i][r]|=((u128)1)<<j;}}
  u128 S=0; for(int j=0;j<n;j++) S|=((u128)1)<<j;
  dfs(0,S);
  if(best==(1<<30)){printf("k=%d D=%d G=%d none\n",K,D,G);return 0;}
  printf("k=%d D=%d G=%d minbad=%d leaves=%lld tuple:",K,D,G,best,leaves); for(int i=0;i<bestn;i++) printf(" %d",bestT[i]); printf("\n");
}
