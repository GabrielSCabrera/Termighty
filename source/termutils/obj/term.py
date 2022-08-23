import os


class Term:
    """
    A collection of commands that can be used to make modifications to the terminal state.
    """

    cursor_active = True

    @classmethod
    def clear(cls):
        """
        Cross-platform terminal clear command.
        """
        os.system("cls" if os.name == "nt" else "clear")

    @classmethod
    def print_at(cls, column: int, line: int, string: str):
        """
        Print the given `string` starting at the given `line` and `column`.
        """
        print(f"\x1b7\x1b[{column};{line}f{string}\x1b8", end="", flush=True)

    @classmethod
    def cursor_at(cls, column: int, line: int):
        """
        Move the cursor to the given `line` and `column`.
        """
        print(f"\033[{line};{column}H", end="", flush=True)

    @classmethod
    def cursor_hide(cls):
        """
        Make the cursor invisible.
        """
        print("\033[?25l", end="", flush=True)
        cls.cursor_active = False

    @classmethod
    def cursor_load(cls):
        """
        Loads the cursor position -- save it first by calling `cursor_save`.
        """
        print("\0338", end="", flush=True)

    @classmethod
    def cursor_save(cls):
        """
        Save the cursor position -- reload it by calling `cursor_load`.
        """
        print("\0337", end="", flush=True)

    @classmethod
    def cursor_show(cls):
        """
        Make the cursor visible.
        """
        print("\033[?25h", end="", flush=True)
        cls.cursor_active = True

    @classmethod
    def cursor_toggle(cls):
        """
        If the cursor is visible, make it invisible.  If it is invisible, make it visible.
        """
        if cls.cursor_active:
            print("\033[?25h", end="", flush=True)
        else:
            print("\033[?25l", end="", flush=True)
