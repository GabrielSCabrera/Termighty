from typing import Optional, Union

import numpy as np
import string

from termutils.data import Data
from termutils.obj.term import Term
from termutils.obj.color import Color
from termutils.config import defaults


class Widget:

    """
    Base class for rectangular shapes (that may or may not contain text) that display on the terminal. Used to simplify
    & standardize more complex objects. Should normally be inherited.
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
        Returns a new instance of class `Widget`.  Shouldn't normally be instantiated directly, but inherited.
        """
        # `Widget`, or the name of the subclass that inherits `Widget`.

        self._size: int = (row_end - row_start) * (column_end - column_start)
        self._shape: tuple[int, int] = (row_end - row_start, column_end - column_start)

        background, foreground, style = self._check_arguments(background, foreground, style)

        self._init_attributes(row_start, column_start, row_end, column_end, background, foreground, style)

        self.__call__("")


    """MAGIC METHODS"""

    def __call__(self, text: str) -> None:
        """
        Modifies the current state of the widget by replacing its contents with the given text.
        """
        if not isinstance(text, str):
            msg: str = f"\n\nArgument `text` in calling of {self._type} instance must be of <class 'str'>."
            raise TypeError(msg)

        text:list[str,...] = text.split("\n")
        text:list[str,...] = [row.strip() for row in text]
        if self._wrap:
            pass
        self._text_prep(text)
        self.set_view(0,0)

    def _text_prep(self, text: list[str, ...], align="left"):
        """ """
        rows = len(text)
        columns = max(len(row) for row in text)

        if align == "left":
            pad_char = "<"
        elif align == "right":
            pad_char = ">"
        elif align == "center":
            pad_char = "^"

        text = [f"{line:{pad_char}{columns}}" for line in text]
        text = [line.ljust(columns + self._shape[1]) for line in text]
        vert_pad = [" "*(columns + self._shape[1])]*self._shape[0]
        text = text + vert_pad

        self._text_grid = np.array([list(row) for row in text])
        self._text_shape: tuple[int, int] = (rows, columns)
        self._text_size: int = rows*columns

    def wrap():
        """ """
        self._wrap = True

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
        self._wrap = False

        self._row_start: int = row_start
        self._row_end: int = row_end
        self._column_start: int = column_start
        self._column_end: int = column_end

        self._back_fmt: str = "48;2;{};{};{}".format(*background._rgb)
        self._fore_fmt: str = "38;2;{};{};{}".format(*foreground._rgb)

        self._style_fmt: str = f"{Data.styles[style.lower()]};"
        self._style: str = style

        self.ANSI_format: str = f"\033[{self._style_fmt}{self._fore_fmt};{self._back_fmt}m"

        row_idx: np.ndarray = np.arange(0, self._shape[0], 1, dtype=np.int64)
        column_idx: np.ndarray = np.arange(0, self._shape[1], 1, dtype=np.int64)
        Y, X = np.meshgrid(column_idx, row_idx)
        Y, X = Y[:, :, np.newaxis], X[:, :, np.newaxis]
        self._indices: np.ndarray = np.concatenate([X, Y], axis=2)

    def _check_arguments(
        self, background: Union[str, Color], foreground: Union[str, Color], style: str
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
                raise ValueError(msg)

        if background is None:
            background: Color = defaults.background_color
        if isinstance(background, str):
            background: Color = Color.palette(background)
        elif isinstance(background, (tuple, list, np.ndarray)):
            background: Color = Color(background)
        elif not isinstance(background, Color):
            msg: str = (
                f"\n\nArgument `background` in instantiation of {self._type} must be a valid color as an instance of "
                f"<class 'str'>, or an instance of <class 'Color'>.\n\nCannot recognize the user-provided color: "
                f"`{background}`."
            )
            raise ValueError(msg)

        if foreground is None:
            foreground: Color = defaults.foreground_color
        if isinstance(foreground, str):
            foreground: Color = Color.palette(foreground)
        elif isinstance(foreground, (tuple, list, np.ndarray)):
            foreground: Color = Color(foreground)
        elif not isinstance(foreground, Color):
            msg: str = (
                f"\n\nArgument `foreground` in instantiation of {self._type} must be a valid color as an instance of "
                f"<class 'str'>, or an instance of <class 'Color'>.\n\nCannot recognize the user-provided color: "
                f"`{foreground}`."
            )
            raise ValueError(msg)

        if style is None:
            style: str = defaults.style
        elif style.lower() not in Data.styles.keys():
            styles_str: str = ", ".join(Data.styles.keys())
            msg: str = (
                f"\n\nArgument `style` received an unknown option `{style}` in constructor for {self._type}.  Use one "
                f"of the following styles: {styles_str}.\n"
            )
            raise ValueError(msg)

        return background, foreground, style

    def _set_view(self) -> None:
        """
        Backend for method `set_view`.
        """
        row=min(self._origin[0], self._text_shape[0])
        column=min(self._origin[1], self._text_shape[1])
        self._view: np.ndarray = self._text_grid[row:row+self._shape[0], column:column+self._shape[1]]

    """PUBLIC METHODS"""

    def scroll_down(self, rows: int = 1) -> None:
        """
        Scrolls the current view down by the designated number of rows.
        """
        self._set_view(row=self._view[0] + rows, column=self._view[1])

    def scroll_left(self, columns: int = 1) -> None:
        """
        Scrolls the current view left by the designated number of columns.
        """
        self._set_view(row=self._view[0], column=self._view[1] - columns)

    def scroll_right(self, columns: int = 1) -> None:
        """
        Scrolls the current view right by the designated number of columns.
        """
        self._set_view(row=self._view[0], column=self._view[1] + columns)

    def scroll_up(self, rows: int = 1) -> None:
        """
        Scrolls the current view up by the designated number of rows.
        """
        self._set_view(row=self._view[0] - rows, column=self._view[1])

    def set_view(self, row: int, column: int) -> None:
        """
        Sets the current view on the text to the given coordinates. For example, given a widget with shape
        (rows=1, columns=10) the string

                        "We're no strangers to love\nYou know the rules and so do I"

        would by default only display: "We're no s".  By default, the view is set to (row=0, column=0), the values
        representing the upper left part of the view into the text.

        If we were to run set_view(row=0, column=10), then the widget would instead display "trangers t". Or if we run
        set_view(row=1, column=-15), we would get "les and so".

        Locks the view such that it never exceeds the text's total boundary.
        """
        for i, j in zip((row, column), ("row", "column")):
            if not isinstance(i, (int, float)) or i != int(i):
                msg: str = f"\n\nAttribute `{j}` in method `set_view` of a {self._type} instance must be an integer."
                raise TypeError(msg)
        self._origin = (row, column)
        self._set_view()

    def write(self) -> None:
        """
        Writes the string to its designated coordinates with the view taken
        into account.
        """
        # Saving the cursor position
        print("\0337", end="")

        for m, line in enumerate(self._view):
            row = self._row_start + m + 1
            for n, char in enumerate(line):
                column = self._column_start + n + 1
                char = f"{self.ANSI_format}{char}\033[m"
                Term.print_at(row, column, char)

        # Restoring the cursor position
        print("\0338", end="")
