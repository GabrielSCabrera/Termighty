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
        wrap_text: bool = False,
        show_line_numbers: bool = False,
        background: Union[str, Color, tuple[int, int, int]] = None,
        foreground: Union[str, Color, tuple[int, int, int]] = None,
        style: Optional[str] = None,
        select_background: Union[str, Color, tuple[int, int, int]] = None,
        select_foreground: Union[str, Color, tuple[int, int, int]] = None,
        select_style: Optional[str] = None,
        cursor_position: Optional[tuple[int, int]] = None,
        vertical_scroll_buffer: Optional[int] = None,
        horizontal_scroll_buffer: Optional[int] = None,
    ):
        """
        Creates an instance of WordProcessor, and initializes its attributes and those of its inherited `TextBox`.
        """
        # Set the default position of the cursor.
        if cursor_position is None:
            cursor_position = (0, 0)
        self._cursor_position = cursor_position
        # To keep track of changes to the cursor position, store the previous position (updated by method `_set_view`).
        self._prev_cursor_position = self._cursor_position
        # Whether the text should wrap to the next line if a line exceeds the width of the underlying TextBox.
        self._wrap_text = wrap_text
        # Whether line numbers should be displayed on the left side of the text.
        self._line_numbers = show_line_numbers
        # Whether the WordProcessor should be locked and all inputs ignored.
        self._frozen = False

        super().__init__(row_start, column_start, row_end, column_end, background, foreground, style)

        # If the background color of selected text is not explicitly given, uses the negative of the TextBox background.
        if select_background is None:
            select_background = self._background.negative()

        # If the foreground color of selected text is not explicitly given, uses the negative of the TextBox foreground.
        if select_foreground is None:
            select_foreground = self._foreground.negative()

        # Confirming that the style, background color, and foreground color of selected text are valid.
        select_background, select_foreground, select_style = self._check_arguments(
            select_background, select_foreground, select_style
        )

        self._select_background = select_background
        self._select_foreground = select_foreground
        self._select_style = select_style

        # If the scroll buffer values are not explicitely defined, changes as the terminal is resized.
        self._dynamic_scroll_buffer = (vertical_scroll_buffer is None, horizontal_scroll_buffer is None)
        # Distances to the TextBox edges before scrolling is initiated (vertical, horizontal).
        self._scroll_buffer = (vertical_scroll_buffer, horizontal_scroll_buffer)

        # Set the initial dynamic scroll buffers values.
        self._set_scroll_buffer()


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

    def _set_scroll_buffer(self) -> None:
        """
        If the vertical and/or horizontal scroll buffers are dynamic, changes them based on the current terminal
        dimensions.
        """
        scroll_buffer = [self._scroll_buffer[0], self._scroll_buffer[1]]

        # How close (in rows) the cursor must get to the top or bottom of the TextBox before scrolling vertically.
        if self._dynamic_scroll_buffer[0]:
            scroll_buffer[0] = max(self._shape[0] // 10, 2)

        # How close (in columns) the cursor must get to the left or right TextBox edge before scrolling horizontally.
        if self._dynamic_scroll_buffer[1]:
            scroll_buffer[1] = max(self._shape[1] // 10, 4)

        self._scroll_buffer = (scroll_buffer[0], scroll_buffer[1])

    def _set_view(self) -> None:
        """
        Backend for method `set_view`.
        """
        row, col = self._cursor_position
        row_prev, col_prev = self._prev_cursor_position

        if row_prev != row:
            self._origin = (self._origin[0], 0)

        cursor_position = (
            row + self._row_start - self._origin[0],
            col + self._column_start - self._origin[1],
        )

        self._set_scroll_buffer()

        if not self._wrap_text:
            # Vertically scrolls the view of the text based on the cursor position.
            if (diff := cursor_position[0] - self._shape[0] + self._scroll_buffer[0]) >= 0:
                self._origin = (self._origin[0] + diff, self._origin[1])
            elif (diff := cursor_position[0] - self._scroll_buffer[0]) < 0:
                self._origin = (max(0, self._origin[0] + diff), self._origin[1])

            # Horizontally scrolls the view of the text based on the cursor position.
            if (diff := cursor_position[1] - self._shape[1] + self._scroll_buffer[1]) >= 0:
                self._origin = (self._origin[0], self._origin[1] + diff)
            elif (diff := cursor_position[1] - self._scroll_buffer[1]) < 0:
                self._origin = (self._origin[0], max(0, self._origin[1] + diff))

            cursor_position = (
                row + self._row_start - self._origin[0],
                col + self._column_start - self._origin[1],
            )

        self._prev_cursor_position = self._cursor_position
        self._term.cursor_move(*cursor_position, flush=True)
        super()._set_view()

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
        """
        Freeze the WordProcessor -- the `getch_iterator` in method `_run_getch_thread` will continue to run, but it will
        not act on the inputs and leave the window unchanged.
        """
        self._frozen = True

    def unfreeze(self):
        """
        Unfreeze the WordProcessor and reopen it to getch inputs.
        """
        self._frozen = False
