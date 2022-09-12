from termighty.settings.config import Config


class KeyProcessor:
    """
    Performs all text processing operations given rows of text, a cursor position, and a key input.
    """

    @classmethod
    def key_alt_arrow_down(
        cls, raw_text: list[str, ...], cursor_position: tuple[int, int], selected: list[tuple[int, int], ...]
    ) -> tuple[tuple[int, int], list[tuple[int, int], ...]]:
        """
        Perform the actions of method `key_arrow_down` and also adds all the characters between the current cursor
        position and new cursor position to the list of currently selected keys if they aren't already in the list. If
        they are already in the list, deselects the given characters, removing them from the list.
        """
        new_cursor_position = cls.key_arrow_down(raw_text=raw_text, cursor_position=cursor_position, selected=[])
        selected = cls.select_range(
            raw_text=raw_text,
            cursor_position=cursor_position,
            new_cursor_position=new_cursor_position,
            selected=selected,
        )
        return new_cursor_position, selected

    @classmethod
    def key_alt_arrow_left(
        cls, raw_text: list[str, ...], cursor_position: tuple[int, int], selected: list[tuple[int, int], ...]
    ) -> tuple[tuple[int, int], list[tuple[int, int], ...]]:
        """
        Perform the actions of method `key_arrow_left` and also adds the character to the left of the cursor to the list
        of currently selected keys if it isn't already in the list.  If it is already in the list, deselects the given
        character, removing it from the list.
        """
        new_cursor_position = cls.key_arrow_left(raw_text=raw_text, cursor_position=cursor_position, selected=[])
        selected = cls.select_range(
            raw_text=raw_text,
            cursor_position=cursor_position,
            new_cursor_position=new_cursor_position,
            selected=selected,
        )
        return new_cursor_position, selected

    @classmethod
    def key_alt_arrow_right(
        cls, raw_text: list[str, ...], cursor_position: tuple[int, int], selected: list[tuple[int, int], ...]
    ) -> tuple[tuple[int, int], list[tuple[int, int], ...]]:
        """
        Perform the actions of method `key_arrow_right` and also adds the character to the right of the cursor to the
        list of currently selected keys if it isn't already in the list.  If it is already in the list, deselects the
        given character, removing it from the list.
        """
        new_cursor_position = cls.key_arrow_right(raw_text=raw_text, cursor_position=cursor_position, selected=[])
        selected = cls.select_range(
            raw_text=raw_text,
            cursor_position=cursor_position,
            new_cursor_position=new_cursor_position,
            selected=selected,
        )
        return new_cursor_position, selected

    @classmethod
    def key_alt_arrow_up(
        cls, raw_text: list[str, ...], cursor_position: tuple[int, int], selected: list[tuple[int, int], ...]
    ) -> tuple[tuple[int, int], list[tuple[int, int], ...]]:
        """
        Perform the actions of method `key_arrow_up` and also adds all the characters between the current cursor
        position and new cursor position to the list of currently selected keys if they aren't already in the list. If
        they are already in the list, deselects the given characters, removing them from the list.
        """
        new_cursor_position = cls.key_arrow_up(raw_text=raw_text, cursor_position=cursor_position, selected=[])
        selected = cls.select_range(
            raw_text=raw_text,
            cursor_position=cursor_position,
            new_cursor_position=new_cursor_position,
            selected=selected,
        )
        return new_cursor_position, selected

    @classmethod
    def key_arrow_down(
        cls, raw_text: list[str, ...], cursor_position: tuple[int, int], selected: list[tuple[int, int], ...]
    ) -> tuple[int, int]:
        """
        Move the cursor down by one row, unless it is positioned at the last row of the text.

        If the current row is longer than the one below, move the cursor to the position of the last character in the
        row below, otherwise leave the cursor column position unchanged.

        If some text is selected, considers the cursor to be at the end of the selection.
        """
        if not selected:
            row, col = cursor_position
        else:
            row, col = selected[-1]

        if row == len(raw_text) - 1:
            new_cursor_position = cursor_position
        else:
            new_col = min(col, len(raw_text[row + 1]))
            new_cursor_position = (row + 1, new_col)
        return new_cursor_position

    @classmethod
    def key_arrow_left(
        cls, raw_text: list[str, ...], cursor_position: tuple[int, int], selected: list[tuple[int, int], ...]
    ) -> tuple[int, int]:
        """
        Move the cursor left by one column, unless it is positioned at the first row & column of the text.

        If the cursor is at the first column, and NOT on the first row, move it to the end of the previous row.

        If some text is selected, considers the cursor to be at the beginning of the selection.
        """
        if not selected:
            row, col = cursor_position
        else:
            row, col = selected[0]

        if cursor_position == (0, 0):
            new_cursor_position = cursor_position
        elif col == 0:
            new_cursor_position = (row - 1, len(raw_text[row - 1]))
        else:
            new_cursor_position = (row, col - 1)
        return new_cursor_position

    @classmethod
    def key_arrow_right(
        cls, raw_text: list[str, ...], cursor_position: tuple[int, int], selected: list[tuple[int, int], ...]
    ) -> tuple[int, int]:
        """
        Move the cursor right by one column, unless it is positioned at the last row & column of the text.

        If the cursor is at the last column, and NOT on the last row, move it to the beginning of the next row.

        If some text is selected, considers the cursor to be at the end of the selection.
        """
        if not selected:
            row, col = cursor_position
        else:
            row, col = selected[-1]

        if cursor_position == (len(raw_text) - 1, len(raw_text[-1])):
            new_cursor_position = (row, col)
        elif col == len(raw_text[row]):
            new_cursor_position = (row + 1, 0)
        else:
            new_cursor_position = (row, col + 1)
        return new_cursor_position

    @classmethod
    def key_arrow_up(
        cls, raw_text: list[str, ...], cursor_position: tuple[int, int], selected: list[tuple[int, int], ...]
    ) -> tuple[int, int]:
        """
        Move the cursor up by one row, unless it is positioned at the first row of the text.

        If the current row is longer than the one above, move the cursor to the position of the last character in the
        row above, otherwise leave the cursor column position unchanged.
        """
        if not selected:
            row, col = cursor_position
        else:
            row, col = selected[0]

        if row == 0:
            new_cursor_position = cursor_position
        else:
            new_col = min(col, len(raw_text[row - 1]))
            new_cursor_position = (row - 1, new_col)
        return new_cursor_position

    @classmethod
    def key_backspace(
        cls, raw_text: list[str, ...], cursor_position: tuple[int, int], selected: list[tuple[int, int], ...]
    ) -> tuple[list[str, ...], tuple[int, int]]:
        """
        Remove the character to the left of the current cursor position.  Moot if the cursor is positioned at the first
        row & column of the text.

        If the cursor is at the first column, and NOT on the first row, combines the current and previous rows into one,
        without removing any characters.

        Special case: if all characters to the left of the cursor are spaces, and the cursor position is a multiple of
        the tab-length, backspace will remove one tab-length's worth of spaces to the left of the cursor, instead of
        just one.

        If some text is selected, deletes all selected text, and sets the cursor to the beginning of the selection.
        """
        if selected:
            new_text, new_cursor_position = cls.remove_selected(raw_text, cursor_position, selected)
        else:
            row, col = cursor_position
            # If the cursor is at position (0,0), backspace has no effect, so make no changes to the text.
            if cursor_position == (0, 0):
                new_text = raw_text
                new_cursor_position = cursor_position
            # If the cursor is at position (N,0), backspace appends row N to row N-1.
            elif col == 0:
                new_text = raw_text[: row - 1] + [raw_text[row - 1] + raw_text[row]] + raw_text[row + 1 :]
                new_cursor_position = (row - 1, len(raw_text[row - 1]))
            # If all characters to the left of the cursor are spaces, and the column is a multiple of the tab-length,
            # remove one tab-length's worth of preceeding spaces.
            elif raw_text[row][:col].strip() == "" and col % Config.tab_length == 0:
                new_text = (
                    raw_text[:row]
                    + [raw_text[row][: col - Config.tab_length] + raw_text[row][col:]]
                    + raw_text[row + 1 :]
                )
                new_cursor_position = (row, col - Config.tab_length)
            # If the cursor is at position (M,N), backspace removes character (M,N-1).
            else:
                new_text = raw_text[:row] + [raw_text[row][: col - 1] + raw_text[row][col:]] + raw_text[row + 1 :]
                new_cursor_position = (row, col - 1)

        return new_text, new_cursor_position

    @classmethod
    def key_char(
        cls, raw_text: list[str, ...], cursor_position: tuple[int, int], selected: list[tuple[int, int], ...], char: str
    ) -> tuple[list[str, ...], tuple[int, int]]:
        """
        Add a character at the designated cursor position.

        If some text is selected, deletes all selected text, sets the cursor to the beginning of the selection, then
        adds the character at that position.
        """
        if selected:
            raw_text, cursor_position = cls.remove_selected(raw_text, cursor_position, selected)
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
        cls, raw_text: list[str, ...], cursor_position: tuple[int, int], selected: list[tuple[int, int], ...]
    ) -> tuple[list[str, ...], tuple[int, int], list[tuple[int, int], ...]]:
        """
        Swaps the current row (or selected rows) with the subsequent row.

        Applies the indentation level of the first non-empty row beneath the selected rows.

        If one of the selected rows is the last row, no changes are made.
        """
        selected_rows = set([cursor_position[0]] + [position[0] for position in selected])
        if len(raw_text) - 1 in selected_rows:
            new_text = raw_text
            new_cursor_position = cursor_position
            new_selected = selected
        else:
            row, col = cursor_position
            row_min = min(row, row if not selected else selected[0][0])
            row_max = max(row, row if not selected else selected[-1][0])

            indent = 0
            for indent_row in raw_text[row_max + 1 :]:
                if indent_row.strip():
                    indent = len(indent_row) - len(indent_row.lstrip())
                    break

            pad = " " * indent
            indent_rows = [pad + indent_rows.strip() for indent_rows in raw_text[row_min : row_max + 1]]
            new_text = raw_text[:row_min] + [raw_text[row_max + 1]] + indent_rows + raw_text[row_max + 2 :]

            diffs = {idx: indent - (len(raw_text[idx]) - len(raw_text[idx].lstrip())) for idx in selected_rows}
            if selected:
                new_selected = []
                for position in selected:
                    new_selected.append((position[0] + 1, position[1] + diffs[position[0]]))
            else:
                new_selected = selected
            new_cursor_position = (cursor_position[0] + 1, cursor_position[1] + diffs[cursor_position[0]])

        return new_text, new_cursor_position, new_selected

    @classmethod
    def key_ctrl_left(
        cls, raw_text: list[str, ...], cursor_position: tuple[int, int]
    ) -> tuple[list[str, ...], tuple[int, int]]:
        """
        Moves the cursor to the left until the beginning of the preceeding word is reached. Performs this function
        regardless of which row contains the preceeding word.
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
        which row contains the next word.
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
        cls, raw_text: list[str, ...], cursor_position: tuple[int, int], selected: list[tuple[int, int], ...]
    ) -> tuple[list[str, ...], tuple[int, int], list[tuple[int, int], ...]]:
        """
        Swaps the current row (or selected rows) with the preceeding row.

        Applies the indentation level of the first non-empty row above the row preceeding the selected rows.

        If one of the selected rows is row zero, no changes are made.
        """
        selected_rows = set([cursor_position[0]] + [position[0] for position in selected])
        if 0 in selected_rows:
            new_text = raw_text
            new_cursor_position = cursor_position
            new_selected = selected
        else:
            row, col = cursor_position
            row_min = min(row, row if not selected else selected[0][0])
            row_max = max(row, row if not selected else selected[-1][0])

            indent = 0
            for indent_row in raw_text[: row_min - 1][::-1]:
                if indent_row.strip():
                    indent = len(indent_row) - len(indent_row.lstrip())
                    break

            pad = " " * indent
            indent_rows = [pad + indent_rows.strip() for indent_rows in raw_text[row_min : row_max + 1]]
            new_text = raw_text[: row_min - 1] + indent_rows + [raw_text[row_min - 1]] + raw_text[row_max + 1 :]

            diffs = {idx: indent - (len(raw_text[idx]) - len(raw_text[idx].lstrip())) for idx in selected_rows}
            if selected:
                new_selected = []
                for position in selected:
                    new_selected.append((position[0] - 1, position[1] + diffs[position[0]]))
            else:
                new_selected = selected
            new_cursor_position = (cursor_position[0] - 1, cursor_position[1] + diffs[cursor_position[0]])

        return new_text, new_cursor_position, new_selected

    @classmethod
    def key_delete(
        cls, raw_text: list[str, ...], cursor_position: tuple[int, int], selected: list[tuple[int, int], ...]
    ) -> tuple[list[str, ...]]:
        """
        Remove the character to the right of the current cursor position.  Moot if the cursor is positioned at the last
        row & column of the text.
        If the cursor is at the last column, and NOT on the last row, combines the current and next rows into one,
        without removing any characters.
        If some text is selected, deletes all selected text, and sets the cursor to the beginning of the selection.
        """
        if selected:
            new_text, new_cursor_position = cls.remove_selected(raw_text, cursor_position, selected)
        else:
            new_cursor_position = cursor_position
            row, col = cursor_position
            # If the cursor is at the end of the text, delete has no effect, so make no changes to the text.
            if cursor_position == (len(raw_text) - 1, len(raw_text[-1])):
                new_text = raw_text

            # If the cursor is at the end of row N, delete appends row N+1 to row N.
            elif col == len(raw_text[row]):
                new_text = raw_text[:row] + [raw_text[row] + raw_text[row + 1]] + raw_text[row + 2 :]

            # If the cursor is at position (M,N), backspace removes character (M,N-1).
            else:
                new_text = raw_text[:row] + [raw_text[row][:col] + raw_text[row][col + 1 :]] + raw_text[row + 1 :]

        return new_text, new_cursor_position

    @classmethod
    def key_end(cls, raw_text: list[str, ...], cursor_position: tuple[int, int]) -> tuple[int, int]:
        """
        Move the cursor to the end of the current row, if it isn't already there.
        """
        row, col = cursor_position
        new_cursor_position = (row, len(raw_text[row]))
        return new_cursor_position

    @classmethod
    def key_enter(
        cls, raw_text: list[str, ...], cursor_position: tuple[int, int], selected: list[tuple[int, int], ...]
    ) -> tuple[list[str, ...], tuple[int, int]]:
        """
        If the cursor is at the last column, create a new empty row below the current row and move the cursor there.

        Otherwise, divide the current row at the current cursor position, and move the second half into a new row below
        the first half, and place the cursor and the first column of this new row.

        If some text is selected, deletes all selected text, and sets the cursor to the beginning of the selection,
        then runs the rest of this method as it normally would.

        If the current row has indentation, apply the same indentation to the newly created row.
        """
        if selected:
            raw_text, cursor_position = cls.remove_selected(raw_text, cursor_position, selected)
        row, col = cursor_position
        indent = len(raw_text[row]) - len(raw_text[row].lstrip())
        pad = " " * indent
        new_text = raw_text[:row] + [raw_text[row][:col]] + [pad + raw_text[row][col:]] + raw_text[row + 1 :]
        new_cursor_position = (row + 1, indent)

        return new_text, new_cursor_position

    @classmethod
    def key_home(cls, raw_text: list[str, ...], cursor_position: tuple[int, int]) -> tuple[int, int]:
        """
        Move the cursor to the beginning of the current row, if it isn't already there.
        """
        row, col = cursor_position
        new_cursor_position = (row, 0)
        return new_cursor_position

    @classmethod
    def key_tab(
        cls, raw_text: list[str, ...], cursor_position: tuple[int, int], selected: list[tuple[int, int], ...]
    ) -> tuple[list[str, ...], tuple[int, int], list[tuple[int, int], ...]]:
        """
        Given a cursor column position P, and a tab length L, adds N spaces starting at P, such that,
            N = L * (P // L) + L,
        where // represents integer division.
        If some text is selected, simply prepends a number of spaces equal to the tab-length to all rows that have one
        or more selected characters.
        """
        if selected:
            rows = set(position[0] for position in selected)
            new_text = [" " * Config.tab_length + row if n in rows else row for n, row in enumerate(raw_text)]
            selected = [(row, column + Config.tab_length) for row, column in selected]

            new_cursor_position = (cursor_position[0], cursor_position[1] + Config.tab_length)
        else:
            row, col = cursor_position

            new_col = Config.tab_length * (col // Config.tab_length) + Config.tab_length
            N_spaces = new_col - col
            new_text = (
                raw_text[:row] + [raw_text[row][:col] + " " * N_spaces + raw_text[row][col:]] + raw_text[row + 1 :]
            )

            new_cursor_position = (row, new_col)

        return new_text, new_cursor_position, selected

    @classmethod
    def process_key(
        cls, raw_text: list[str, ...], cursor_position: tuple[int, int], selected: list[tuple[int, int], ...], key: str
    ) -> tuple[bool, list[str, ...], tuple[int, int], list[tuple[int, int], ...]]:
        """
        Take the current text and cursor position, and modify them using the given key input.
        """
        call = True
        match key:
            case "Backspace":
                raw_text, cursor_position = cls.key_backspace(raw_text, cursor_position, selected)
                selected = []
            case "Delete" | "Keypad-Delete":
                raw_text, cursor_position = cls.key_delete(raw_text, cursor_position, selected)
                selected = []
            case "Space":
                raw_text, cursor_position = cls.key_char(raw_text, cursor_position, selected, " ")
            case "Enter":
                raw_text, cursor_position = cls.key_enter(raw_text, cursor_position, selected)
                selected = []
            case "Left" | "Keypad-Left":
                cursor_position = cls.key_arrow_left(raw_text, cursor_position, selected)
                selected = []
            case "Right" | "Keypad-Right":
                cursor_position = cls.key_arrow_right(raw_text, cursor_position, selected)
                selected = []
            case "Up" | "Keypad-Up":
                cursor_position = cls.key_arrow_up(raw_text, cursor_position, selected)
                selected = []
            case "Down" | "Keypad-Down":
                cursor_position = cls.key_arrow_down(raw_text, cursor_position, selected)
                selected = []
            case "Alt-Left":
                cursor_position, selected = cls.key_alt_arrow_left(raw_text, cursor_position, selected)
            case "Alt-Right":
                cursor_position, selected = cls.key_alt_arrow_right(raw_text, cursor_position, selected)
            case "Alt-Up":
                cursor_position, selected = cls.key_alt_arrow_up(raw_text, cursor_position, selected)
            case "Alt-Down":
                cursor_position, selected = cls.key_alt_arrow_down(raw_text, cursor_position, selected)
            case "Ctrl-Left":
                cursor_position = cls.key_ctrl_left(raw_text, cursor_position)
                selected = []
            case "Ctrl-Right":
                cursor_position = cls.key_ctrl_right(raw_text, cursor_position)
                selected = []
            case "Ctrl-Up":
                raw_text, cursor_position, selected = cls.key_ctrl_up(raw_text, cursor_position, selected)
            case "Ctrl-Down":
                raw_text, cursor_position, selected = cls.key_ctrl_down(raw_text, cursor_position, selected)
            case "Home" | "Keypad-Home":
                cursor_position = cls.key_home(raw_text, cursor_position)
                selected = []
            case "End" | "Keypad-End":
                cursor_position = cls.key_end(raw_text, cursor_position)
                selected = []
            case "Tab":
                raw_text, cursor_position, selected = cls.key_tab(raw_text, cursor_position, selected)
            case other:
                if len(key) == 1:
                    raw_text, cursor_position = cls.key_char(raw_text, cursor_position, selected, key)
                    selected = []
                else:
                    call = False

        return call, raw_text, cursor_position, selected

    @classmethod
    def remove_selected(
        cls, raw_text: list[str, ...], cursor_position: tuple[int, int], selected: list[tuple[int, int], ...]
    ) -> tuple[list[str, ...], tuple[int, int]]:
        """
        Given a set of coordinates for characters that are currently selected, removes these characters from the text
        and sets the position of the cursor to that of the first selected character.
        """
        row, col = selected[-1]
        new_cursor_position = selected[0]
        rows = list(set(position[0] for position in selected))

        row_min = rows[0]
        col_min = selected[0][1]
        row_max = rows[-1]
        col_max = selected[-1][1]

        new_text = (
            raw_text[: rows[0]]
            + [raw_text[row_min][:col_min] + raw_text[row_max][col_max + 1 :]]
            + raw_text[row_max + 1 :]
        )

        return new_text, new_cursor_position

    @classmethod
    def select_range(
        cls,
        raw_text: list[str, ...],
        cursor_position: tuple[int, int],
        new_cursor_position: tuple[int, int],
        selected: list[tuple[int, int], ...],
    ) -> list[tuple[int, int], ...]:
        """
        Determine which coordinates should be added and/or removed from the list of selected keys based on the movement
        of the cursor.
        """
        position_range = []
        row_start = cursor_position[0]
        row_stop = new_cursor_position[0]

        if row_start == row_stop:
            reversed = cursor_position[1] > new_cursor_position[1]
        else:
            reversed = row_start > row_stop

        if reversed:
            step = -1
            row_stop -= 1
        else:
            step = 1
            row_stop += 1

        rows = range(row_start, row_stop, step)[::step]
        for row in rows:
            if reversed:
                column_start = len(raw_text[row]) - 1
                column_stop = -1
                if row == rows[-1]:
                    column_start = min(cursor_position[1], len(raw_text[row])) - 1
                if row == rows[0]:
                    column_stop = new_cursor_position[1] - 1
            else:
                column_start = 0
                column_stop = len(raw_text[row])
                if row == rows[0]:
                    column_start = cursor_position[1]
                if row == rows[-1]:
                    column_stop = min(new_cursor_position[1], len(raw_text[row]))

            columns = range(column_start, column_stop, step)[::step]

            for column in columns:
                position_range.append((row, column))

        for position in position_range:
            if position not in selected:
                selected.append(position)
            else:
                selected.remove(position)

        selected.sort(key=lambda element: element[1])
        selected.sort(key=lambda element: element[0])

        return selected
