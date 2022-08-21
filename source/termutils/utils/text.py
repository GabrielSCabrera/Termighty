def bold(string: str) -> str:
    """
    Converts the given string to bold.
    """
    return f"\033[1m{string}"


def italic(string: str) -> str:
    """
    Converts the given string to italic.
    """
    return f"\033[3m{string}"


def norm() -> str:
    """
    Returns the text style to normal.
    """
    return "\033[m"


def cursor_to(y: int, x: int) -> None:
    """
    Moves the cursor to the designated terminal coordinates.
    Uses (0,0) as the origin (top-left of the terminal) with the y-axis
    pointing downwards, and the x-axis pointing to the right.
    """
    print(f"\033[{y+1};{x+1}f", end="")
