from typing import Optional, Union

import numpy as np

from termutils.data import Data
from termutils.utils import text as textutils
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
        y0: int,
        x0: int,
        y1: int,
        x1: int,
        background: Optional[Union[str, Color]] = None,
        foreground: Optional[Union[str, Color]] = None,
        style: Optional[str] = None,
    ):
        """
        Returns a new instance of class `Widget`.  Shouldn't normally be instantiated directly, but inherited.
        """
        # `Widget`, or the name of the subclass that inherits `Widget`.
        self._cls_name: str = self.__class__.__name__
        self._type: str = f"<class '{self._cls_name}'>"

        for i, j in zip((y1, y0, x1, x0), ("y1", "y0", "x1", "x0")):
            if i != int(i) or i < 0:
                msg: str = f"\n\nArgument `{j}` in the instantiation of {self._type} must be a positive integer."
                raise ValueError(msg)

        self._y0: int = y0
        self._y1: int = y1
        self._x0: int = x0
        self._x1: int = x1

        self._size: int = (y1 - y0) * (x1 - x0)
        self._shape: tuple[int, int] = (y1 - y0, x1 - x0)

        for i, j in zip(self._shape, (("y1", "y0"), ("x1", "x0"))):
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
        self._back_fmt: str = "48;2;{};{};{}".format(*background._rgb)

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
        self._fore_fmt: str = "38;2;{};{};{}".format(*foreground._rgb)

        if style is None:
            style: str = defaults.style
        elif style.lower() not in Data.styles.keys():
            styles_str: str = ", ".join(Data.styles.keys())
            msg: str = (
                f"\n\nArgument `style` received an unknown option `{style}` in constructor for {self._type}.  Use one "
                f"of the following styles: {styles_str}.\n"
            )
            raise ValueError(msg)

        self._style_fmt: str = f"{Data.styles[style.lower()]};"
        self._style: str = style

        self.ANSI_format: str = f"\033[{self._style_fmt}{self._fore_fmt};{self._back_fmt}m"

        row_idx: np.ndarray = np.arange(0, self._shape[0], 1, dtype=np.int64)
        column_idx: np.ndarray = np.arange(0, self._shape[1], 1, dtype=np.int64)
        Y, X = np.meshgrid(row_idx, column_idx)
        Y, X = Y[:, :, np.newaxis], X[:, :, np.newaxis]
        self._indices: np.ndarray = np.concatenate([X, Y], axis=2)

        self.__call__("")

    """MAGIC METHODS"""

    def __call__(self, text: str, fmt_spec: str = "<") -> None:
        """
        Sets the current state of the widget to the given text.
        """
        if not isinstance(text, str):
            msg: str = f"\n\nAttribute `text` in calling of {self._type} instance must be of <class 'str'>."
            raise TypeError(msg)

        rows: list = []
        split_text: list[str, ...] = text.split("\n")
        max_len: int = max(len(line) for line in split_text)
        max_len: int = max(self._shape[1], max_len)

        if fmt_spec == "c":
            for i in split_text:
                row: str = f"{i:^{self._shape[1]}}"
                rows.append(f"{row:<{max_len}}")
        else:
            for i in split_text:
                rows.append(f"{i:{fmt_spec}{max_len}}")

            for _ in range(self._shape[0] - len(rows)):
                rows.append(f"{' ':{fmt_spec}{max_len}}")

        self._text: str = text
        self._rows: list[str, ...] = rows
        self._text_shape: tuple[int, int] = (len(rows), max_len)
        self._text_size: int = len(rows) * max_len

        self._view: np.ndarray = np.zeros(2, dtype=np.int64)

        row_idx: np.ndarray = np.arange(0, self._text_shape[0], 1, dtype=np.int64)
        column_idx: np.ndarray = np.arange(0, self._text_shape[1], 1, dtype=np.int64)
        Y, X = np.meshgrid(row_idx, column_idx)
        Y, X = Y[:, :, np.newaxis], X[:, :, np.newaxis]
        self._text_indices: np.ndarray = np.concatenate([X, Y], axis=2)

    """PROPERTIES"""

    @property
    def lines(self) -> list[list[str, ...], ...]:
        """
        Returns the current view of the text: this is dependent on the text dimensions and shape of the widget, as well
        as the current view state.

        The returned list will contain equidistant strings, each exactly as long as the widget's width.
        """
        return self._lines

    """PRIVATE METHODS"""

    def _set_view(self, row: int, column: int) -> None:
        """
        Backend for method `set_view`.
        """
        row: int = max(0, min(row, max(0, self._text_shape[0] - self._shape[0]-1)))
        column: int = max(0, min(column, max(0, self._text_shape[1] - self._shape[1]-1)))
        self._view: np.ndarray = self._text_indices[row, column]

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
        self._set_view(row=row, column=column)

    def write(self, ellipsis: bool = False) -> None:
        """
        Writes the string to its designated coordinates with the view taken
        into account.
        """
        # Saving the cursor position
        print("\0337", end="")

        row_start: int = self._view[0]
        row_stop: int = self._view[0] + self._shape[0]
        column_start: int = self._view[1]
        column_stop: int = self._view[1] + self._shape[1]

        for i, row_idx in enumerate(range(row_start, row_stop)):
            textutils.cursor_to(self._y0 + i, self._x0)
            if ellipsis:
                row: str = self._rows[row_idx]
                if row[column_stop:].strip() != "":
                    row: str = row[column_start : column_stop - 1] + "…"
                else:
                    row: str = row[column_start:column_stop]
                row: str = f"{self.ANSI_format}{row}\033[m"
                print(row, end="", flush=True)
            else:
                row: str = f"{self.ANSI_format}{self._rows[row_idx][column_start:column_stop]}\033[m"
                print(row, end="", flush=True)

        # Restoring the cursor position
        print("\0338", end="")
