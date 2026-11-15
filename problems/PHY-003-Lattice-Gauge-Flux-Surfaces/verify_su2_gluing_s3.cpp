// Independently exhausts the 2D irrep of S3 on cube and pair surfaces.
// Tree gauge fixing leaves 5 free links (cube) or 9 free links (pairs).
// Since the gluing theorem is group independent, this finite non-Abelian
// group is a clean cross-check of the 1/16 and 1/256 character integrals.
// Compile: g++ -O2 -std=c++17 verify_su2_gluing_s3.cpp -o /tmp/check && /tmp/check
#include <cstdio>
#include <cstdlib>
using namespace std;
static const int T[6][6]={{0,1,2,3,4,5},{1,0,4,5,2,3},{2,3,0,1,5,4},{3,2,5,4,0,1},{4,5,1,0,3,2},{5,4,3,2,1,0}};
static const int inv[6]={0,1,2,4,3,5};
static const int chi[6]={2,0,0,-1,-1,0}; // standard irrep character = fixed points - 1
struct E {int idx,sgn;};
static const E cube[6][4]={
{{-1,1},{1,1},{-1,-1},{-1,-1}},
{{-1,1},{2,1},{-1,-1},{-1,-1}},
{{-1,1},{0,1},{-1,-1},{-1,-1}},
{{-1,1},{3,1},{-1,-1},{-1,-1}},
{{-1,1},{4,1},{-1,-1},{0,-1}},
{{1,1},{4,1},{3,-1},{2,-1}}};
static const E same[10][4]={
{{-1,1},{2,1},{-1,-1},{-1,-1}},
{{-1,1},{3,1},{-1,-1},{-1,-1}},
{{-1,1},{0,1},{-1,-1},{-1,-1}},
{{-1,1},{5,1},{-1,-1},{-1,-1}},
{{-1,1},{1,1},{-1,-1},{-1,-1}},
{{-1,1},{6,1},{-1,-1},{-1,-1}},
{{-1,1},{7,1},{-1,-1},{0,-1}},
{{-1,1},{8,1},{-1,-1},{1,-1}},
{{2,1},{7,1},{4,-1},{3,-1}},
{{4,1},{8,1},{6,-1},{5,-1}}};
static const E mixed[10][4]={
{{-1,1},{3,1},{-1,-1},{-1,-1}},
{{-1,1},{4,1},{-1,-1},{-1,-1}},
{{-1,1},{0,1},{-1,-1},{-1,-1}},
{{-1,1},{1,1},{-1,-1},{-1,-1}},
{{-1,1},{5,1},{-1,-1},{-1,-1}},
{{-1,1},{6,1},{-1,-1},{-1,-1}},
{{-1,1},{7,1},{-1,-1},{0,-1}},
{{-1,1},{8,1},{-1,-1},{1,-1}},
{{2,1},{7,1},{6,-1},{3,-1}},
{{2,1},{8,1},{5,-1},{4,-1}}};
long long sum(const E (*f)[4], int nf, int n) {
 long long count=1,total=0;
 for(int i=0;i<n;i++)count*=6;
 int g[9];
 for(long long z=0;z<count;z++){
  long long x=z;
  for(int j=0;j<n;j++){g[j]=x%6;x/=6;}
  long long val=1;
  for(int p=0;p<nf;p++){
   int h=0;
   for(int k=0;k<4;k++){
    int a=f[p][k].idx<0?0:g[f[p][k].idx];
    if(f[p][k].sgn<0)a=inv[a];
    h=T[h][a];
   }
   val*=chi[h];
   if(val==0)break;
  }
  total+=val;
 }
 return total;
}
int main() {
 const long long c=sum(cube,6,5),a=sum(same,10,9),b=sum(mixed,10,9);
 printf("SU2 Haar-gluing group-independent test via S3 standard irrep:\n");
 printf("cube: %lld / 7776 = 1/16\n",c);
 printf("same: %lld / 10077696 = 1/256\n",a);
 printf("mixed: %lld / 10077696 = 1/256\n",b);
 if(c!=486 || a!=39366 || b!=39366)return 1;
 puts("PASS: all three exact non-Abelian group-integral cross-checks");
 return 0;
}
