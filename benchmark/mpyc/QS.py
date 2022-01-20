from random import randrange
from mpyc.runtime import mpc    # load MPyC
from mpyc.seclists import seclist, secindex
secint = mpc.SecInt()           # 32-bit secure MPyC integers
import math 

# def oddeven_merge(lo, hi, r):
#     step = r * 2
#     if step < hi - lo:
#         yield from oddeven_merge(lo, hi, step)
#         yield from oddeven_merge(lo + r, hi, step)
#         yield from [(i, i + r) for i in range(lo + r, hi - r, step)]
#     else:
#         yield (lo, lo + r)

# def oddeven_merge_sort_range(lo, hi):
#     """ sort the part of x with indices between lo and hi.

#     Note: endpoints (lo and hi) are included.
#     """
#     if (hi - lo) >= 1:
#         # if there is more than one element, split the input
#         # down the middle and first sort the first and second
#         # half, followed by merging them.
#         mid = lo + ((hi - lo) // 2)
#         yield from oddeven_merge_sort_range(lo, mid)
#         yield from oddeven_merge_sort_range(mid + 1, hi)
#         yield from oddeven_merge(lo, hi, 1)

# def oddeven_merge_sort(length):
#     """ "length" is the length of the list to be sorted.
#     Returns a list of pairs of indices starting with 0 """
#     yield from oddeven_merge_sort_range(0, length - 1)


# def compare_and_swap(x, a, b):
#     c = x[a] > x[b]                  # secure comparison, secint c represents a secret-shared bit
#     d = c * (x[b] - x[a])            # secure subtraction
#     x[a], x[b] = x[a] + d, x[b] - d  # secure swap: x[a], x[b] swapped if only if c=1

# def batcher_sort(arr1, arr2):
#     mpc.run(mpc.start())
#     shared_arr1 = mpc.input(arr1, senders=[0])[0]
#     shared_arr2 = mpc.input(arr2, senders=[1])[0]
#     shared_arr = shared_arr1 + shared_arr2
#     n = len(shared_arr)
#     extend = 2 ** math.ceil(math.log2(n))
#     extend = extend - n 
#     for i in range(extend):
#         shared_arr.append(secint(0))
#     for i in oddeven_merge_sort(len(shared_arr)):
#         compare_and_swap(shared_arr, *i)
#     x = shared_arr[extend:]
#     mpc.run(mpc.shutdown())

def partition(arr, output, low, high):
    i = low         # index of smaller element
    pivot = arr[high]     # pivot
    for j in range(low, high):
        oleq = arr[j] <= pivot
        leq = mpc.run(mpc.eq_public(oleq, 1))
        if leq:
            arr[i], arr[j] = arr[j], arr[i]
            output[i], output[j] = output[j], output[i]
            i = i+1
  
    arr[i], arr[high] = arr[high], arr[i]
    output[i], output[high] = output[high], output[i]
    return i
  
  
# Function to do Quick sort
def quickSort(arr, output, low, high):
    if len(arr) == 1:
        return arr
    if low < high:
        pi = partition(arr, output, low, high)
        quickSort(arr, output, low, pi-1)
        quickSort(arr, output, pi+1, high)

def quick_sort(arr1, arr2):
    mpc.run(mpc.start())
    shared_arr1 = mpc.input(arr1, senders=[0])[0]
    shared_arr2 = mpc.input(arr2, senders=[1])[0]
    shared_arr = shared_arr1 + shared_arr2
    output = [x for x in range(len(shared_arr))]
    quickSort(shared_arr, output, 0, len(shared_arr)-1)
    mpc.run(mpc.shutdown())
    return output

def partition_std(arr, output, low, high):
    i = low         # index of smaller element
    pivot = arr[high-1]     # pivot
    for ii in range(len(arr)):
        in_range =  mpc.and_((ii >= low), (ii < high)) 
        oleq = mpc.if_else(in_range, arr[ii] <= pivot, False)
        temp = mpc.if_else(oleq, arr[ii], arr[i])
        arr[ii] = mpc.if_else(oleq, arr[i], arr[ii])
        arr[i] = temp 
        temp = mpc.if_else(oleq, output[ii], output[i])
        output[ii] = mpc.if_else(oleq, output[i], output[ii])
        output[i] = temp 
        i = mpc.if_else(oleq, i+1, i)
  
    arr[i], arr[high-1] = arr[high-1], arr[i]
    return i
  
def quickSort_std(arr, output, low, high):
    if len(arr) == 1:
        return arr
    ogt = (high - low) > 1
    gt = mpc.run(mpc.eq_public(1,ogt))
    if gt:
        pi = partition_std(arr, output, low, high)
        quickSort_std(arr, output, low, pi-1)
        quickSort_std(arr, output, pi+1, high)

def quick_sort_std(arr1, arr2):
    mpc.run(mpc.start())
    shared_arr1 = mpc.input(arr1, senders=[0])[0]
    shared_arr2 = mpc.input(arr2, senders=[1])[0]
    shared_arr =  seclist(shared_arr1 + shared_arr2)
    output = seclist([secint(x) for x in range(len(shared_arr))])

    quickSort_std(shared_arr, output, secint(0), secint(len(shared_arr)))

    ret = [mpc.run(mpc.output(x)) for x in output]
    mpc.run(mpc.shutdown())
    return ret

def bench(isopt = False, arraySize=10,  samples=1):
    import random
    import time
    MIN = 0
    MAX = 2*arraySize

    totalTime = 0
    print("start benchmark %s, %d times repeat:" % ("quick_sort" if isopt else "batcher_sort", samples))
    for kk in range(samples):
        cleartext1 = random.sample(range(MIN, MAX), int(arraySize/2))
        cleartext2 = random.sample(range(MIN, MAX), arraySize - int(arraySize/2))
        x1 = list(map(secint, cleartext1))
        x2 = list(map(secint, cleartext2))

        if isopt:
            timeS = time.perf_counter()
            out = quick_sort(x1, x2)
            timeE = time.perf_counter()
        else:
            timeS = time.perf_counter()
            out = quick_sort_std(x1, x2)
            timeE = time.perf_counter()
        timeDiff = timeE-timeS 
        totalTime += timeDiff
        print("Sample %d cost %.3f" % (kk, timeDiff))
    print("Total repeat %d times. Average execution time is %.3fs." % (samples, totalTime/samples))

    # f = open("Party.csv", "a+")
    # f.write("%s, %d, Time/s, %.3f,%d\n" 
    # % ("quick_sort" if isopt else "batcher_sort", arraySize, totalTime/samples, samples))
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
