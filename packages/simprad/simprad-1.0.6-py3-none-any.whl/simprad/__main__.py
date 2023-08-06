def main() -> None:
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
    main()
