import collections.abc
import numpy as np
import string

from termutils.obj.color import Color
from termutils.settings.config import Config
from termutils.settings.data import Data
from termutils.settings.system import System
from termutils.utils.term import Term

import threading
import time

from typing import Optional, Union


class TextBox:

    """
    Base class for rectangular shapes (that may or may not contain text) that display on the terminal. Used to simplify
    & standardize more complex objects.
    """

    """CONSTRUCTOR"""

    def __init__(
        self,
        row_start: int,
        column_start: int,
        row_end: int,
        column_end: int,
        background: Optional[Union[str, Color]] = None,
        foreground: Optional[Union[str, Color]] = None,
        style: Optional[str] = None,
    ):
        """
        Returns a new instance of class `TextBox` at the specified coordinates.  If negative coordinates are given, they
        will be set dynamically relative to the size of the terminal; a thread will loop in the background keeping
        track of the terminal dimensions and resizing the text box if its coordinates are dynamic.
        """
        self._term = Term()

        self._ref_row_start = row_start
        self._ref_column_start = column_start
        self._ref_row_end = row_end
        self._ref_column_end = column_end

        # Text alignment set to "left" by default. "right" and "center" are other alternatives.
        self._align = "left"

        # Terminal dimensions (rows, columns).
        self._terminal_size = System.terminal_size

        self._set_shape()

        background, foreground, style = self._check_arguments(background, foreground, style)

        self._init_attributes(row_start, column_start, row_end, column_end, background, foreground, style)

        self._active = False
        self._new_view = False

    """MAGIC METHODS"""

    def __call__(self, text: Union[str, list[str, ...]]) -> None:
        """
        Modifies the current state of the TextBox by replacing its contents with the given lines of text.
        """
        if isinstance(text, str):
            text = [text]
        elif not isinstance(text, list) and any(not isinstance(i, str) for i in text):
            msg: str = (
                f"\n\nArgument `text` in calling of {self._type} instance must be a list containing <class 'str'>."
            )
            System.kill_all = True
            raise TypeError(msg)

        self._text = text
        self._text_prep()
        self._set_view()

    def _text_prep(self):
        """ """
        rows = len(self._text)
        columns = max(len(row) for row in self._text)

        if self._align == "left":
            pad_char = "<"
        elif self._align == "right":
            pad_char = ">"
        elif self._align == "center":
            pad_char = "^"

        vertical_pad = [" " * (columns + 2 * self._shape[1])] * self._shape[0]
        text = [f"{line:{pad_char}{self._shape[1]}s}" for line in self._text]
        text = [line.ljust(columns + self._shape[1]) for line in text]
        text = [line.rjust(columns + 2 * self._shape[1]) for line in text]
        text = vertical_pad + text + vertical_pad

        self._text_grid = np.array([list(row) for row in text])
        self._text_shape: tuple[int, int] = self._text_grid.shape
        self._text_size: int = self._text_grid.size

    """PRIVATE METHODS"""

    def _init_attributes(
        self,
        row_start: int,
        column_start: int,
        row_end: int,
        column_end: int,
        background: Color,
        foreground: Color,
        style: str,
    ):
        """ """
        self._background = background
        self._foreground = foreground
        self._style = style

        self._back_fmt: str = "48;2;{};{};{}".format(*self._background._rgb)
        self._fore_fmt: str = "38;2;{};{};{}".format(*self._foreground._rgb)
        self._style_fmt: str = f"{Data.styles[self._style.lower()]};"

        self.ANSI_format: str = f"\033[{self._style_fmt}{self._fore_fmt};{self._back_fmt}m"

        self._position = (0, 0)

    def _check_arguments(
        self,
        background: Union[str, Color, tuple[int, int, int]],
        foreground: Union[str, Color, tuple[int, int, int]],
        style: str,
        argnames: tuple[str, str, str] = ("background", "foreground", "style"),
    ) -> tuple[Color, Color, str]:
        """
        Perform checks making sure that the initialization arguments are correctly set up.
        """
        self._cls_name: str = self.__class__.__name__
        self._type: str = f"<class '{self._cls_name}'>"

        for i, j in zip(self._shape, (("row_end", "row_start"), ("column_end", "column_start"))):
            if i <= 0:
                msg: str = (
                    f"\n\nArgument `{j[0]}` must be larger than argument `{j[1]}` in the instantiation of {self._type}."
                )
                System.kill_all = True
                raise ValueError(msg)

        color_error_msg: str = (
            f"\n\nArgument `{{}}` in instantiation of {self._type} is invalid! Cannot recognize the  user-provided "
            f"color: `{{}}` -- valid options are:\n"
            f"\n* The name of a known color (<class 'str'>) -- hint: print `termutils.Color.list_colors()`,"
            f"\n* A sequence containing 3 integers in range [0, 255],"
            f"\n* An instance of <class 'Color'>.\n"
        )

        if background is None:
            background: Color = Config.background_color
        if isinstance(background, str):
            background: Color = Color.palette(background)
        elif (
            isinstance(background, collections.abc.Sequence)
            and len(background) == 3
            and all([(0 <= i <= 255 and isinstance(i, int)) for i in background])
        ):
            background: Color = Color(*background)
        elif not isinstance(background, Color):
            color_error_msg.format(argnames[0], background)
            System.kill_all = True
            raise ValueError(color_error_msg)

        if foreground is None:
            foreground: Color = Config.foreground_color
        if isinstance(foreground, str):
            foreground: Color = Color.palette(foreground)
        elif (
            isinstance(foreground, collections.abc.Sequence)
            and len(foreground) == 3
            and all([(0 <= i <= 255 and isinstance(i, int)) for i in foreground])
        ):
            foreground: Color = Color(*foreground)
        elif not isinstance(foreground, Color):
            color_error_msg.format(argnames[1], foreground)
            System.kill_all = True
            raise ValueError(color_error_msg)

        if style is None:
            style: str = Config.style
        elif style.lower() not in Data.styles.keys():
            styles_str: str = ", ".join(Data.styles.keys())
            msg: str = (
                f"\n\nArgument `{argnames[2]}` received an unknown option `{style}` in constructor for {self._type}. "
                f"Use one of the following styles: {styles_str}.\n"
            )
            System.kill_all = True
            raise ValueError(msg)

        return background, foreground, style

    def _run_thread(self, dt: float) -> None:
        """
        Keeps updating the window every set number of seconds (given by `dt`) and accounts for changes in the terminal
        size (useful when dealing with relative coordinates on initializiation).
        """
        self._active = True
        while self._active and not System.kill_all:
            if self._terminal_size != (terminal_size := System.terminal_size):
                self._terminal_size = terminal_size
                # Repeat the reset process three times in order to account for lag in the terminal as it is resized.
                # Two iterations usually is enough, but three seems to always prevent issues.
                for i in range(3):
                    time.sleep(0.01)
                    self._set_shape()
                    self._set_view()
                    self._text_prep()

            if self._new_view:
                self._new_view: bool = False
                self.write()
            time.sleep(dt)

    def _set_shape(self) -> None:
        """
        Sets the size of the text box to those given by the user at instantiation.  If the terminal size is smaller than
        the text box size, will decrease the text box size to make it fit in the terminal.  Also accounts for negative
        size instantiation values; if a value is negative, it is subtracted from the terminal size (from the axis in
        question).
        """
        self._row_start = self._ref_row_start
        self._column_start = self._ref_column_start
        self._row_end = self._ref_row_end
        self._column_end = self._ref_column_end

        if self._row_start < 0:
            self._row_start = self._terminal_size[0] + self._row_start + 1

        if self._row_end < 0:
            self._row_end = self._terminal_size[0] + self._row_end + 1

        if self._column_start < 0:
            self._column_start = self._terminal_size[1] + self._column_start + 1

        if self._column_end < 0:
            self._column_end = self._terminal_size[1] + self._column_end + 1

        self._shape: tuple[int, int] = (self._row_end - self._row_start, self._column_end - self._column_start)
        self._size: int = self._shape[0] * self._shape[1]

    def _set_view(self) -> None:
        """
        Backend for method `set_view`.
        """
        row = max(min(self._position[0] + self._shape[0], self._text_shape[0]), 0)
        column = max(min(self._position[1] + self._shape[1], self._text_shape[1]), 0)
        self._view: np.ndarray = self._text_grid[row : row + self._shape[0], column : column + self._shape[1]]
        self._new_view: bool = True

    """PUBLIC METHODS"""

    def align(self, mode: str) -> None:
        """
        Set the TextBox text alignment mode.  Set to "left" by default, but can also be set to "right" or "center".
        """
        if (mode := mode.lower()) not in ["left", "right", "center"]:
            error_message = (
                f'Invalid text alignment option selected in TextBox method `align`.  Valid options are "left", '
                f'"right", or "center".'
            )
            System.kill_all = True
            raise ValueError(error_message)

        self._align = mode

    def start(self, dt: float = 0.005):
        """
        Activates a thread that runs the method self._run_thread.
        """
        self._thread = threading.Thread(target=self._run_thread, args=(dt,), daemon=False)
        self._thread.start()

    def stop(self) -> None:
        """ """
        self._active = False
        self._thread.join()

    def scroll_down(self, rows: int = 1) -> None:
        """
        Scrolls the current view down by the designated number of rows.
        """
        self._position: tuple[int, int] = (self._view[0] + rows, self._view[1])
        self._set_view()

    def scroll_left(self, columns: int = 1) -> None:
        """
        Scrolls the current view left by the designated number of columns.
        """
        self._position: tuple[int, int] = (self._view[0], self._view[1] - columns)
        self._set_view()

    def scroll_right(self, columns: int = 1) -> None:
        """
        Scrolls the current view right by the designated number of columns.
        """
        self._position: tuple[int, int] = (self._view[0], self._view[1] + columns)
        self._set_view()

    def scroll_up(self, rows: int = 1) -> None:
        """
        Scrolls the current view up by the designated number of rows.
        """
        self._position: tuple[int, int] = (self._view[0] - rows, self._view[1])
        self._set_view()

    def set_view(self, row: int, column: int) -> None:
        """
        Sets the current view on the text to the given coordinates. For example, given a TextBox with shape
        (rows=1, columns=10) the string

                        "We're no strangers to love\nYou know the rules and so do I"

        would by default only display: "We're no s".  By default, the view is set to (row=0, column=0), the values
        representing the upper left part of the view into the text.

        If we were to run set_view(row=0, column=10), then the TextBox would instead display "trangers t". Or if we run
        set_view(row=1, column=15), we would get "les and so".

        The view may exceed the text's boundary, as it is automatically padded.
        """
        self._position = (row, column)
        self._set_view()

    def write(self) -> None:
        """
        Writes the text to its designated coordinates with the view taken into account.
        """
        # Saving the cursor position
        self._term.cursor_save()
        for m, line in enumerate(self._view):
            row = self._row_start + m
            for n, char in enumerate(line):
                column = self._column_start + n
                char = f"{self.ANSI_format}{char}\033[m"
                self._term.write_at(row, column, char)
        # Restoring the cursor position
        self._term.cursor_load()
        # Flushing the results to the terminal
        self._term.flush()
