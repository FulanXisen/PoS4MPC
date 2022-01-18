//#include "../src/checker.h"
#include "stdbool.h"
#include "stdint.h"

__always_inline int inner_loop_opt(int8_t *val, int8_t *arr, int8_t size){
    bool find;
    int8_t idx = -1;
    int8_t target = *val;
    for (int8_t j = 0; j < size; j++) {
        find = revealOblivBool(target == arr[j], 0);
        if ( find ) {
            idx = j;
            break;
        }
    } 
    return idx;
}

int8_t * psi_opt(int8_t *aarr, int8_t *barr, int8_t size){
    int8_t *intersection = malloc(sizeof(int8_t) * size);
    for (int8_t i = 0; i < size; i++) {
        intersection[i] = inner_loop_opt(&aarr[i], barr, size);
    }
    return intersection;
}


int main(){
    int8_t size = 50;
    int8_t aarr[size];
    int8_t barr[size];

    checker_init(1);
    checker_make_symbolic(&aarr, sizeof(aarr), "aarr");
    checker_make_symbolic(&barr, sizeof(barr), "barr");

    int8_t * intersection = psi_opt(aarr, barr, size);
    checker_check_int8_array(intersection, size);

    free(intersection);
    return 0;
}