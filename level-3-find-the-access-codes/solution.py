from collections import defaultdict


def solution(l):
    result = 0
    mem = defaultdict(lambda: 0)
    for i in range(len(l)):
        for j in range(i):
            if l[i] % l[j] == 0:
                mem[i] += 1
                result = result + mem[j]
    return result
