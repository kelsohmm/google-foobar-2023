def _count_trailing_0s(num):
    # this could be done faster using bits directly
    for idx, digit in enumerate(bin(num).lstrip('0b')[::-1]):
        if digit != '0':
            return idx


def solution(num):
    num = int(num)

    steps = 0
    while num != 1:
        steps += 1

        # all even numbers - divide - the distance to hypothetical closest best solution will also half
        if num % 2 == 0:
            num = num // 2
        # edge case - for 3, always better to go down
        elif num == 3:
            num = num - 1
        # core of the algorithm: check how many trailing 0s do binary formats of surrounding even numbers have
        # each zero at the end means the number can be divided by 2 one time - more is better
        elif _count_trailing_0s(num-1) > _count_trailing_0s(num+1):
            num = num - 1
        else:
            num = num + 1

    return steps
