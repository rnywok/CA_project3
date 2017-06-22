#include <stdio.h>
#include <stdlib.h>

#define VECTOR_SIZE (512)

    
int a[VECTOR_SIZE], b[VECTOR_SIZE], c[VECTOR_SIZE];

void vec_mult(int n) {

    int i;

    for (i=0 ; i<n ; i++)
        c[i] = a[i] * b[i];
}

int main(void) {

    int i;

    for (i=0 ; i<VECTOR_SIZE ; i+=8)
        vec_mult(i);

    return 0;
}
