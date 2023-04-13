import numpy as np

from termighty.obj.color import Color
from termighty.settings.config import Config
from termighty.settings.data import Data
from termighty.utils.listener import Listener
from termighty.utils import KeyProcessor
from termighty.widgets.text_box import TextBox

import textwrap
import threading

from typing import Optional, Union


class TextEditor(TextBox):
    """
    A subclass of `TextBox` that uses class `Listener` to detect keyboard inputs, and emulate a fully-functional word
    processor.  Supported advanced functions include:

    * Cursor positioning with the arrow keys,
    * Ctrl-arrow key to move the cursor to the beginning/end of words,
    * Alt-arrow to select text,
    * Deletion of selected text,
    * Copying & pasting of selected text.
    """

    def __init__(
        self,
        row_start: int,
        col_start: int,
        row_end: int,
        col_end: int,
        wrap_text: bool = False,
        line_numbers: bool = False,
        background: Union[str, Color, tuple[int, int, int]] = None,
        foreground: Union[str, Color, tuple[int, int, int]] = None,
        style: Optional[str] = None,
        select_background: Union[str, Color, tuple[int, int, int]] = None,
        select_foreground: Union[str, Color, tuple[int, int, int]] = None,
        select_style: Optional[str] = None,
        line_number_background: Union[str, Color, tuple[int, int, int]] = None,
        line_number_foreground: Union[str, Color, tuple[int, int, int]] = None,
        line_number_style: Optional[str] = None,
        vertical_scroll_buffer: Optional[int] = None,
        horizontal_scroll_buffer: Optional[int] = None,
        cursor_position: tuple[int, int] = (0, 0),
        frozen: bool = False,
    ):
        """
        Creates an instance of TextEditor, and initializes its attributes and those of its inherited `TextBox`.
        """
        # Performing the initialization of the TextBox base class.
        super().__init__(
            row_start=row_start,
            col_start=col_start,
            row_end=row_end,
            col_end=col_end,
            wrap_text=wrap_text,
            background=background,
            foreground=foreground,
            style=style,
        )

        # Confirming that the style, background color, and foreground color of the selected text are valid, and
        # processing them if they are not `Color` instances.
        select_background, select_foreground, select_style = self._prep_arguments(
            background=select_background,
            foreground=select_foreground,
            style=select_style,
            defaults=(
                Config.selected_background_color,
                Config.selected_foreground_color,
                Config.selected_style,
            ),
            argnames=("select_background", "select_foreground", "select_style"),
        )

        # Confirming that the style, background color, and foreground color of the line numbers are valid, and
        # processing them if they are not `Color` instances.
        line_number_background, line_number_foreground, line_number_style = self._prep_arguments(
            background=line_number_background,
            foreground=line_number_foreground,
            style=line_number_style,
            defaults=(
                Config.line_numbers_background_color,
                Config.line_numbers_foreground_color,
                Config.line_numbers_style,
            ),
            argnames=("line_numbers_background", "line_numbers_foreground", "line_numbers_style"),
        )

        # Prepare the color and style settings for selected text.
        self._init_editor_attributes(
            cursor_position=cursor_position,
            frozen=frozen,
            line_numbers=line_numbers,
            select_background=select_background,
            select_foreground=select_foreground,
            select_style=select_style,
            line_number_background=line_number_background,
            line_number_foreground=line_number_foreground,
            line_number_style=line_number_style,
        )

        # If the scroll buffer values are not explicitely defined, changes as the terminal is resized.
        self._dynamic_scroll_buffer = (vertical_scroll_buffer is None, horizontal_scroll_buffer is None)
        # Distances to the TextBox edges before scrolling is initiated (vertical, horizontal).
        self._scroll_buffer = (vertical_scroll_buffer, horizontal_scroll_buffer)
        # Set the initial dynamic scroll buffers values.
        self._set_scroll_buffer()

    def _init_editor_attributes(
        self,
        cursor_position: tuple[int, int],
        frozen: bool,
        line_numbers: bool,
        select_background: Color,
        select_foreground: Color,
        select_style: str,
        line_number_background: Color,
        line_number_foreground: Color,
        line_number_style: str,
        selected: Optional[list[tuple[int, int], ...]] = None,
    ):
        """
        Prepare all the instance attributes for selected text, such as colors, style, and the resulting ANSI sequences
        that will be used to correctly display the text with these colors and styles.

        Also initializes the coordinate list of selected text, set to an empty list by default.
        """
        # Set the default position of the cursor to (0, 0) if not otherwise specified.
        self._cursor_position = cursor_position
        # To keep track of changes to the cursor position, store the previous position (updated by method `_set_view`).
        self._prev_cursor_position = self._cursor_position

        # Whether the TextEditor should be locked and all inputs ignored.
        self._frozen = frozen

        # Whether line numbers should be displayed on the left side of the text.
        self._line_numbers = line_numbers
        # The default minimum width of the column containing line numbers.
        self._line_numbers_width = Config.line_numbers_width

        # Saving the selected text color and style settings to instance attributes.
        self._select_background = select_background
        self._select_foreground = select_foreground
        self._select_style = select_style

        # ANSI escape sequences for the background color, foreground color, and text style of selected text.
        self._select_back_fmt: str = "48;2;{};{};{}".format(*self._select_background._rgb)
        self._select_fore_fmt: str = "38;2;{};{};{}".format(*self._select_foreground._rgb)
        self._select_style_fmt: str = f"{Data.styles[self._select_style.lower()]};"

        # The full ANSI escape sequence that combines all the above three into one statement.
        self._select_ANSI_format: str = f"\033[{self._select_style_fmt}{self._select_fore_fmt};{self._select_back_fmt}m"
        self._selected = selected if selected is not None else []

        # Saving the line number color and style settings to instance attributes.
        self._line_number_background = line_number_background
        self._line_number_foreground = line_number_foreground
        self._line_number_style = line_number_style

        # ANSI escape sequences for the background color, foreground color, and text style of the line numbers.
        self._line_number_back_fmt: str = "48;2;{};{};{}".format(*self._line_number_background._rgb)
        self._line_number_fore_fmt: str = "38;2;{};{};{}".format(*self._line_number_foreground._rgb)
        self._line_number_style_fmt: str = f"{Data.styles[self._line_number_style.lower()]};"

        # The full ANSI escape sequence that combines all the above three into one statement.
        self._line_number_ANSI_format: str = (
            f"\033[{self._line_number_style_fmt}{self._line_number_fore_fmt};{self._line_number_back_fmt}m"
        )

    def _run_getch_thread(self) -> None:
        """
        Keeps updating the window every set number of seconds (given by `dt`) and accounts for changes in the terminal
        size (useful when dealing with relative coordinates on initializiation).
        """
        self._raw_text = self._text
        getch_iterator = Listener.getch_iterator()

        self._term.cursor_show(flush=True)
        for key in getch_iterator:
            if not self._frozen:
                call, self._raw_text, self._cursor_position, self._selected = KeyProcessor.process_key(
                    raw_text=self._raw_text,
                    cursor_position=self._cursor_position,
                    selected=self._selected,
                    shape=self._shape,
                    key=key,
                )
                if call:
                    if self._wrap_text:
                        self.__call__([i for i in self._raw_text for j in textwrap.wrap(i, self._shape[1])])
                    else:
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
        """ """

        row, col = self._cursor_position
        row_prev, col_prev = self._prev_cursor_position

        if row_prev != row:
            self._origin = (self._origin[0], 0)

        cursor_position = (
            row + self._ref_row_start - self._origin[0],
            col + self._ref_col_start - self._origin[1],
        )

        self._set_scroll_buffer()

        # Number of columns reserved for displaying line numbers -- accounts for the number of lines in the text.
        if self._line_numbers:
            w = max(self._line_numbers_width, int(np.log10(len(self._text))) + 2)
        else:
            w = 0

        if self._wrap_text:
            pass
        else:

            # Vertically scrolls the view of the text based on the cursor position.
            if (diff := cursor_position[0] - self._shape[0] + self._scroll_buffer[0]) >= 0:
                self._origin = (self._origin[0] + diff, self._origin[1])
            elif (diff := cursor_position[0] - self._scroll_buffer[0]) < 0:
                self._origin = (max(0, self._origin[0] + diff - self._row_start), self._origin[1])

            # Horizontally scrolls the view of the text based on the cursor position.
            if (diff := cursor_position[1] - self._shape[1] + self._scroll_buffer[1]) >= 0:
                self._origin = (self._origin[0], self._origin[1] + diff)
            elif (diff := cursor_position[1] - self._scroll_buffer[1]) < 0:
                self._origin = (self._origin[0], max(0, self._origin[1] + diff - self._col_start))

            cursor_position = (
                row + self._row_start - self._origin[0],
                col + self._col_start - self._origin[1] + w,
            )

        self._selected_processed = [
            (position[0] + self._row_start - self._origin[0], position[1] + self._col_start - self._origin[1])
            for position in self._selected
        ]
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
        Freeze the TextEditor -- the `getch_iterator` in method `_run_getch_thread` will continue to run, but it will
        not act on the inputs and leave the window unchanged.
        """
        self._frozen = True

    def unfreeze(self):
        """
        Unfreeze the TextEditor and reopen it to getch inputs.
        """
        self._frozen = False

    def write(self) -> None:
        """
        Write the text to its designated coordinates with the view taken into account.
        """
        if self._line_numbers:
            # Number of columns reserved for displaying line numbers -- accounts for the number of lines in the text.
            w = max(self._line_numbers_width, int(np.log10(len(self._text))) + 2)
            # Checking the shape the terminal had when this method was last called.
            expected_shape = (self._view.shape[0], self._view.shape[1] + w)
        else:
            w = 0
            expected_shape = self._view.shape

        # Clearing the current_output attribute if the terminal had a different shape when last writing to the terminal.
        if self._current_output is None or self._current_output.shape != expected_shape:
            self._current_output = np.full(expected_shape, "", dtype=object)

        # Saving the cursor position, as it will move during printing.
        self._term.cursor_save()
        # Hiding the cursor, otherwise it might jump around the terminal.
        self._term.cursor_hide()

        # Iterate through each row of the text.
        for m, line in enumerate(self._view):
            row = self._row_start + m
            if self._line_numbers:
                if (number := m + 1 + self._origin[0]) <= len(self._text):
                    number = str(number) + " "
                else:
                    number = " "
                # TODO: vectorize
                # line[w:] = line[:-w]
                # line[:w] = np.array(list(f"{number:>{w}s}"), dtype=object)
                line = np.concatenate([np.array(list(f"{number:>{w}s}"), dtype=object), line[:-w]])
            # Iterate through each column in the current row of the text.
            for n, char in enumerate(line):
                col = self._col_start + n
                position = (row, col - w)
                if self._line_numbers and n < w:
                    char = f"{self._line_number_ANSI_format}{char}\033[m"
                elif position in self._selected_processed:
                    char = f"{self._select_ANSI_format}{char}\033[m"
                else:
                    char = f"{self._ANSI_format}{char}\033[m"
                # Write to the buffer, without flushing to the terminal.
                if char != self._current_output[m, n]:
                    self._term.write(row, col, char, flush=False)
                    self._current_output[m, n] = char

        # Restoring the cursor position to its intended location.
        self._term.cursor_load()
        # Restoring the cursor after all the characters will have been printed.
        self._term.cursor_show()
        # Flushing the results to the terminal.  Waiting to flush improves efficienty significantly.
        self._term.flush()
