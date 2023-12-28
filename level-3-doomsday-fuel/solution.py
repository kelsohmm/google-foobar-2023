try:  # python >3.6
    from math import gcd as math_gcd
    from functools import reduce
except ImportError:  # python 2.7
    from fractions import gcd as math_gcd_onearg
    def math_gcd(*args):
        res = math_gcd_onearg(args[0], args[1])
        for arg in args[2:]:
            res = math_gcd_onearg(res, arg)
        return res

def math_lcm_onearg(a, b):
    return (a * b) // math_gcd(a, b)

def math_lcm(*args):  # python 2.7 doesnt have lcm function
    res = math_lcm_onearg(args[0], args[1])
    for arg in args[2:]:
        res = math_lcm_onearg(res, arg)
    return res

import numpy as np
from fractions import Fraction

def _convert_to_absorbing_markov_chain_standard_form(arr):  # returns new arr + num of terminal states
    """
    This function converts the markov chain transition probabilities array from exercise,
    to a proper "absorbing markov chain" standard form.
    It moves all the terminal states to the beginning, rearranges the columns so that they still point to the right rows
    and fills the probabilities 
    """
    terminal_idxs = {idx for idx in range(len(arr)) if sum(arr[idx]) == 0}
    curr_terminal_idx, curr_nonterminal_idx = 0, 0
    idxs_mapping = {}  # first - build mapping of original index to index in new array
    for idx in range(len(arr)):
        if idx in terminal_idxs:
            idxs_mapping[curr_terminal_idx] = idx
            curr_terminal_idx += 1
        else:
            idxs_mapping[curr_nonterminal_idx + len(terminal_idxs)] = idx
            curr_nonterminal_idx += 1

    result = np.array([
        [
            arr[idxs_mapping[x]][idxs_mapping[y]]
            for y in range(len(arr[0]))
        ]
        for x in range(len(arr))
    ], dtype=np.float64)  # 64 bit precision is required
    for idx in range(len(terminal_idxs)):  # fill probability of transition to itself for terminating states
        result[idx][idx] = 1
    
    # convert integers to probabilities
    result = result / result.sum(axis=-1, keepdims=True)
    
    return result, len(terminal_idxs)


def _convert_floats_to_integer_fractions(floats):
    """
    Takes an arrray of floats, convert them to rational fractions
    and bring to smallest common denominator
    """
    fractions = [Fraction(num).limit_denominator() for num in floats]

    lcm = math_lcm(*[f.denominator for f in fractions])
    numerators = [f.numerator * (lcm // f.denominator) for f in fractions]
    
    nums_with_denom = numerators + [lcm]
    gcd = math_gcd(*nums_with_denom)
    return [n // gcd for n in nums_with_denom]

def solution(arr):
    if sum(arr[0]) == 0:  # edge case - initial state is terminal state, return [1, 0s...., 1]
        terminal_idxs = {idx for idx in range(len(arr)) if sum(arr[idx]) == 0}
        return [1] + ([0] * (len(terminal_idxs)-1)) + [1]

    matrix, num_term = _convert_to_absorbing_markov_chain_standard_form(arr)
    
    # as described in https://github.com/ivanseed/google-foobar-help/blob/master/challenges/doomsday_fuel/doomsday_fuel.md
    Q = matrix[num_term:, num_term:]
    I = np.diag(np.ones(Q.shape[0]))
    F = np.linalg.inv(I - Q)
    R = matrix[num_term:, :num_term]
    FR = np.dot(F, R)

    return _convert_floats_to_integer_fractions(FR[0])
