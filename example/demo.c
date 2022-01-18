#include "stdbool.h"
//#include "../src/checker.h"

char demo(int a, int b, int c){
    char r = 1;
    int max = a;
    bool c1 = max < b;
    if ( c1 ){
        r = 2;
        max = b;
    }
    bool c2 = revealOblivBool(max < c, 0);
    if ( c2 ){
        r = 3;
    }
    return r;
}

int main() {
    int a; int b; int c; int o;
    checker_init(1);
    checker_make_symbolic(a, sizeof(a), "a");
    checker_make_symbolic(b, sizeof(b), "b");
    checker_make_symbolic(c, sizeof(c), "c");

    o = max_three(a, b, c);
    checker_check_int(o);
    return 0;
}
