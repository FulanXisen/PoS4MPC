from mpyc.runtime import mpc    # load MPyC
secint = mpc.SecInt()           # 32-bit secure MPyC integers

def naive_psi(aarr, barr, size):
    mpc.run(mpc.start())
    shared_a = mpc.input(aarr, senders=[0])[0]
    shared_b = mpc.input(barr, senders=[1])[0]

    intersect = [secint(-1)]*size
    for i in range(size):
        for j in range(size):
            intersect[i] = mpc.if_else(shared_a[i]==shared_b[j], j, intersect[i])
    output = mpc.run(mpc.output(intersect))
    mpc.run(mpc.shutdown())
    return output

def naive_psi_opt(aarr, barr, size):
    mpc.run(mpc.start())
    shared_a = mpc.input(aarr, senders=[0])[0]
    shared_b = mpc.input(barr, senders=[1])[0]

    intersect = [-1]*size
    for i in range(size):
        for j in range(size):
            match = mpc.run(mpc.eq_public(shared_a[i], shared_b[j]))
            if match:
                intersect[i] = j
                break
    mpc.run(mpc.shutdown())
    return intersect

def bench(isopt = False, arraySize=10, samples=1):
    import random
    import time
    MIN = 0
    MAX = 2*arraySize

    totalTime = 0
    print("start benchmark naive_psi %s, %d times repeat:" % ("opt" if isopt else "", samples))
    for kk in range(samples):
        # Suppose party 0 get random set A, while party 1 get random set B
        # the probability Pr(unite(A,B) == A == B) = Pr(unite(A,B) == None)
        caarr = random.sample(range(MIN, MAX), arraySize)
        cbarr = random.sample(range(MIN, MAX), arraySize)

        saarr = list(map(secint, caarr))
        sbarr = list(map(secint, cbarr))

        if isopt:
            timeS = time.perf_counter()
            idx = naive_psi_opt(saarr, sbarr, arraySize)
            timeE = time.perf_counter()
        else:
            timeS = time.perf_counter()
            idx = naive_psi(saarr, sbarr, arraySize)
            timeE = time.perf_counter()
        timeDiff = timeE-timeS 
        totalTime += timeDiff
        print("Sample %d cost %.3f" % (kk, timeDiff))
    print("Total repeat %d times. Average execution time is %.3fs." % (samples, totalTime/samples))

    # f = open("Party.csv", "a+")
    # f.write("%s, %d, Time/s, %.3f,%d\n" 
    # % ("naive_psi_opt" if isopt else "naive_psi", arraySize, totalTime/samples, samples))
    # f.close()

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--opt', action='store_true')
    parser.add_argument('-n', type=int)
    parser.add_argument('-i', type=int)

    args = parser.parse_args()

    bench(args.opt, args.n, args.i)
main()