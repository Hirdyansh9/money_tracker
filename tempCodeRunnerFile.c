#include <stdio.h> 
#include <unistd.h>
int main(){
fork();
(fork() && fork()) || fork(); 
fork();
int i = 1;
printf("TIET \n");
return 0; 
}
// how many times tiet would be printed, make a fork tree diagram also