#include "stdbool.h"
//#include "../src/checker.h"

int linear_search_opt(int *val, int *arr, int arr_size){
    int idx = -1; 
    int target = *val;
    bool find;
    for (int i = 0; i < arr_size; i++) {
        find = revealOblivBool(target == arr[i], 0);
        if (find){
            idx = i;
            break;
        }
    }
    return idx;
}

int main(){
    int arr_size = 50;
    int arr[arr_size];
    int val;
    checker_init(1);
    checker_make_symbolic(&arr, sizeof(arr), "arr");
    checker_make_symbolic(&val, sizeof(val), "val");

    int idx = linear_search_opt(&val, arr, arr_size);
    checker_check_int(idx);
    return 0;
}