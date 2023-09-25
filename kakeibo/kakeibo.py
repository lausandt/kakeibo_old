from functools import cache


@cache
def fib(n: int) -> int:
    if n < 1:
        return 0
    if n == 1:
        return n
    else:
        return fib(n - 1) + fib(n - 2)
