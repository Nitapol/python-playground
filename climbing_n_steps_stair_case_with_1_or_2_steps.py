# You are climbing a stair case. It takes n steps to reach to the top.
#
# Each time you can either climb 1 or 2 steps. In how many distinct ways can
# you climb to the top?
#
# Example :
#   Input : 3
#   Steps : [1 1 1], [1 2], [2 1]
#   Return : 3
#
# Access Hint
# Think of DP.
# You need to come up with O(n) solution.
#
# Access Hint
# This is the most basic dynamic programming problem.
# We know that we can take 1 or 2 step at a time. So, to take n steps, we must
# have arrived at it immediately from n - 1 or n-2th step.
# If we knew the number of ways to reach n-1 and n-2th step, our answer would
# be the summation of their number of ways.
#
# class Solution {
# public:
#     int climbStairs(int n) {
#            int ways[n+1];
#     ways[0] = 1;
#     ways[1] = 1;
#     for (int i = 2; i <= n; i++) ways[i] = ways[i - 1] + ways[i - 2];
#     return ways[n];
#     }
# };
#
# BONUS: Can you come up with O(logn) solution?
import operator as op
from functools import reduce


def ncr(n, k):
    k = min(k, n-k)
    numerator = reduce(op.mul, range(n, n-k, -1), 1)
    denominator = reduce(op.mul, range(1, k+1), 1)
    return numerator // denominator


def fibonacci_by_counting(number):
    a, b = 0, 1
    for _ in range(1, number):
        a, b = b, a + b
    return b


def fibonacci_by_formula(number):
    if number >= 72:
        return fibonacci_by_counting(number)
    square_root_of_5 = 5.0 ** 0.5
    φ = (1.0 + square_root_of_5) / 2.0  # Phi could use greek letter!
    ψ = (1.0 - square_root_of_5) / 2.0  # Psi
    return (φ ** number - ψ ** number) / square_root_of_5
#
#  pattern     length quantity comment
#  111...111 = n
#  111...12  = n-1
#  111...21
#  112...11
#  121...11
#  211...11
#  ...
#  222...2   = n/2    1 this   pattern only if n is even


def climb_stairs_first_solution(total_steps):
    two_steps_total = total_steps // 2
    distinct_ways = 1
    for two_steps in range(1, two_steps_total+1):
        one_steps = total_steps - two_steps * 2
        distinct_ways += ncr(two_steps + one_steps, two_steps)
    return distinct_ways


def climb_stairs_as_fibonacci_number(total_steps):
    return fibonacci_by_counting(total_steps)


def climb_stairs_by_formula(total_steps):
    return fibonacci_by_formula(total_steps)


if __name__ == '__main__':

    for stair_one_steps in range(100):
        k = climb_stairs_first_solution(stair_one_steps)
        f1 = fibonacci_by_counting(stair_one_steps+1)
        f2 = int(fibonacci_by_formula(stair_one_steps+1))
        print(stair_one_steps, abs(f1-k), abs(f2-k), k, f2)
