from random import sample
from time import process_time
from mpyc.runtime import mpc    # load MPyC
secint = mpc.SecInt()           # 32-bit secure MPyC integers

 
def linear_search(val, arr, size):
    mpc.run(mpc.start())
    idx = -1
    shared_arr = mpc.input(arr, senders=[0])[0]
    shared_val = mpc.input(val, senders=[1])[0]
    for i in range(size): 
        find = shared_val == shared_arr[i]
        idx = mpc.if_else(find, i, idx)
    oidx = mpc.run(mpc.output(idx))
    mpc.run(mpc.shutdown())
    return oidx

def linear_search_opt(val, arr, size):
    mpc.run(mpc.start())
    idx = -1
    shared_arr = mpc.input(arr, senders=[0])[0]
    shared_val = mpc.input(val, senders=[1])[0]
    for i in range(size): 
        eq = mpc.run(mpc.eq_public(shared_val, shared_arr[i]))
        if eq:
            idx = i 
            break 
    mpc.run(mpc.shutdown())
    return idx

def bench(isopt = False, arraySize=10, searchSize = 1, samples=1):
    import random
    import time
    MIN = 0
    MAX = 2*arraySize

    totalTime = 0
    print("start benchmark binary search %s, %d times repeat:" % ("opt" if isopt else "", samples))
    for kk in range(samples):
        # Each party generates a random list in local, suppose party 0 gets list A and party 1 gets list B
        # Each time, party 0 selects a integer e in list A, while party 1 has list B 
        # Search e in B
        cleartext = random.sample(range(MIN, MAX), arraySize)
        eles = [cleartext[random.randint(0, arraySize-1)] for _ in range(searchSize)]
        x = list(map(secint, cleartext))
        timeSample = 0
        for jj in range(searchSize):
            e = secint(eles[jj])
            if isopt:
                timeS = time.perf_counter()
                oy = linear_search_opt(e, x, arraySize)
                timeE = time.perf_counter()
            else:
                timeS = time.perf_counter()
                oy = linear_search(e, x, arraySize)
                timeE = time.perf_counter()

            timeDiff = timeE-timeS 
            timeSample += timeDiff
            totalTime += timeDiff
        print("Sample %d cost %.3f" % (kk, timeSample))
    print("Total repeat %d times. Average execution time is %.3fs." % (samples, totalTime/samples))
    
    # f = open("Party.csv", "a+")
    # f.write("%s, %d, Time/s, %.3f,%d\n" % ("linear_search_opt" if isopt else "linear_search", arraySize,totalTime/samples, samples))
    # f.close()

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--opt', action='store_true')
    parser.add_argument('-e', type=int)
    parser.add_argument('-s', type=int)
    parser.add_argument('-i', type=int)

    args = parser.parse_args()

    bench(args.opt, args.e, args.s, args.i )
main()
