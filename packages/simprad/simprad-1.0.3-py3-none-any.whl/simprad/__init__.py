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


def _main() -> None:
    complicated_radicand = float(input("Radical to simplify: √"))
    root = float(input("Root [2]: ") or 2)
    multiple, radicand = simprad(complicated_radicand, root)

    if root % 1 == 0:
        # If the decimal point is .0, drop it for the output
        root = int(root)

    if root == 2:
        symbol = "√"
    elif root == 3:
        symbol = "∛"
    elif root == 4:
        symbol = "∜"
    else:
        symbol = f"{root}√"

    if radicand % 1 == 0:
        # If the decimal point is .0, drop it for the output
        radicand = int(radicand)

    if multiple == radicand == 1:
        print(1)
    elif multiple == 1:
        print(f"{symbol}{radicand}")
    elif radicand == 1:
        print(multiple)
    else:
        print(f"{multiple} × {symbol}{radicand}")

if __name__ == "__main__":
    _main()
