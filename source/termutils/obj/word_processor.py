from termutils.obj.text_box import TextBox
from termutils.obj.color import Color
from termutils.obj.listener import Listener
import textwrap
import time

from typing import Optional, Union


class WordProcessor(TextBox):
    """
    A subclass of `TextBox` that uses class `Listener` to detect keyboard inputs, and emulate a fully-functional word
    processor.  Supported advanced functions include:

        Cursor positioning with the arrow keys,
        Ctrl-arrow key to move the cursor to the beginning/end of words,
        Alt-arrow to select text,
        Deletion of selected text,
        Copying of selected text.
    """

    def __init__(
        self,
        row_start: int,
        column_start: int,
        row_end: int,
        column_end: int,
        wrap_text: bool = True,
        show_line_numbers: bool = False,
        background: Optional[Union[str, Color]] = None,
        foreground: Optional[Union[str, Color]] = None,
        style: Optional[str] = None,
    ):
        """
        Creates an instance of TextEditor.  Supports usage of the default listener provided by class LiveMenu.
        """
        super().__init__(row_start, column_start, row_end, column_end, background, foreground, style)
        self._cursor_position = (0, 0)
        self._wrap_text = wrap_text
        self._line_numbers = show_line_numbers

    def __call__(self, text: str) -> None:
        """
        Force the text box to display whatever string is passed into argument `text`.
        """
        self._raw_text = text
        super().__call__(text)

    def _delete(self) -> tuple[list[str, ...], tuple[int, int]]:
        """
        Performs a delete on the given list of characters, using the context attached to them (see docstring in
        self._process_key).
        """

    def _ctrl_delete(self) -> tuple[list[str, ...], tuple[int, int]]:
        """
        Performs a ctrl-delete on the given list of characters, using the context attached to them (see docstring in
        self._process_key).
        """

    def _backspace(self) -> tuple[list[str, ...], tuple[int, int]]:
        """
        Performs a backspace on the given list of characters, using the context attached to them (see docstring in
        self._process_key).
        """
        # If the cursor is at position (0,0), backspace has no effect, so make no changes to the text.
        if self._cursor_position == (0, 0):
            return self._raw_text, (0, 0)
        # If the cursor is at position (N,0), backspace appends line N to line N-1.
        elif self._cursor_position[1] == 0:
            new_text = [self._raw_text[self._cursor_position[0] - 1] + self._raw_text[self._cursor_position[0]]]
            if self._cursor_position[0] > 1:
                new_text = self._raw_text[: self._cursor_position[0] - 1] + new_text
            new_cursor_position = (self._cursor_position[0] - 1, len(self._raw_text[self._cursor_position[0]]))
        # If the cursor is at position (M,N), backspace removes character (M,N-1).
        else:
            new_text = [
                self._raw_text[self._cursor_position[0]][: self._cursor_position[1] - 1]
                + self._raw_text[self._cursor_position[0]][self._cursor_position[1] :]
            ]
            if self._cursor_position[0] > 0:
                new_text = self._raw_text[: self._cursor_position[0]] + new_text
            new_cursor_position = (self._cursor_position[0], self._cursor_position[1] - 1)

        if self._cursor_position[0] < len(self._raw_text) - 1:
            new_text += self._raw_text[self._cursor_position[0] + 1 :]

        return new_text, new_cursor_position

    def _ctrl_backspace(self) -> tuple[list[str, ...], tuple[int, int]]:
        """
        Performs a ctrl-backspace on the given list of characters, using the context attached to them (see docstring in
        self._process_key).
        """

    def _ctrl_left(self) -> tuple[list[str, ...], tuple[int, int]]:
        """
        Moves the cursor to the left until the beginning of the previous word is reached.
        """

    def _ctrl_right(self) -> tuple[list[str, ...], tuple[int, int]]:
        """
        Moves the cursor to the right until the end of the current word is reached.
        """

    def _ctrl_up(self) -> tuple[list[str, ...], tuple[int, int]]:
        """
        Swaps the above line with the current one.
        """

    def _ctrl_down(self) -> tuple[list[str, ...], tuple[int, int]]:
        """
        Swaps the below line with the current one.
        """

    def _process_key(self, key):
        """
        Takes the current text and modifies it using the given key input.
        """
        if key == "Backspace":
            text = self._backspace()

        self.__call__(text)

    def start(self):
        """
        Main loop which runs on one thread, while a listener runs on another and provides commands to be read by
        this method.

        These inputs are accessed via the superclass attribute `LiveMenu._input_state` and are processed in an
        infinite loop until broken.
        """
        getch_iterator = Threading.getch_iterator()
        for key in getch_iterator:
            self._process_key(key)
