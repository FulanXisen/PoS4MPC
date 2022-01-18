#include "stdbool.h"
#include "stdint.h"
#include "stddef.h"
//#include "checker.h"

__always_inline void swap(int8_t* a, int8_t* b) {
  int8_t t = *a;
  *a = *b;
  *b = t;
}

__always_inline int8_t partition(int8_t * data, int8_t * output, int8_t n){
  int8_t i = 0;
  int8_t *pi = data + n - 1;
  bool leq ;
  for (int8_t j = 0; j < n-1; j++){
    leq = revealOblivBool(data[j] <= *pi, 0);
    if ( leq) {
      bool neq = revealOblivBool(i!=j, 1);
      if ( neq ) {
        swap(data+i, data+j);
        swap(output+i, output+j);
      }
      i = i + 1;
    }
  }
  bool nend = revealOblivBool(i != n-1, 2);
  if ( nend ) {
    swap(data+i, pi);
    swap(output+i, output + n - 1);
  }

  return i;
}

void qsort_main(int8_t * data, int8_t * output, int8_t len){
  if (1 < len) {
    // p is the index of pivot
    int8_t p = partition(data, output, len);
    // sort first p value
    qsort_main(data, output, p);
    // sort last n-p-1 value
    qsort_main(data+p+1, output+p+1, len-p-1);
  }
}


int8_t *qsort(int8_t * data, size_t end){
  int8_t *output = malloc(sizeof(int8_t) * end);
  for (int i = 0; i < end; i++){
    output[i] = i;
  }
  qsort_main(data, output, end);
  return output;
}


int main(){
    int size = 100;
    int8_t arr[size];
    int8_t pv;

    checker_init(3);
    checker_make_symbolic(arr, sizeof(arr), "arr");
    
    // pv = partition(arr, output, size);
    //checker_check_int(pv);
    int8_t *output = qsort(arr, size);
    checker_check_int8_array(output, size);
    
    free(output);
    return 0;
}