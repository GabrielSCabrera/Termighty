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
        self._cursor_position = (0,0)
        self._wrap_text = wrap_text
        self._line_numbers = show_line_numbers

    def __call__(self, text:str) -> None:
        """
        """
        super().__call__(text)

    def _delete(self):
        """
        Performs a delete on the given list of characters, using the context attached to them (see docstring in
        self._process_key).
        """

    def _ctrl_delete(self):
        """
        Performs a ctrl-delete on the given list of characters, using the context attached to them (see docstring in
        self._process_key).
        """

    def _backspace(self):
        """
        Performs a backspace on the given list of characters, using the context attached to them (see docstring in
        self._process_key).
        """

    def _ctrl_backspace(self):
        """
        Performs a ctrl-backspace on the given list of characters, using the context attached to them (see docstring in
        self._process_key).
        """

    def _ctrl_left(self):
        """
        Moves the cursor to the left until the beginning of the previous word is reached.
        """

    def _ctrl_right(self):
        """
        Moves the cursor to the right until the end of the current word is reached.
        """

    def _ctrl_up(self):
        """
        Swaps the above line with the current one.
        """

    def _ctrl_down(self):
        """
        Swaps the below line with the current one.
        """

    def _process_key(self):
        """
        Takes the current text and modifies it using the given key input.
        """


    def run(self):
        """
        Main loop which runs on one thread, while a listener runs on another and provides commands to be read by
        this method.

        These inputs are accessed via the superclass attribute `LiveMenu._input_state` and are processed in an
        infinite loop until broken.
        """
