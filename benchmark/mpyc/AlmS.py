from mpyc.runtime import mpc    # load MPyC
from mpyc.seclists import seclist, secindex
secint = mpc.SecInt()           # 32-bit secure MPyC integers
import math  
import random
import time

def gen_sorted_array(n):
    l = []
    v = 0
    for i in range(n):
        v = v + random.randrange(0,3)
        l.append(v)

    return l 

def binary_almost_search(haystack, haystack_length, needle):
    mpc.run(mpc.start())

    shared_haystack = seclist(mpc.input(haystack, senders=[0])[0])
    shared_needle = mpc.input(needle, senders=[1])[0]

    upper_bound = int(math.log2(haystack_length)) + 1
    index = secint(-1)
    iimin = secint(0)
    iimax = secint(haystack_length - 1)
    bb = shared_needle
    for _ in range(upper_bound):
        ii = iimin + iimax
        cc =  ii % 2
        iimid = mpc.if_else( cc, mpc.div(iimax+iimin-1, 2), mpc.div(iimax+iimin, 2) )
        aa = shared_haystack[iimid] # oram_read(haystack, haystack_length, iimid)
        oeq = aa == bb 
        index = mpc.if_else(oeq, iimid, index)

        hasleft = iimid > iimin
        left = mpc.if_else(hasleft,shared_haystack[iimid-1], -1) 
        index = mpc.if_else(aa==left, iimid-1, index)

        hasright = iimid < iimax 
        right = mpc.if_else(hasright,shared_haystack[iimid+1], -1)
        index = mpc.if_else(aa==right, iimid+1, index)

        ogt = aa > bb
        iimin = mpc.if_else(ogt, iimin, iimid+2)
        iimax = mpc.if_else(ogt, iimid-2, iimax)
    oindex = mpc.run(mpc.output(index))
    mpc.run(mpc.shutdown())
    return oindex

def binary_almost_search_opt(haystack, haystack_length, needle):
    mpc.run(mpc.start())
    shared_haystack = seclist(mpc.input(haystack, senders=[0])[0])
    shared_needle = mpc.input(needle, senders=[1])[0]
    
    upper_bound = int(math.log2(haystack_length)) + 1
    index = secint(-1)
    iimin = secint(0)
    iimax = secint(haystack_length - 1)
    bb = shared_needle
    for _ in range(upper_bound):
        ii = iimin + iimax
        cc =  ii % 2
        iimid = mpc.if_else( cc, mpc.div(iimax+iimin-1, 2), mpc.div(iimax+iimin, 2) )
        aa = shared_haystack[iimid] 
        eq = aa == bb 
        index = mpc.if_else(eq, iimid, index)

        hasleft = mpc.run(mpc.output(iimid > iimin)) 
        left = shared_haystack[iimid-1] if hasleft else -1
        index = mpc.if_else(aa==left, iimid-1, index)

        hasright = mpc.run(mpc.output(iimid < iimax))
        right = shared_haystack[iimid+1] if hasright else -1
        index = mpc.if_else(aa==right, iimid+1, index)

        ogt = aa > bb
        iimin = mpc.if_else(ogt, iimin, iimid+2)
        iimax = mpc.if_else(ogt, iimid-2, iimax)
    oindex = mpc.run(mpc.output(index))
    mpc.run(mpc.shutdown())
    return oindex


def bench(isopt = False, arraySize=10, searchSize = 1, samples=1):

    totalTime = 0
    print("start benchmark almost search %s, %d times repeat:" % ("opt" if isopt else "", samples))
    for kk in range(samples):
        # Each party generates a random list in local, suppose party 0 gets list A and party 1 gets list B
        # Each time, party 0 selects a integer e in list A, while party 1 has list B 
        # Search e in B
        cleartext = gen_sorted_array(arraySize)
        eles = [cleartext[random.randint(0,arraySize-1)] for _ in range(searchSize)]
        x = list(map(secint, cleartext))
        for jj in range(searchSize):
            e = secint(eles[jj])
            if isopt:
                timeS = time.perf_counter()
                oy = binary_almost_search_opt(x, arraySize, e)
                timeE = time.perf_counter()
            else:
                timeS = time.perf_counter()
                oy = binary_almost_search(x, arraySize, e)
                timeE = time.perf_counter()
            timeDiff = timeE-timeS 
            totalTime += timeDiff
        print("Sample %d cost %.3f" % (kk, timeDiff))
    print("Total repeat %d times. Average execution time is %.3fs." % (samples, totalTime/samples))

    # f = open("Party.csv", "a+")
    # f.write("%s, %d, Time/s, %.3f,%d\n" 
    # % ("almost_search_opt" if isopt else "almost_search", arraySize, totalTime/samples, samples))
    # f.close()

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--opt', action='store_true')
    parser.add_argument('-e', type=int)
    parser.add_argument('-s', type=int)
    parser.add_argument('-i', type=int)

    args = parser.parse_args()

    bench(args.opt, args.e, args.s, args.i)
main()


        
