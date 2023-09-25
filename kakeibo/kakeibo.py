# from functools import cache
#
# @cache
# def fib(n: int) -> int:
#     if n < 1:
#         return 0
#     if n == 1:
#         return n
#     else:
#         return fib(n - 1) + fib(n - 2)
from typing import Iterator


def fibonacci(n: int) -> Iterator[int]:
    idx = -1
    a, b = 0, 1
    while idx < n:
        yield a
        a, b = b, a + b
        idx += 1


def fib(n: int) -> int:
    if n < 1:
        return 0
    return [f for f in fibonacci(n)][n]
