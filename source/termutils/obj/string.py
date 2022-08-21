from collections import UserString
from termutils.obj.color import Color
from typing import Optional, Union


class String(UserString):
    def __init__(
        self,
        string: str,
        foreground: Optional[Union[Color, str]] = None,
        background: Optional[Union[Color, str]] = None,
        style: Optional[str] = None,
    ):
        """
        Creates an instance of class `String`.

        Argument `color` should be a known color in /data/rgb.json or an instance of <class 'Color'>.

        Argument `style` should be a known style in /data/styles.json.
        """
        super().__init__(string)
        self.set_foreground(color=foreground)
        self.set_background(color=background)
        self.set_style(style=style)

    """SETTERS"""

    def set_foreground(self, color: Optional[Union[Color, str]] = None):
        """
        Sets the foreground color to a new value.
        """
        esc = "38;2"
        if color is None:
            temp = esc
        else:
            if not isinstance(color, Color):
                if not Color._is_color(color):
                    msg = (
                        f"\n\nAttempt to pass unknown color `{color}` to argument `color` in `set_foreground` for "
                        f"<class 'String'>. Use a known color (see classmethod Color.list_colors()) or an instance "
                        f"of <class 'Color'>.\n"
                    )
                    raise ValueError(msg)
                color = Color.palette(color)
            temp = f"{esc};{color._rgb[0]:d};{color._rgb[1]:d};" f"{color._rgb[2]:d}"
        self._fore = color
        self._fore_str = temp

    def set_background(self, color: Optional[Union[Color, str]] = None):
        """
        Sets the background color to a new value.
        """
        esc = "48;2"
        if color is None:
            temp = esc
        else:
            if not isinstance(color, Color):
                if not Color._is_color(color):
                    msg = (
                        f"\n\nAttempt to pass unknown color `{color}` to argument `color` in `set_background` for "
                        f"<class 'String'>. Use a known color (see classmethod Color.list_colors()) or an instance "
                        f"of <class 'Color'>.\n"
                    )
                    raise ValueError(msg)
                color = Color.palette(color)
            temp = f"{esc};{color._rgb[0]:d};{color._rgb[1]:d};" f"{color._rgb[2]:d}"
        self._back = color
        self._back_str = temp

    def set_style(self, style: Optional[str] = None) -> None:
        """
        Sets the style to a new value.
        """
        if style is None:
            self._style_str = ""
        elif style not in Data.styles.keys():
            styles_str = ", ".join(Data.styles.keys())
            msg = (
                f"\n\nAttempt to pass unknown key `{style}` to argument `style` in constructor for <class 'String'>. "
                f"Use one of the following styles: {styles_str}.\n"
            )
            raise ValueError(msg)
        else:
            style = style.lower()
            self._style_str = f"{Data.styles[style]};"
        self._style = style

    def __set__(self, string: Union["String", str]) -> None:
        """
        Changes the current String's text, or replaces the instance completely, depending on the given type of argument
        `string`.
        """
        if isinstance(string, "String"):
            self = string
        else:
            self.data = string

    """GETTERS"""

    @property
    def foreground(self):
        """
        Returns the `Color` instance assigned to the current foreground.
        """
        return self._fore.copy()

    @property
    def background(self):
        """
        Returns the `Color` instance assigned to the current background.
        """
        return self._back.copy()

    @property
    def style(self):
        """
        Returns the text style associated with the current instance.
        """
        return self._style

    def __getitem__(self, *args, **kwargs) -> None:
        """
        Replace the data string's elements at the given indices.
        """
        new_str = super().__getitem__(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def __str__(self):
        """
        Returns a printable string using the given color.
        """
        out = (
            # Foreground
            f"\033[{self._style_str}{self._fore_str};{self._back_str}m"
            # Main String
            f"{self.data}"
            # Resetting to Default
            f"\033[m"
        )
        return out

    def __repr__(self):
        """
        Returns a printable string using the given color.
        """
        return self.__str__()

    def __format__(self, spec: str):
        """
        Formats the given string using the desired spec.
        """
        out = (
            # Foreground
            f"\033[{self._style_str}{self._fore_str};{self._back_str}m"
            # Main String
            f"{self.data:{spec}}"
            # Resetting to Default
            f"\033[m"
        )
        return out

    """OPERATORS"""

    def __add__(self, *args, **kwargs):
        """
        Wrapper for `UserString` method `__add__`.
        """
        new_str = super().__add__(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def __mul__(self, *args, **kwargs):
        """
        Wrapper for `UserString` method `__mul__`.
        """
        new_str = super().__mul__(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def __rmul__(self, *args, **kwargs):
        """
        Wrapper for `UserString` method `__mul__`.
        """
        new_str = super().__rmul__(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def __iter__(self):
        """
        Iterates through each element of the current `String` instance.
        """
        self._iter_idx = -1
        return self

    def __next__(self):
        """
        See method `__iter__`.
        """
        self._iter_idx += 1
        if self._iter_idx >= super().__len__():
            raise StopIteration
        else:
            return self.__getitem__(self._iter_idx)

    def __radd__(self, *args, **kwargs):
        """
        Wrapper for `UserString` method `__radd__`.
        """
        new_str = super().__add__(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    """WRAPPED CLASS str METHODS"""

    def capitalize(self, *args, **kwargs):
        """
        Wrapper for `UserString` method `capitalize`.
        """
        new_str = super().capitalize(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def casefold(self, *args, **kwargs):
        """
        Wrapper for `UserString` method `casefold`.
        """
        new_str = super().casefold(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def center(self, *args, **kwargs):
        """
        Wrapper for `UserString` method `center`.
        """
        new_str = super().center(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def expandtabs(self, *args, **kwargs):
        """
        Wrapper for `UserString` method `expandtabs`.
        """
        new_str = super().expandtabs(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def format(self, *args, **kwargs):
        """
        Wrapper for `UserString` method `format`.
        """
        new_str = super().format(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def format_map(self, *args, **kwargs):
        """
        Wrapper for `UserString` method `format_map`.
        """
        new_str = super().format_map(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def join(self, *args, **kwargs):
        """
        Wrapper for `UserString` method `join`.
        """
        new_str = super().join(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def ljust(self, *args, **kwargs):
        """
        Wrapper for `UserString` method `ljust`.
        """
        new_str = super().ljust(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def lower(self, *args, **kwargs):
        """
        Wrapper for `UserString` method `lower`.
        """
        new_str = super().lower(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def lstrip(self, *args, **kwargs):
        """
        Wrapper for `UserString` method `lstrip`.
        """
        new_str = super().lstrip(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def partition(self, *args, **kwargs):
        """
        Wrapper for `UserString` method `partition`.
        """
        new_list = []
        for i in super().partition(*args, **kwargs):
            new_list.append(self.__class__(new_str, self._fore, self._back, self._style))
        return tuple(new_list)

    def removeprefix(self, *args, **kwargs):
        """
        Wrapper for `UserString` method `removeprefix`.
        """
        new_str = super().removeprefix(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def removesuffix(self, *args, **kwargs):
        """
        Wrapper for `UserString` method `removesuffix`.
        """
        new_str = super().removesuffix(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def replace(self, *args, **kwargs):
        """
        Wrapper for `UserString` method `replace`.
        """
        new_str = super().replace(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def rjust(self, *args, **kwargs):
        """
        Wrapper for `UserString` method `rjust`.
        """
        new_str = super().rjust(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def rpartition(self, *args, **kwargs):
        """
        Wrapper for `UserString` method `rpartition`.
        """
        new_list = []
        for i in super().rpartition(*args, **kwargs):
            new_list.append(self.__class__(new_str, self._fore, self._back, self._style))
        return tuple(new_list)

    def rsplit(self, *args, **kwargs):
        """
        Wrapper for `UserString` method `rsplit`.
        """
        new_list = []
        for i in super().rsplit(*args, **kwargs):
            new_list.append(self.__class__(new_str, self._fore, self._back, self._style))
        return new_list

    def rstrip(self, *args, **kwargs):
        """
        Wrapper for `UserString` method `rstrip`.
        """
        new_str = super().rstrip(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def split(self, *args, **kwargs):
        """
        Wrapper for `UserString` method `split`.
        """
        new_list = []
        for i in super().split(*args, **kwargs):
            new_list.append(self.__class__(new_str, self._fore, self._back, self._style))
        return new_list

    def splitlines(self, *args, **kwargs):
        """
        Wrapper for `UserString` method `splitlines`.
        """
        new_list = []
        for i in super().splitlines(*args, **kwargs):
            new_list.append(self.__class__(new_str, self._fore, self._back, self._style))
        return new_list

    def strip(self, *args, **kwargs):
        """
        Wrapper for `UserString` method `strip`.
        """
        new_str = super().strip(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def swapcase(self, *args, **kwargs):
        """
        Wrapper for `UserString` method `swapcase`.
        """
        new_str = super().swapcase(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def title(self, *args, **kwargs):
        """
        Wrapper for `UserString` method `title`.
        """
        new_str = super().title(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def translate(self, *args, **kwargs):
        """
        Wrapper for `UserString` method `translate`.
        """
        new_str = super().translate(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def upper(self, *args, **kwargs):
        """
        Wrapper for `UserString` method `upper`.
        """
        new_str = super().upper(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def zfill(self, *args, **kwargs):
        """
        Wrapper for `UserString` method `zfill`.
        """
        new_str = super().zfill(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)
