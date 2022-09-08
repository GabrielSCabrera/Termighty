from termutils.obj.text_box import TextBox
from termutils.obj.term import Term
from termutils.obj.color import Color
from termutils.obj.listener import Listener
import textwrap
import time

from typing import Optional, Union


class WordProcessor(TextBox):
    """
    A subclass of `TextBox` that uses class `Listener` to detect keyboard inputs, and emulate a fully-functional word
    processor.  Supported advanced functions include:

    * Cursor positioning with the arrow keys,
    * Ctrl-arrow key to move the cursor to the beginning/end of words,
    * Alt-arrow to select text,
    * Deletion of selected text,
    * Copying of selected text.
    """

    def __init__(
        self,
        row_start: int,
        column_start: int,
        row_end: int,
        column_end: int,
        wrap_text: bool = True,
        show_line_numbers: bool = False,
        background: Union[str, Color, tuple[int, int, int]] = None,
        foreground: Union[str, Color, tuple[int, int, int]] = None,
        style: Optional[str] = None,
        cursor_background: Union[str, Color, tuple[int, int, int]] = None,
        cursor_foreground: Union[str, Color, tuple[int, int, int]] = None,
        cursor_style: Optional[str] = None,
    ):
        """
        Creates an instance of TextEditor.  Supports usage of the default listener provided by class LiveMenu.
        """
        self._cursor_position = (0, 0)
        self._wrap_text = wrap_text
        self._line_numbers = show_line_numbers
        self._tab_length = 4

        super().__init__(row_start, column_start, row_end, column_end, background, foreground, style)

        if cursor_background is None:
            cursor_background = self._background.negative()

        if cursor_foreground is None:
            cursor_foreground = self._foreground.negative()

        cursor_background, cursor_foreground, cursor_style = self._check_arguments(
            cursor_background, cursor_foreground, cursor_style
        )

        self._cursor_background = cursor_background
        self._cursor_foreground = cursor_foreground
        self._cursor_style = cursor_style

    def _key_arrow_down(self) -> tuple[int, int]:
        """ """
        row, col = self._cursor_position
        if row == len(self._raw_text) - 1:
            new_cursor_position = self._cursor_position
        else:
            new_col = min(col, len(self._raw_text[row + 1]))
            new_cursor_position = (row + 1, new_col)
        return new_cursor_position

    def _key_arrow_left(self) -> tuple[int, int]:
        """ """
        row, col = self._cursor_position
        if self._cursor_position == (0, 0):
            new_cursor_position = self._cursor_position
        elif col == 0:
            new_cursor_position = (row - 1, len(self._raw_text[row - 1]))
        else:
            new_cursor_position = (row, col - 1)
        return new_cursor_position

    def _key_arrow_right(self) -> tuple[int, int]:
        """ """
        row, col = self._cursor_position
        if self._cursor_position == (len(self._raw_text) - 1, len(self._raw_text[-1])):
            new_cursor_position = self._cursor_position
        elif col == len(self._raw_text[row]):
            new_cursor_position = (row + 1, 0)
        else:
            new_cursor_position = (row, col + 1)
        return new_cursor_position

    def _key_arrow_up(self) -> tuple[int, int]:
        """ """
        row, col = self._cursor_position
        if row == 0:
            new_cursor_position = self._cursor_position
        else:
            new_col = min(col, len(self._raw_text[row - 1]))
            new_cursor_position = (row - 1, new_col)
        return new_cursor_position

    def _key_backspace(self) -> tuple[list[str, ...], tuple[int, int]]:
        """
        Performs a backspace operation on the given list of characters, taking cursor position into account.
        """
        row, col = self._cursor_position
        # If the cursor is at position (0,0), backspace has no effect, so make no changes to the text.
        if self._cursor_position == (0, 0):
            new_text = self._raw_text
            new_cursor_position = self._cursor_position
        # If the cursor is at position (N,0), backspace appends line N to line N-1.
        elif col == 0:
            new_text = (
                self._raw_text[: row - 1] + [self._raw_text[row - 1] + self._raw_text[row]] + self._raw_text[row + 1 :]
            )
            new_cursor_position = (row - 1, len(self._raw_text[row - 1]))
        # If the cursor is at position (M,N), backspace removes character (M,N-1).
        else:
            new_text = (
                self._raw_text[:row]
                + [self._raw_text[row][: col - 1] + self._raw_text[row][col:]]
                + self._raw_text[row + 1 :]
            )
            new_cursor_position = (row, col - 1)

        return new_text, new_cursor_position

    def _key_char(self, char: str) -> tuple[list[str, ...], tuple[int, int]]:
        """
        Add a character at the designated cursor position.
        """
        row, col = self._cursor_position
        new_text = (
            self._raw_text[:row]
            + [self._raw_text[row][:col] + char + self._raw_text[row][col:]]
            + self._raw_text[row + 1 :]
        )

        new_cursor_position = (row, col + 1)

        return new_text, new_cursor_position

    def _key_ctrl_backspace(self) -> tuple[list[str, ...], tuple[int, int]]:
        """
        Performs a ctrl-backspace on the given list of characters, using the context attached to them (see docstring in
        self._process_key).
        """

    def _key_ctrl_delete(self) -> tuple[list[str, ...], tuple[int, int]]:
        """
        Performs a ctrl-delete on the given list of characters, using the context attached to them (see docstring in
        self._process_key).
        """

    def _key_ctrl_down(self) -> tuple[list[str, ...], tuple[int, int]]:
        """
        Swaps the below line with the current one.
        """

    def _key_ctrl_left(self) -> tuple[list[str, ...], tuple[int, int]]:
        """
        Moves the cursor to the left until the beginning of the previous word is reached.
        """
        row, col = self._cursor_position
        if self._cursor_position == (0, 0):
            new_cursor_position = self._cursor_position
        else:
            if len(self._raw_text[row][:col].lstrip()) == 0:
                col = len(self._raw_text[row - 1].rstrip())
                row -= 1

            new_col = self._raw_text[row].rfind(" ", 0, col - 1) + 1
            new_cursor_position = (row, new_col if new_col >= 0 else 0)

        return new_cursor_position

    def _key_ctrl_right(self) -> tuple[list[str, ...], tuple[int, int]]:
        """
        Moves the cursor to the right until the end of the current word is reached.
        """
        row, col = self._cursor_position
        if self._cursor_position == (len(self._raw_text) - 1, len(self._raw_text[-1])):
            new_cursor_position = self._cursor_position
        else:
            if col == len(self._raw_text[row]):
                col = len(self._raw_text[row + 1]) - len(self._raw_text[row + 1].lstrip())
                row += 1

            if col < len(self._raw_text[row]) and self._raw_text[row][col] == " ":
                col = len(self._raw_text[row][col:]) - len(self._raw_text[row][col:].lstrip()) + col

            new_col = self._raw_text[row].find(" ", col)
            new_cursor_position = (row, new_col if new_col >= 0 else len(self._raw_text[row]))

        return new_cursor_position

    def _key_ctrl_up(self) -> tuple[list[str, ...], tuple[int, int]]:
        """
        Swaps the above line with the current one.
        """

    def _key_delete(self) -> list[str, ...]:
        """
        Performs a delete operation on the given list of characters, taking cursor position into account.
        """

        row, col = self._cursor_position
        # If the cursor is at the end of the text, delete has no effect, so make no changes to the text.
        if self._cursor_position == (len(self._raw_text) - 1, len(self._raw_text[-1])):
            new_text = self._raw_text

        # If the cursor is at the end of line N, delete appends line N+1 to line N.
        elif col == len(self._raw_text[row]):
            new_text = (
                self._raw_text[:row] + [self._raw_text[row] + self._raw_text[row + 1]] + self._raw_text[row + 2 :]
            )

        # If the cursor is at position (M,N), backspace removes character (M,N-1).
        else:
            new_text = (
                self._raw_text[:row]
                + [self._raw_text[row][:col] + self._raw_text[row][col + 1 :]]
                + self._raw_text[row + 1 :]
            )

        return new_text

    def _key_end(self) -> tuple[int, int]:
        """ """
        row, col = self._cursor_position
        new_cursor_position = (row, len(self._raw_text[row]))
        return new_cursor_position

    def _key_enter(self) -> tuple[list[str, ...], tuple[int, int]]:
        """ """
        row, col = self._cursor_position
        new_text = (
            self._raw_text[:row] + [self._raw_text[row][:col]] + [self._raw_text[row][col:]] + self._raw_text[row + 1 :]
        )
        new_cursor_position = (row + 1, 0)

        return new_text, new_cursor_position

    def _key_home(self) -> tuple[int, int]:
        """ """
        row, col = self._cursor_position
        new_cursor_position = (row, 0)
        return new_cursor_position

    def _key_tab(self) -> tuple[list[str, ...], tuple[int, int]]:
        """ """
        row, col = self._cursor_position
        new_col = self._tab_length * (col // self._tab_length) + self._tab_length
        N_spaces = new_col - col
        new_text = (
            self._raw_text[:row]
            + [self._raw_text[row][:col] + " " * N_spaces + self._raw_text[row][col:]]
            + self._raw_text[row + 1 :]
        )

        new_cursor_position = (row, new_col)

        return new_text, new_cursor_position

    def _process_key(self, key):
        """
        Takes the current text and modifies it using the given key input.
        """
        call = True
        match key:
            case "Backspace":
                self._raw_text, self._cursor_position = self._key_backspace()
            case "Delete":
                self._raw_text = self._key_delete()
            case "Space":
                self._raw_text, self._cursor_position = self._key_char(" ")
            case "Enter":
                self._raw_text, self._cursor_position = self._key_enter()
            case "Left":
                self._cursor_position = self._key_arrow_left()
            case "Right":
                self._cursor_position = self._key_arrow_right()
            case "Up":
                self._cursor_position = self._key_arrow_up()
            case "Down":
                self._cursor_position = self._key_arrow_down()
            case "Ctrl-Left":
                self._cursor_position = self._key_ctrl_left()
            case "Ctrl-Right":
                self._cursor_position = self._key_ctrl_right()
            case "Home":
                self._cursor_position = self._key_home()
            case "End":
                self._cursor_position = self._key_end()
            case "Tab":
                self._raw_text, self._cursor_position = self._key_tab()
            case other:
                if len(key) == 1:
                    self._raw_text, self._cursor_position = self._key_char(key)
                else:
                    call = False

        if call:
            self.__call__(self._raw_text)

    def _set_view(self) -> None:
        """
        Backend for method `set_view`.
        """
        super()._set_view()
        row, col = self._cursor_position
        cursor_abs_position = (
            row + self._row_start,
            col + self._column_start,
        )
        self._term.cursor_move(*cursor_abs_position, flush=True)

    def start(self):
        """
        Main loop which runs on one thread, while a listener runs on another and provides commands to be read by
        this method.

        These inputs are accessed via the superclass attribute `LiveMenu._input_state` and are processed in an
        infinite loop until broken.
        """
        super().start()
        self._raw_text = self._text
        getch_iterator = Listener.getch_iterator()
        for key in getch_iterator:
            self._process_key(key)
