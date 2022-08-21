from typing import Optional, Union
from textwrap import wrap

import numpy as np

from termutils.data import Data
from termutils.utils import text as textutils
from termutils.obj.color import Color
from termutils.config import defaults


class Widget:

    """
    Backend used to simplify & standardize more complex classes such as <class 'Display'>. Should normally be inherited.
    """

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
        self._cls_name = self.__class__.__name__
        self._type = f"<class '{self._cls_name}'>"

        for i, j in zip((y1, y0, x1, x0), ("y1", "y0", "x1", "x0")):
            if i != int(i) or i < 0:
                msg = f"\n\nArgument `{j}` in the instantiation of {self._type} must be a positive integer."
                raise ValueError(msg)

        self._y0 = y0
        self._y1 = y1
        self._x0 = x0
        self._x1 = x1

        self._size = (y1 - y0) * (x1 - x0)
        self._shape = (y1 - y0, x1 - x0)

        for i, j in zip(self._shape, (("y1", "y0"), ("x1", "x0"))):
            if i <= 0:
                msg = (
                    f"\n\nArgument `{j[0]}` must be larger than argument `{j[1]}` in the instantiation of {self._type}."
                )
                raise ValueError(msg)

        if background is None:
            background = defaults.background_color
        elif isinstance(background, str):
            background = Color.palette(background)
        elif isinstance(background, (tuple, list, np.ndarray)):
            background = Color(background)
        elif not isinstance(background, Color):
            msg = (
                f"\n\nArgument `background` in instantiation of {self._type} must be a valid color as an instance of "
                f"<class 'str'>, or an instance of <class 'Color'>.\n\nCannot recognize the user-provided color: "
                f"`{background}`."
            )
            raise ValueError(msg)
        self._back_fmt = "48;2;{};{};{}".format(*background._rgb)

        if foreground is None:
            foreground = defaults.foreground_color
        elif isinstance(foreground, str):
            foreground = Color.palette(foreground)
        elif isinstance(foreground, (tuple, list, np.ndarray)):
            foreground = Color(foreground)
        elif not isinstance(foreground, Color):
            msg = (
                f"\n\nArgument `foreground` in instantiation of {self._type} must be a valid color as an instance of "
                f"<class 'str'>, or an instance of <class 'Color'>.\n\nCannot recognize the user-provided color: "
                f"`{foreground}`."
            )
            raise ValueError(msg)
        self._fore_fmt = "38;2;{};{};{}".format(*foreground._rgb)

        if style is None:
            style = defaults.style
        elif style.lower() not in Data.styles.keys():
            styles_str = ", ".join(Data.styles.keys())
            msg = (
                f"\n\nArgument `style` received an unknown option `{style}` in constructor for {self._type}.  Use one "
                f"of the following styles: {styles_str}.\n"
            )
            raise ValueError(msg)

        self._style_fmt = f"{Data.styles[style.lower()]};"
        self._style = style

        self.ANSI_format = f"\033[{self._style_fmt}{self._fore_fmt};{self._back_fmt}m"

        y_idx = np.arange(0, self._shape[0], 1, dtype=np.int64)
        x_idx = np.arange(0, self._shape[1], 1, dtype=np.int64)
        Y, X = np.meshgrid(y_idx, x_idx)
        Y, X = Y[:, :, np.newaxis], X[:, :, np.newaxis]
        self._indices = np.concatenate([X, Y], axis=2)

        self.__call__("")

    # PROPERTIES
    @property
    def lines(self) -> tuple[str]:
        """
        Returns the current view of the text: this is dependent on the text dimensions and shape of the widget, as well
        as the current view state.

        The returned list will contain equidistant strings, each exactly as long as the widget's width.
        """
        return tuple(self._lines)

    # SETTERS
    def __call__(self, text: str, fmt_spec: str = "<") -> None:
        """
        Sets the current state of the widget to the given text.
        """
        if not isinstance(text, str):
            msg = f"\n\nAttribute `text` in calling of {self._type} instance must be of <class 'str'>."
            raise TypeError(msg)

        rows = []
        split_text = text.split("\n")
        max_len = max(len(line) for line in split_text)
        max_len = max(self._shape[1], max_len)

        if fmt_spec == "c":
            for i in split_text:
                row = f"{i:^{self._shape[1]}}"
                rows.append(f"{row:<{max_len}}")
        else:
            for i in split_text:
                rows.append(f"{i:{fmt_spec}{max_len}}")

        self._text = text
        self._rows = rows
        self._text_shape = (len(rows), max_len)
        self._text_size = len(rows) * max_len

        self._view = np.zeros(2, dtype=np.int64)

        y_idx = np.arange(0, self._text_shape[0], 1, dtype=np.int64)
        x_idx = np.arange(0, self._text_shape[1], 1, dtype=np.int64)
        Y, X = np.meshgrid(y_idx, x_idx)
        Y, X = Y[:, :, np.newaxis], X[:, :, np.newaxis]
        self._text_indices = np.concatenate([X, Y], axis=2)

    def set_view(self, y: int, x: int) -> None:
        """
        Sets the current view on the text to the given coordinates. For example, given a widget with shape
        (rows=1, cols=10) the string

                        "We're no strangers to love\nYou know the rules and so do I"

        would by default only display: "We're no s".  By default, the view is set to (y=0, x=0), the values
        representing the upper left part of the view into the text.

        If we were to run set_view(y=0, x=10), then the widget would instead display "trangers t". Or if we run
        set_view(y=1, x=-15), we would get "les and so".

        Locks the view such that it never exceeds the text's total boundary.
        """
        for i, j in zip((y, x), ("y", "x")):
            if not isinstance(i, (int, float)) or i != int(i):
                msg = f"\n\nAttribute `{j}` in method `set_view` of a {self._type} instance must be an integer."
                raise TypeError(msg)
        self._set_view(y=y, x=x)

    def _set_view(self, y: int, x: int) -> None:
        """
        Backend for method `set_view`.
        """
        y = max(0, min(y, max(0, self._text_shape[0] - self._shape[0])))
        x = max(0, min(x, max(0, self._text_shape[1] - self._shape[1])))
        self._view = self._text_indices[y, x]

    def scroll_up(self, rows: int = 1) -> None:
        """
        Scrolls the current view up by the designated number of rows.
        """
        self._set_view(y=self._view[0] - rows, x=self._view[1])

    def scroll_down(self, rows: int = 1) -> None:
        """
        Scrolls the current view down by the designated number of rows.
        """
        self._set_view(y=self._view[0] + rows, x=self._view[1])

    def scroll_right(self, cols: int = 1) -> None:
        """
        Scrolls the current view right by the designated number of columns.
        """
        self._set_view(y=self._view[0], x=self._view[1] + cols)

    def scroll_left(self, cols: int = 1) -> None:
        """
        Scrolls the current view left by the designated number of columns.
        """
        self._set_view(y=self._view[0], x=self._view[1] - cols)

    # GETTERS
    def write(self, ellipsis: bool = False) -> None:
        """
        Writes the string to its designated coordinates with the view taken
        into account.
        """
        # Saving the cursor position
        print("\0337", end="")

        y_start = self._view[0]
        y_stop = self._view[0] + self._shape[0]
        x_start = self._view[1]
        x_stop = self._view[1] + self._shape[1]

        for i, row_idx in enumerate(range(y_start, y_stop)):
            textutils.cursor_to(self._y0 + i, self._x0)
            if ellipsis:
                row = self._rows[row_idx]
                if row[x_stop:].strip() != "":
                    row = row[x_start : x_stop - 1] + "…"
                else:
                    row = row[x_start:x_stop]
                row = f"{self.ANSI_format}" f"{row}" f"\033[m"
                print(row, end="", flush=True)
            else:
                row = f"{self.ANSI_format}" f"{self._rows[row_idx][x_start:x_stop]}" f"\033[m"
                print(row, end="", flush=True)

        # Restoring the cursor position
        print("\0338", end="")
