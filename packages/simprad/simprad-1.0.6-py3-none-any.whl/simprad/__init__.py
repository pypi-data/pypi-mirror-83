from typing import Tuple, Union

def simprad(radicand: float, root: float=2) -> Tuple[Union[int, complex], float]:
    """
    Simplify a radical into a multiple of the square root of a prime number.
    When the input is negative, the output coefficient will be complex.
    """
    is_complex = False

    if radicand < 0:
        is_complex = True
        radicand = -radicand

    coefficient = 1
    factor = 2
    while factor <= (radicand ** root ** -1):
        while radicand % (factor ** root) == 0:
            coefficient *= factor
            radicand /= factor ** root
        if factor == 2:
            factor = 1
        factor += 2

    if is_complex:
        coefficient = complex(0, coefficient)

    return (coefficient, radicand)
