import pytest

from kakeibo.kakeibo import fib


@pytest.mark.parametrize(
    "input, expected",
    [(-1, 0), (0, 0), (1, 1), (2, 1), (4, 3), (5, 5), (111, 70492524767089125814114)],
)
def test_fib(input: int, expected: int) -> None:
    assert fib(input) == expected
