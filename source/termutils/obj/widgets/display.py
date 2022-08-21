from typing import Optional, Union
from termutils.obj.color import Color


class Display:

    """
    For displaying text in a region of the terminal with automatic formatting over multiple lines.
    """

    def __init__(
        self,
        x0: int,
        y0: int,
        x1: int,
        y1: int,
        border: Optional[Union[str, Color]] = None,
        background: Optional[Union[str, Color]] = None,
        foreground: Optional[Union[str, Color]] = None,
    ):
        """
        Returns a new instance of class `Display`
        """

        if not all(isinstance(i, int) and i >= 0 for i in (x0, y0, x1, y1)):
            msg = f"\n\nArguments `x0`, `y0`, `x1`, and `y1` must be positive and of <class 'int'>."
            raise ValueError(msg)

        self._x0 = x0
        self._y0 = y0
        self._x1 = x1
        self._y1 = y1

        self._size = (y1 - y0) * (x1 - x0)
        self._shape = (y1 - y0, x1 - x0)

        if self._shape[0] <= 0 or self._shape[1] <= 0:
            msg = (
                f"\n\nWhen instantiating class `Display`, arguments `x1` and `y1` must be larger than `x0` and `y0`, "
                f"respectively."
            )
            raise ValueError(msg)

        if border is None:
            border = defaults.btn_border
        elif isinstance(border, str):
            border = Color.palette(border)
        elif isinstance(border, (tuple, list, np.ndarray)):
            border = Color(border)
        elif not isinstance(border, Color):
            msg = f"\n\nInvalid attempt to create `Display` with border color `{border}`."
            raise ValueError(msg)

        if background is None:
            background = defaults.background_color
        elif isinstance(background, str):
            background = Color.palette(background)
        elif isinstance(background, (tuple, list, np.ndarray)):
            background = Color(background)
        elif not isinstance(background, Color):
            msg = f"\n\nInvalid attempt to create `Display` with background color `{background}`."
            raise ValueError(msg)

        if foreground is None:
            foreground = defaults.foreground_color
        elif isinstance(foreground, str):
            foreground = Color.palette(foreground)
        elif isinstance(foreground, (tuple, list, np.ndarray)):
            foreground = Color(foreground)
        elif not isinstance(foreground, Color):
            msg = f"\n\nInvalid attempt to create `Display` with text color `{foreground}`."
            raise ValueError(msg)

        self._text = self.__call__("")

    def __call__(self, text: str) -> None:
        """
        Sets the current state of the display to the given text.  Ignores newline characters and automatically formats
        using python's textwrap.wrap utility.
        """
        self._text = [i.strip() for i in wrap(text.strip(), self._shape[1])]

    def rows(self, fmt_spec: str = "<") -> tuple[str]:
        """
        Returns the rows of the display as a list of strings.  Each row is exactly the length of self.shape[1].

        `fmt_spec` can take the values '<', '>', and '^'.
        """
        rows = []
        for i in self._text:
            rows.append(f"{i:{fmt_spec}{self._shape[1]}s}")
        return tuple(rows)
