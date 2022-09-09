from termutils.obj.color import Color
from termutils.widgets.text_box import TextBox
from termutils.settings.system import System
from termutils.utils.listener import Listener
from termutils.utils.key_processor import KeyProcessor
from termutils.utils.term import Term

import textwrap
import threading
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
        self._frozen = False

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

    def _run_getch_thread(self) -> None:
        """
        Keeps updating the window every set number of seconds (given by `dt`) and accounts for changes in the terminal
        size (useful when dealing with relative coordinates on initializiation).
        """
        self._raw_text = self._text
        getch_iterator = Listener.getch_iterator()

        for key in getch_iterator:
            if not self._frozen:
                call, self._raw_text, self._cursor_position = KeyProcessor.process_key(
                    raw_text=self._raw_text, cursor_position=self._cursor_position, key=key
                )
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
        self.__call__(self._text)
        self._thread = threading.Thread(target=self._run_getch_thread, daemon=False)
        self._thread.start()

    def freeze(self):
        """ """
        self._frozen = True

    def unfreeze(self):
        """ """
        self._frozen = False
