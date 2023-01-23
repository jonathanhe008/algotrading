import numpy
def lis(arr):
    n = len(arr)

    LWIS = [1] * n       # Initialize LWIS[0..n-1] for memoization

    for i in range(1, n):      # or should it be reversed(range(n))?
        for j in range(0, i):
            if arr[i] >= arr[j] and LWIS[i] < LWIS[j] + 1:
                LWIS[i] = LWIS[j] + 1


    answer = max(LWIS)
    return answer

if __name__ == "__main__":
    print(lis([10,22,9,33,21,50,41,60,80]))