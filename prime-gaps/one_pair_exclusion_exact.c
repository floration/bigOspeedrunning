// Exhaustive: does an admissible k-tuple of diameter exactly d exist (containing 0 and d)?
#include <stdio.h>
#include <stdlib.h>
typedef unsigned __int128 u128;
int K,D,n; int primes[]={3,5,7,11,13,17,19,23,29,31,37,41,43,47}; int np;
u128 cls[16][50]; // cls[i][r]: bitmask of evens 2j with 2j%p==r
long long nodes=0; u128 found;
static int pc(u128 x){return __builtin_popcountll((unsigned long long)x)+__builtin_popcountll((unsigned long long)(x>>64));}
int dfs(int i,u128 S){
  nodes++;
  if(pc(S)<K) return 0;
  if(i==np){found=S;return 1;}
  // bound: each remaining prime removes at least its min class count
  int p=primes[i];
  for(int r=0;r<p;r++){ if(r==0||r==D%p) continue;
    u128 T=S&~cls[i][r]; if(pc(T)<K) continue;
    if(dfs(i+1,T)) return 1;}
  return 0;}
int main(int c,char**v){K=atoi(v[1]);D=atoi(v[2]);n=D/2+1;
  np=0; while(np<14 && primes[np]<=K) np++; // need primes <=K
  for(int i=0;i<np;i++){int p=primes[i];for(int r=0;r<p;r++){cls[i][r]=0;for(int j=0;j<n;j++) if((2*j)%p==r) cls[i][r]|=((u128)1)<<j;}}
  u128 S=0; int G=atoi(v[3]); for(int j=0;j<n;j++){int x=2*j; if(x==0||x==D||(x>=D-G && x<=G)) S|=((u128)1)<<j;}
  int ok=dfs(0,S);
  printf("k=%d d=%d %s nodes=%lld\n",K,D,ok?"FOUND":"none",nodes);
  if(ok){int cnt=0;for(int j=0;j<n;j++) if((found>>j)&1){printf("%d ",2*j);cnt++;} printf("\n(%d survivors)\n",cnt);}
}
