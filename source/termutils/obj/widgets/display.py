from typing import Optional, Union
from termutils.obj.color import Color
from termutils.obj.widgets.widget import Widget
from textwrap import wrap


class Display(Widget):

    """
    For displaying text in a region of the terminal with automatic formatting over multiple lines.
    """

    def rows(self, fmt_spec: str = "<") -> list[list[str, ...], ...]:
        """
        Returns the rows of the display as a list of strings.  Each row is exactly the length of self.shape[1].

        `fmt_spec` can take the values '<', '>', and '^'.
        """
        rows = []
        for i in self._text:
            rows.append(f"{i:{fmt_spec}{self._shape[1]}s}")
        return rows
