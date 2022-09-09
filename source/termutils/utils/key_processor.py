from termutils.settings.config import Config


class KeyProcessor:
    """
    Performs all text processing operations given lines of text, a cursor position, and a key input.
    """

    @classmethod
    def key_arrow_down(cls, raw_text: list[str, ...], cursor_position: tuple[int, int]) -> tuple[int, int]:
        """
        Move the cursor down by one line, unless it is positioned at the last line of the text.
        If the current line is longer than the one below, move the cursor to the position of the last character in the
        line below, otherwise leave the cursor column position unchanged.
        """
        row, col = cursor_position
        if row == len(raw_text) - 1:
            new_cursor_position = cursor_position
        else:
            new_col = min(col, len(raw_text[row + 1]))
            new_cursor_position = (row + 1, new_col)
        return new_cursor_position

    @classmethod
    def key_arrow_left(cls, raw_text: list[str, ...], cursor_position: tuple[int, int]) -> tuple[int, int]:
        """
        Move the cursor left by one column, unless it is positioned at the first line & column of the text.
        If the cursor is at the first column, and NOT on the first line, move it to the end of the previous line.
        """
        row, col = cursor_position
        if cursor_position == (0, 0):
            new_cursor_position = cursor_position
        elif col == 0:
            new_cursor_position = (row - 1, len(raw_text[row - 1]))
        else:
            new_cursor_position = (row, col - 1)
        return new_cursor_position

    @classmethod
    def key_arrow_right(cls, raw_text: list[str, ...], cursor_position: tuple[int, int]) -> tuple[int, int]:
        """
        Move the cursor right by one column, unless it is positioned at the last line & column of the text.
        If the cursor is at the last column, and NOT on the last line, move it to the beginning of the next line.
        """
        row, col = cursor_position
        if cursor_position == (len(raw_text) - 1, len(raw_text[-1])):
            new_cursor_position = cursor_position
        elif col == len(raw_text[row]):
            new_cursor_position = (row + 1, 0)
        else:
            new_cursor_position = (row, col + 1)
        return new_cursor_position

    @classmethod
    def key_arrow_up(cls, raw_text: list[str, ...], cursor_position: tuple[int, int]) -> tuple[int, int]:
        """
        Move the cursor up by one line, unless it is positioned at the first line of the text.
        If the current line is longer than the one above, move the cursor to the position of the last character in the
        line above, otherwise leave the cursor column position unchanged.
        """
        row, col = cursor_position
        if row == 0:
            new_cursor_position = cursor_position
        else:
            new_col = min(col, len(raw_text[row - 1]))
            new_cursor_position = (row - 1, new_col)
        return new_cursor_position

    @classmethod
    def key_backspace(
        cls, raw_text: list[str, ...], cursor_position: tuple[int, int]
    ) -> tuple[list[str, ...], tuple[int, int]]:
        """
        Remove the character to the left of the current cursor position.  Moot if the cursor is positioned at the first
        line & column of the text.
        If the cursor is at the first column, and NOT on the first line, combines the current and previous lines into
        one, without removing any characters.
        """
        row, col = cursor_position
        # If the cursor is at position (0,0), backspace has no effect, so make no changes to the text.
        if cursor_position == (0, 0):
            new_text = raw_text
            new_cursor_position = cursor_position
        # If the cursor is at position (N,0), backspace appends line N to line N-1.
        elif col == 0:
            new_text = raw_text[: row - 1] + [raw_text[row - 1] + raw_text[row]] + raw_text[row + 1 :]
            new_cursor_position = (row - 1, len(raw_text[row - 1]))
        # If the cursor is at position (M,N), backspace removes character (M,N-1).
        else:
            new_text = raw_text[:row] + [raw_text[row][: col - 1] + raw_text[row][col:]] + raw_text[row + 1 :]
            new_cursor_position = (row, col - 1)

        return new_text, new_cursor_position

    @classmethod
    def key_char(
        cls, raw_text: list[str, ...], cursor_position: tuple[int, int], char: str
    ) -> tuple[list[str, ...], tuple[int, int]]:
        """
        Add a character at the designated cursor position.
        """
        row, col = cursor_position
        new_text = raw_text[:row] + [raw_text[row][:col] + char + raw_text[row][col:]] + raw_text[row + 1 :]

        new_cursor_position = (row, col + 1)

        return new_text, new_cursor_position

    @classmethod
    def key_ctrl_backspace(
        cls, raw_text: list[str, ...], cursor_position: tuple[int, int]
    ) -> tuple[list[str, ...], tuple[int, int]]:
        """
        Performs a ctrl-backspace on the given list of characters, using the context attached to them (see docstring in
        cls._process_key).
        """

    @classmethod
    def key_ctrl_delete(
        cls, raw_text: list[str, ...], cursor_position: tuple[int, int]
    ) -> tuple[list[str, ...], tuple[int, int]]:
        """
        Performs a ctrl-delete on the given list of characters, using the context attached to them (see docstring in
        cls._process_key).
        """

    @classmethod
    def key_ctrl_down(
        cls, raw_text: list[str, ...], cursor_position: tuple[int, int]
    ) -> tuple[list[str, ...], tuple[int, int]]:
        """
        Swaps the below line with the current one.
        """

    @classmethod
    def key_ctrl_left(
        cls, raw_text: list[str, ...], cursor_position: tuple[int, int]
    ) -> tuple[list[str, ...], tuple[int, int]]:
        """
        Moves the cursor to the left until the beginning of the preceeding word is reached. Performs this function
        regardless of which line contains the preceeding word.
        """
        row, col = cursor_position
        if cursor_position == (0, 0):
            new_cursor_position = cursor_position
        else:
            if len(raw_text[row][:col].lstrip()) == 0:
                col = len(raw_text[row - 1].rstrip())
                row -= 1

            new_col = raw_text[row].rfind(" ", 0, col - 1) + 1
            new_cursor_position = (row, new_col if new_col >= 0 else 0)

        return new_cursor_position

    @classmethod
    def key_ctrl_right(
        cls, raw_text: list[str, ...], cursor_position: tuple[int, int]
    ) -> tuple[list[str, ...], tuple[int, int]]:
        """
        Moves the cursor to the right until the end of the next word is reached. Performs this function regardless of
        which line contains the next word.
        """
        row, col = cursor_position
        if cursor_position == (len(raw_text) - 1, len(raw_text[-1])):
            new_cursor_position = cursor_position
        else:
            if col == len(raw_text[row]):
                col = len(raw_text[row + 1]) - len(raw_text[row + 1].lstrip())
                row += 1

            if col < len(raw_text[row]) and raw_text[row][col] == " ":
                col = len(raw_text[row][col:]) - len(raw_text[row][col:].lstrip()) + col

            new_col = raw_text[row].find(" ", col)
            new_cursor_position = (row, new_col if new_col >= 0 else len(raw_text[row]))

        return new_cursor_position

    @classmethod
    def key_ctrl_up(
        cls, raw_text: list[str, ...], cursor_position: tuple[int, int]
    ) -> tuple[list[str, ...], tuple[int, int]]:
        """
        Swaps the above line with the current one.
        """

    @classmethod
    def key_delete(cls, raw_text: list[str, ...], cursor_position: tuple[int, int]) -> list[str, ...]:
        """
        Remove the character to the right of the current cursor position.  Moot if the cursor is positioned at the last
        line & column of the text.
        If the cursor is at the last column, and NOT on the last line, combines the current and next lines into one,
        without removing any characters.
        """

        row, col = cursor_position
        # If the cursor is at the end of the text, delete has no effect, so make no changes to the text.
        if cursor_position == (len(raw_text) - 1, len(raw_text[-1])):
            new_text = raw_text

        # If the cursor is at the end of line N, delete appends line N+1 to line N.
        elif col == len(raw_text[row]):
            new_text = raw_text[:row] + [raw_text[row] + raw_text[row + 1]] + raw_text[row + 2 :]

        # If the cursor is at position (M,N), backspace removes character (M,N-1).
        else:
            new_text = raw_text[:row] + [raw_text[row][:col] + raw_text[row][col + 1 :]] + raw_text[row + 1 :]

        return new_text

    @classmethod
    def key_end(cls, raw_text: list[str, ...], cursor_position: tuple[int, int]) -> tuple[int, int]:
        """
        Move the cursor to the end of the current line, if it isn't already there.
        """
        row, col = cursor_position
        new_cursor_position = (row, len(raw_text[row]))
        return new_cursor_position

    @classmethod
    def key_enter(
        cls, raw_text: list[str, ...], cursor_position: tuple[int, int]
    ) -> tuple[list[str, ...], tuple[int, int]]:
        """
        If the cursor is at the last column, create a new empty line below the current line and move the cursor there.
        Otherwise, divide the current line at the current cursor position, and move the second half into a new line
        below the first half, and place the cursor and the first column of this new line.
        """
        row, col = cursor_position
        new_text = raw_text[:row] + [raw_text[row][:col]] + [raw_text[row][col:]] + raw_text[row + 1 :]
        new_cursor_position = (row + 1, 0)

        return new_text, new_cursor_position

    @classmethod
    def key_home(cls, raw_text: list[str, ...], cursor_position: tuple[int, int]) -> tuple[int, int]:
        """
        Move the cursor to the beginning of the current line, if it isn't already there.
        """
        row, col = cursor_position
        new_cursor_position = (row, 0)
        return new_cursor_position

    @classmethod
    def key_tab(
        cls, raw_text: list[str, ...], cursor_position: tuple[int, int]
    ) -> tuple[list[str, ...], tuple[int, int]]:
        """
        Given a cursor column position P, and a tab length L, adds N spaces starting at P, such that,
            N = L * (P // L) + L,
        where // represents integer division.
        """
        row, col = cursor_position
        new_col = Config.tab_length * (col // Config.tab_length) + Config.tab_length
        N_spaces = new_col - col
        new_text = raw_text[:row] + [raw_text[row][:col] + " " * N_spaces + raw_text[row][col:]] + raw_text[row + 1 :]

        new_cursor_position = (row, new_col)

        return new_text, new_cursor_position

    @classmethod
    def process_key(cls, raw_text: list[str, ...], cursor_position: tuple[int, int], key: str) -> None:
        """
        Take the current text and cursor position, and modify them using the given key input.
        """
        call = True
        match key:
            case "Backspace":
                raw_text, cursor_position = cls.key_backspace(
                    raw_text,
                    cursor_position,
                )
            case "Delete":
                raw_text = cls.key_delete(
                    raw_text,
                    cursor_position,
                )
            case "Space":
                raw_text, cursor_position = cls.key_char(raw_text, cursor_position, " ")
            case "Enter":
                raw_text, cursor_position = cls.key_enter(
                    raw_text,
                    cursor_position,
                )
            case "Left":
                cursor_position = cls.key_arrow_left(
                    raw_text,
                    cursor_position,
                )
            case "Right":
                cursor_position = cls.key_arrow_right(
                    raw_text,
                    cursor_position,
                )
            case "Up":
                cursor_position = cls.key_arrow_up(
                    raw_text,
                    cursor_position,
                )
            case "Down":
                cursor_position = cls.key_arrow_down(
                    raw_text,
                    cursor_position,
                )
            case "Ctrl-Left":
                cursor_position = cls.key_ctrl_left(
                    raw_text,
                    cursor_position,
                )
            case "Ctrl-Right":
                cursor_position = cls.key_ctrl_right(
                    raw_text,
                    cursor_position,
                )
            case "Home":
                cursor_position = cls.key_home(
                    raw_text,
                    cursor_position,
                )
            case "End":
                cursor_position = cls.key_end(
                    raw_text,
                    cursor_position,
                )
            case "Tab":
                raw_text, cursor_position = cls.key_tab(
                    raw_text,
                    cursor_position,
                )
            case other:
                if len(key) == 1:
                    raw_text, cursor_position = cls.key_char(raw_text, cursor_position, key)
                else:
                    call = False

        return call, raw_text, cursor_position
