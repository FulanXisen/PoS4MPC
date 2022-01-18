#include "stdbool.h"
#include "stdint.h"
#include "stddef.h"
#include "math.h"
//#include "../src/checker.h"

int binary_almost_search(int *haystack, int* needle, int size){
    //int upper_bound = Log2N + 1;
    int upper_bound = log2(size) + 1;

    int index = -1;
    int iimin = 0;
    int iimax = size - 1;
    int iimid;

    int cur; 
    int tleft; 
    int tright;
    int target = *needle;
    
    bool hasleft; 
    bool hasright; 
    bool eq; 
    bool gt;

    for (int ii = 0; ii < upper_bound; ii++) {
        iimid = (iimin + iimax) / 2;

        cur = haystack[iimid];
        eq = cur == target;
        if (eq) {
            index = iimid;
        }

        hasleft = revealOblivBool(iimid > iimin, 0);
        if ( hasleft ) {
            tleft = haystack[iimid-1];
            if ( tleft == target ){
                index = (iimid-1);
            }
        }

        hasright = revealOblivBool(iimid < iimax, 1);
        if (hasright) {
            tright = haystack[iimid+1];
            if ( tright == target ){
                index = (iimid + 1);
            }
        }
        
        gt = cur > target;
        if (gt) {
            iimax = iimid-2;
        }else {
            iimin = iimid+2;
        }
        
    }
    return index;
}

void binary_almost_search_main(int *idx, int *needle, int* arr, int n){
    *idx = binary_almost_search(arr, needle, n);
}

int main(){
    int arr_size = 100;
    int arr[arr_size];
    int val;
    int idx = -1;
    checker_init(2);
    checker_make_symbolic(&arr, sizeof(arr), "arr");
    checker_make_symbolic(&val, sizeof(val), "val");

    for(int i = 0; i < arr_size; i++){
        bool c1 = true;
        for(int j = 0; j < arr_size; j++){
            if (j < i-1){
                c1 = c1 & (arr[j]<arr[i]);
            }else if ( j > i + 1){
                c1 = c1 & (arr[j]>arr[i]);
            }
        }
        checker_assume(c1);
    }

    binary_almost_search_main(&idx, &val, arr, arr_size);
    checker_check_int(idx);
}