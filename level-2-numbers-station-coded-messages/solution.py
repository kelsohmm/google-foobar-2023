
def solution(l, key):
    p1 = 0
    p2 = 0
    s = l[0] if len(l) else 0

    while p1 < len(l) and p2 < len(l):
        if s == key:
            return [p1, p2]
        elif s < key:
            p2 += 1
            if p2 < len(l):
                s += l[p2]
        else:
            p1 += 1
            p2 = p1
            s = l[p1]

    return [-1, -1]
