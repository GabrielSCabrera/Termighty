import collections.abc
import numpy as np

from termighty.obj.color import Color
from termighty.settings.config import Config
from termighty.settings.data import Data
from termighty.settings.system import System
from termighty.utils.term import Term

import threading
import time
from textwrap import TextWrapper

from typing import Optional, Union, Literal


class TextBox:

    """
    Base class for rectangular shapes (that may or may not contain text) that display on the terminal. Used to simplify
    & standardize more complex objects.
    """

    """CONSTRUCTOR"""

    def __init__(
        self,
        row_start: int,
        col_start: int,
        row_end: int,
        col_end: int,
        wrap_text: bool = False,
        wrap_subsequent_indent: str = "",
        wrap_text_break_on_hyphens: bool = True,
        wrap_text_break_long_words: bool = True,
        background: Optional[Union[str, Color]] = None,
        foreground: Optional[Union[str, Color]] = None,
        style: Optional[str] = None,
        alignment: Literal["left", "right", "center"] = "left",
        view: tuple[int, int] = (0, 0),
    ):
        """
        Return a new instance of class `TextBox` at the specified coordinates.  If negative coordinates are given, they
        will be set dynamically relative to the size of the terminal; a thread will loop in the background keeping
        track of the terminal dimensions and resizing the TextBox if its coordinates are dynamic.
        """
        # Create a new instance of class Term, which is used to perform writing and cursor operations to the terminal.
        self._term: Term = Term()

        # Initialize the terminal dimension attributes.
        self._init_spacial_attributes(
            row_start=row_start, col_start=col_start, row_end=row_end, col_end=col_end, view=view
        )

        # Text alignment set to "left" by default. "right" and "center" are other alternatives.
        self._alignment: Literal["left", "right", "center"] = alignment

        self._set_shape()

        background, foreground, style = self._init_arguments(
            background=background,
            foreground=foreground,
            style=style,
            defaults=(Config.background_color, Config.foreground_color, Config.style),
            argnames=("background", "foreground", "style"),
        )

        self._init_color_attributes(background=background, foreground=foreground, style=style)

        self._active: bool = False
        self._view_changed: bool = False
        self._text: list[str, ...] = None  # [""]

        # Whether the text should wrap to the next line if a line exceeds the width of the underlying TextBox.
        self._wrap_text: bool = wrap_text
        self._wrap_subsequent_indent: str = wrap_subsequent_indent
        self._wrap_text_break_on_hyphens: bool = wrap_text_break_on_hyphens
        self._wrap_text_break_long_words: bool = wrap_text_break_long_words
        self._process_text_wrapper()

    """MAGIC METHODS"""

    def __call__(self, text: Union[str, list[str, ...]]) -> None:
        """
        Modify the current state of the TextBox by replacing its contents with the given text. Accepts a single string,
        or a list of strings -- if a list is given, will place each element in its own row within the TextBox.

        Does not support the use of strings containing ANSI escape sequences!
        """
        if isinstance(text, str):
            text: list[str, ...] = [text]
        elif not isinstance(text, list) and any(not isinstance(i, str) for i in text):
            error_message: str = (
                f"\n\nArgument `text` in calling of {self._type} instance must be a list containing <class 'str'>."
            )
            System.kill_all = True
            raise TypeError(error_message)

        self._text: list[str, ...] = text
        self._process_text()
        self._set_view()

    def _process_text(self):
        """
        Justify the raw text given to the __call__ method such that all lines of text are equally-sized, and wide enough
        to allow for the view of the text to be moved left, right, up, and down, until the text is just out of view.

        Takes the `self._alignment` attribute into account, aligning the text either to the left, right, or center of
        the TextBox.
        """
        if self._wrap_text:
            self._new_line: list[bool, ...] = [
                i == 0 for row in self._text for i in range(len(self._text_wrapper.wrap(row)))
            ]
            text: list[str, ...] = [line.strip() for row in self._text for line in self._text_wrapper.wrap(row)]
        else:
            self._new_line: list[bool] = [True for i in range(self._shape[0])]
            text: list[str, ...] = self._text

        rows: int = len(text)
        cols: int = max(len(row) for row in text) if len(text) > 0 else 0

        if self._alignment == "left":
            pad_char: str = "<"
        elif self._alignment == "right":
            pad_char: str = ">"
        elif self._alignment == "center":
            pad_char: str = "^"

        vertical_pad: list[str, ...] = [" " * (cols + 2 * self._shape[1])] * self._shape[0]
        text: list[str, ...] = [f"{line:{pad_char}{self._shape[1]}s}" for line in text]
        text: list[str, ...] = [line.ljust(cols + self._shape[1]) for line in text]
        text: list[str, ...] = [line.rjust(cols + 2 * self._shape[1]) for line in text]
        text: list[str, ...] = vertical_pad + text + vertical_pad

        vertical_pad: list[str, ...] = [False] * self._shape[0]
        new_line: list[str, ...] = vertical_pad + self._new_line + vertical_pad

        dimensions: tuple[int, int] = (2 * self._shape[0] + rows, 2 * self._shape[1] + cols)

        self._text_grid: np.ndarray = np.zeros(dimensions, dtype="<U1")
        self._text_grid: np.ndarray = np.array([list(row) for row in text])
        self._new_line_grid: np.npdarray = np.array(new_line)
        self._text_shape: tuple[int, int] = self._text_grid.shape
        self._text_size: int = self._text_grid.size

    """PRIVATE METHODS"""

    def _init_color_attributes(
        self,
        background: Color,
        foreground: Color,
        style: str,
    ):
        """
        Prepare all the required instance attributes, such as colors, style, and the resulting ANSI sequences that will
        be used to correctly display the text with these colors and styles.

        """
        self._background: Color = background
        self._foreground: Color = foreground
        self._style: Color = style

        self._back_fmt: str = "48;2;{};{};{}".format(*self._background._rgb)
        self._fore_fmt: str = "38;2;{};{};{}".format(*self._foreground._rgb)
        self._style_fmt: str = f"{Data.styles[self._style.lower()]};"

        self._ANSI_format: str = f"\033[{self._style_fmt}{self._fore_fmt};{self._back_fmt}m"

    def _init_spacial_attributes(
        self,
        row_start: int,
        col_start: int,
        row_end: int,
        col_end: int,
        view: tuple[int, int],
    ) -> None:
        """
        Initializes attributes that are related to the TextBox shape, position within the terminal, and the position of
        its contents. This includes:

        * The coordinates of the TextBox corners (user-defined),
        * The initial size of the terminal, as obtained by the System class,
        * The window view, set to (0,0) by default.
        """
        # Store the original (possibly relative) TextBox dimensions; these are used to determine the true TextBox size
        # on initialization and when the terminal changes shape.
        self._ref_row_start: int = row_start
        self._ref_col_start: int = col_start
        self._ref_row_end: int = row_end
        self._ref_col_end: int = col_end

        # Terminal dimensions in row major order (rows, cols).
        self._terminal_size: tuple[int, int] = System.terminal_size

        self._origin: tuple[int, int] = view
        self._current_output: list[str, ...] = None

    def _process_text_wrapper(self):
        self._text_wrapper = TextWrapper(
            width=self._shape[1],
            subsequent_indent=self._wrap_subsequent_indent,
            break_on_hyphens=self._wrap_text_break_on_hyphens,
            break_long_words=self._wrap_text_break_long_words,
        )

    def _init_arguments(
        self,
        background: Union[str, Color, tuple[int, int, int]],
        foreground: Union[str, Color, tuple[int, int, int]],
        style: str,
        defaults: tuple[Color, Color, str],
        argnames: tuple[str, str, str],
    ) -> tuple[Color, Color, str]:
        """
        Perform checks making sure that the initialization arguments are correctly set up.
        * Confirm that the TextBox dimensions are correctly set up (start < end),
        * Confirm that the given background & foreground colors are valid,
        * Confirm that the given style is valid.
        """
        # Get the name of the current class. Since TextBox might be inherited, makes exceptions more comprehensible.
        self._type: str = f"<class '{self.__class__.__name__}'>"

        # Check that `row_end` is greater than `row_start`, and that `col_end` is greater than `col_start`.
        for i, j in zip(self._shape, (("row_end", "row_start"), ("col_end", "col_start"))):
            if i <= 0:
                error_message: str = (
                    f"\n\nArgument `{j[0]}` must be larger than argument `{j[1]}` in the instantiation of {self._type}."
                )
                System.kill_all: bool = True
                raise ValueError(error_message)

        # Detailed exception in case an invalid color option is given. Contains string formatting curly braces so that
        # information on the specific problem is given to the user.
        color_error_message: str = (
            f"\n\nArgument `{{}}` in instantiation of {self._type} is invalid! Cannot recognize the user-provided "
            f"color: `{{}}` -- valid options are:\n"
            f"\n* The name of a known color (<class 'str'>) -- hint: print `termighty.Color.list_colors()`,"
            f"\n* A sequence containing 3 integers in range [0, 255],"
            f"\n* An instance of <class 'Color'>.\n"
        )

        # Will contain the final background and foreground colors, respectively.
        args: list = []
        # Performs the checking and processing for both the background and foreground colors.
        for arg, default, name in zip((background, foreground), defaults[:2], argnames[:2]):
            # If the arg is None, falls back to the color name in argument `default` and uses `Color.palette`.
            if arg is None:
                args.append(Color.palette(default))
            # If the arg is a string and a known color by name, uses `Color.palette`.
            elif isinstance(arg, str) and Color.is_color(arg.lower()):
                args.append(Color.palette(arg.lower()))
            # If the arg consists of a valid tuple of RGB color channels in range [0, 255], uses `Color.__init__`.
            elif (
                isinstance(arg, collections.abc.Sequence)
                and len(arg) == 3
                and all([(0 <= channel <= 255 and isinstance(channel, int)) for channel in arg])
            ):
                args.append(Color(*arg))
            # Raise a ValueError with `color_error_message` if none of the above conditions are met.
            else:
                System.kill_all = True
                raise ValueError(color_error_message.format(name, arg))

        # If no style is given, fall back to the default style given in argument `default`.
        if style is None:
            style: str = defaults[2]
        # If the style is not known, raise an exception explaining the problem and listing all valid styles.
        elif style.lower() not in Data.styles.keys():
            styles_str: str = ", ".join(Data.styles.keys())
            error_message: str = (
                f"\n\nArgument `{argnames[2]}` received an unknown option `{style}` in constructor for {self._type}. "
                f"Use one of the following styles: {styles_str}.\n"
            )
            System.kill_all = True
            raise ValueError(error_message)

        return *args, style

    def _run_thread(self, dt: float) -> None:
        """
        Keep updating the window every `dt` seconds, and account for changes in the terminal size (useful when dealing
        with relative coordinates on initialization).
        """
        self._active: bool = True
        while self._active and not System.kill_all:
            # Reformat the contents of the TextBox due to a change in terminal dimensions.
            if self._terminal_size != (terminal_size := System.terminal_size):
                self._terminal_size: tuple[int, int] = terminal_size
                # Repeat the reset process three times in order to account for lag in the terminal as it is resized.
                # Two iterations usually is enough, but three seems to always prevent issues.
                for i in range(3):
                    time.sleep(0.01)
                    self._process_text_wrapper()
                    self._set_shape()
                    self._set_view()
                    self._process_text()

            if self._view_changed:
                self._view_changed: bool = False
                self.write()
            time.sleep(dt)

    def _set_shape(self) -> None:
        """
        Set the size of the TextBox to those given by the user at instantiation.  If the terminal size is smaller than
        the TextBox size, will decrease the TextBox size to make it fit in the terminal.  Also accounts for negative
        size instantiation values; if a value is negative, it is subtracted from the terminal size (from the axis in
        question).
        """
        # If the ref. row positions are negative (i.e. relative values) subtracts them from the total terminal height.
        self._row_start: int = self._ref_row_start + (self._terminal_size[0] + 1 if self._ref_row_start < 0 else 0)
        self._row_end: int = self._ref_row_end + (self._terminal_size[0] + 1 if self._ref_row_end < 0 else 0)

        # If the ref. column positions are negative (i.e. relative values) subtracts them from the total terminal width.
        self._col_start: int = self._ref_col_start + (self._terminal_size[1] + 1 if self._ref_col_start < 0 else 0)
        self._col_end: int = self._ref_col_end + (self._terminal_size[1] + 1 if self._ref_col_end < 0 else 0)

        self._shape: tuple[int, int] = (self._row_end - self._row_start, self._col_end - self._col_start)
        self._size: int = self._shape[0] * self._shape[1]

    def _set_view(self) -> None:
        """
        Backend for method `set_view` -- limits the view to prevent out of bounds errors by using commands `min` and
        `max` with the TextBox dimensions.
        """
        row: int = max(min(self._origin[0] + self._shape[0], self._text_shape[0]), 0)
        col: int = max(min(self._origin[1] + self._shape[1], self._text_shape[1]), 0)

        self._view: np.ndarray = self._text_grid[row : row + self._shape[0], col : col + self._shape[1]]
        self._view_changed: bool = True

    """PUBLIC METHODS"""

    @property
    def alignment(self) -> str:
        """
        Returns the current alignment mode as a string.
        """
        return self._alignment

    @alignment.setter
    def alignment(self, mode: str) -> None:
        """
        Set the TextBox text alignment mode.  Set to "left" by default, but can also be set to "right" or "center".
        """
        if (mode := mode.lower()) not in ["left", "right", "center"]:
            error_message: str = (
                f'\n\nInvalid text alignment option selected in TextBox method `alignment`.  Valid options are "left", '
                f'"right", or "center".'
            )
            System.kill_all = True
            raise ValueError(error_message)

        self._alignment: str = mode

    def start(self, dt: float = 0.005):
        """
        Activate a thread that runs the method self._run_thread.
        """
        if self._text is None:
            self.__call__([""])
        self._thread: threading.Thread = threading.Thread(target=self._run_thread, args=(dt,), daemon=False)
        self._thread.start()

    def stop(self) -> None:
        """
        Kill the active thread.
        """
        self._active: bool = False
        self._thread.join()

    def set_view(self, row: Optional[int] = 0, col: Optional[int] = 0) -> None:
        """
        Set the current view on the text to the given coordinates. For example, given a TextBox with shape (rows=1,
        cols=10) the string

                        "We're no strangers to love\nYou know the rules and so do I"

        would by default only display: "We're no s".  By default, the view is set to (row=0, col=0), the values
        representing the upper left part of the view into the text.

        If we were to run set_view(row=0, col=10), then the TextBox would instead display "trangers t". Or if we run
        set_view(row=1, col=15), we would get "les and so".

        The view may exceed the text's boundary, as it is automatically padded.
        """
        self._origin: tuple[int, int] = (row, col)
        self._set_view()

    def write(self) -> None:
        """
        Write the text to its designated coordinates with the view taken into account.
        """
        # Saving the cursor position.
        self._term.cursor_save()
        # Iterate through each row of the text.
        for m, line in enumerate(self._view):
            row: int = self._row_start + m
            # Iterate through each column in the current row of the text.
            for n, char in enumerate(line):
                col: int = self._col_start + n
                char: str = f"{self._ANSI_format}{char}\033[m"
                # Write to the buffer, without flushing to the terminal.
                self._term.write(row, col, char, flush=False)
        # Restoring the cursor position.
        self._term.cursor_load()
        # Flushing the results to the terminal.  Waiting to flush improves efficienty significantly.
        self._term.flush()
