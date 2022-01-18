#include "stdbool.h"
#include "stdint.h"
#include "stddef.h"
#include "math.h"
//#include "../src/checker.h"


int binary_search(int *haystack, int *needle, int size) {
    // upper bound = logN + 1;
    int upper_bound = log2(size) + 1;

    int index = -1;
    int iimin = 0;
    int iimax = size - 1;
    int iimid;

    int cur;
    int target = *needle;

    bool lt;
    bool eq;

    for (int ii = 0; ii < upper_bound; ii++) {
        iimid = (iimin + iimax) / 2;
        cur = haystack[iimid];
        eq = revealOblivBool(cur == target, 0);
        if (eq) {
            index = iimid;
            break;
        }else{
            lt = cur < target;
            if (lt) {
                iimin = iimid + 1;
            }else {
                iimax = iimid;
            }
        }
    }
    return index;
}

int main(){
    int arr_size = 100;
    int arr[arr_size];
    int val;

    checker_init(1);
    checker_make_symbolic(&arr, sizeof(arr), "arr");
    checker_make_symbolic(&val, sizeof(val), "val");

    for (int i = 1; i < arr_size; i++) {
        checker_assume(arr[i-1] < arr[i]);
    }
    int idx = binary_search(arr, &val, arr_size);
    checker_check_int(idx);
    return 0;
}