
def _solution_rec(number, digits_left):
    highest_number = number
    for idx in range(len(digits_left)):
        next_digits = digits_left[:idx] + digits_left[idx + 1:]
        new_number = _solution_rec((number * 10) + digits_left[idx], next_digits)
        if new_number % 3 == 0 and new_number > highest_number:
            highest_number = new_number

    return highest_number


def solution(l):
    # number is dividable by 3 if the sum of its digits is dividable by 3
    # this means that 3, 6, 9 and 0 digits will not affect divisability, but 3, 6 & 9 can be at the beginning or end
    # so lets only filter out 0s as they only make sense at the end
    l_nonzeros = sorted(l, reverse=True)
    l_nonzeros = list(filter(lambda x: x != 0, l_nonzeros))

    return _solution_rec(0, digits_left=l_nonzeros) * (10 ** (len(l) - len(l_nonzeros)))
