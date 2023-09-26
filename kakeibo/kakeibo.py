from typing import Iterator


def fibonacci(n: int) -> Iterator[int]:
    idx = 0
    a, b = 0, 1
    while idx <= n:
        yield a
        a, b = b, a + b
        idx += 1


def fib(n: int) -> int:
    """function that returns the nth fibonacci number"""
    if n < 1:
        return 0
    return [f for f in fibonacci(n)][n]
