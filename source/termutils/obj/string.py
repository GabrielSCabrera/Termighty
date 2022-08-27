from collections import UserString
from termutils.obj.color import Color
from typing import Optional, Union


class String(UserString):
    """
    A more advanced version of <class 'str'>, which can handle ANSI Escape Sequences indirectly through calling various
    methods.  These allow for custom text and background colors, as well as text styles.  Most methods for <class 'str'>
    function, such as string.partition(), string.strip(), etc.
    """

    """CONSTRUCTOR"""

    def __init__(
        self,
        string: str,
        foreground: Optional[Union[Color, str]] = None,
        background: Optional[Union[Color, str]] = None,
        style: Optional[str] = None,
    ) -> None:
        """
        Creates an instance of class `String`.

        Argument `color` should be a known color in /data/rgb.json or an instance of <class 'Color'>.

        Argument `style` should be a known style in /data/styles.json.
        """
        super().__init__(string)
        self.foreground = foreground
        self.background = background
        self.style = style

    """MAGIC METHODS"""

    def __add__(self, *args, **kwargs) -> "String":
        """
        Wrapper for `UserString` method `__add__`.
        """
        new_str: str = super().__add__(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def __format__(self, spec: str) -> str:
        """
        Formats the given string using the desired spec.
        """
        out: str = (
            # Foreground
            f"\033[{self._style_str}{self._fore_str};{self._back_str}m"
            # Main String
            f"{self.data:{spec}}"
            # Resetting to Default
            f"\033[m"
        )
        return out

    def __getitem__(self, *args, **kwargs) -> None:
        """
        Extract the data string's elements at the given indices.
        """
        new_str: str = super().__getitem__(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def __iter__(self) -> "String":
        """
        Iterates through each element of the current `String` instance.
        """
        self._iter_idx: int = -1
        return self

    def __mul__(self, *args, **kwargs) -> "String":
        """
        Wrapper for `UserString` method `__mul__`.
        """
        new_str: str = super().__mul__(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def __next__(self) -> "String":
        """
        See method `__iter__`.
        """
        self._iter_idx += 1
        if self._iter_idx >= super().__len__():
            raise StopIteration
        else:
            return self.__getitem__(self._iter_idx)

    def __radd__(self, *args, **kwargs) -> "String":
        """
        Wrapper for `UserString` method `__radd__`.
        """
        new_str: str = super().__add__(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def __repr__(self) -> str:
        """
        Returns a printable string using the given color.
        """
        return self.__str__()

    def __rmul__(self, *args, **kwargs) -> "String":
        """
        Wrapper for `UserString` method `__mul__`.
        """
        new_str: str = super().__rmul__(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def __set__(self, string: Union["String", str]) -> None:
        """
        Changes the current String's text, or replaces the instance completely, depending on the given type of argument
        `string`.
        """
        if isinstance(string, "String"):
            self: "String" = string
        else:
            self.data: str = string

    def __str__(self) -> str:
        """
        Returns a printable string using the given color.
        """
        out: str = (
            # Foreground
            f"\033[{self._style_str}{self._fore_str};{self._back_str}m"
            # Main String
            f"{self.data}"
            # Resetting to Default
            f"\033[m"
        )
        return out

    """PROPERTIES"""

    @property
    def background(self) -> Color:
        """
        Returns the `Color` instance assigned to the current background.
        """
        return self._back.copy()

    @property
    def foreground(self) -> Color:
        """
        Returns the `Color` instance assigned to the current foreground.
        """
        return self._fore.copy()

    @property
    def string(self) -> str:
        """
        Returns the uncolored and unformatted text currently assigned to this String instance.
        """
        return self.data

    @property
    def style(self) -> str:
        """
        Returns the text style associated with the current instance.
        """
        return self._style

    """SETTER METHODS"""

    @background.setter
    def background(self, color: Optional[Union[Color, str]] = None) -> None:
        """
        Sets the background color to a new value.
        """
        esc: str = "48;2"
        if color is None:
            temp: str = esc
        else:
            if not isinstance(color, Color):
                if not Color._is_color(color):
                    msg = (
                        f"\n\nAttempt to pass unknown color `{color}` to argument `color` in `set_background` for "
                        f"<class 'String'>. Use a known color (see classmethod Color.list_colors()) or an instance "
                        f"of <class 'Color'>.\n"
                    )
                    raise ValueError(msg)
                color: Color = Color.palette(color)
            temp = f"{esc};{color._rgb[0]:d};{color._rgb[1]:d};" f"{color._rgb[2]:d}"
        self._back: Color = color
        self._back_str: str = temp

    @foreground.setter
    def foreground(self, color: Optional[Union[Color, str]] = None) -> None:
        """
        Sets the foreground color to a new value.
        """
        esc: str = "38;2"
        if color is None:
            temp: str = esc
        else:
            if not isinstance(color, Color):
                if not Color._is_color(color):
                    msg = (
                        f"\n\nAttempt to pass unknown color `{color}` to argument `color` in `set_foreground` for "
                        f"<class 'String'>. Use a known color (see classmethod Color.list_colors()) or an instance "
                        f"of <class 'Color'>.\n"
                    )
                    raise ValueError(msg)
                color: Color = Color.palette(color)
            temp: str = f"{esc};{color._rgb[0]:d};{color._rgb[1]:d};" f"{color._rgb[2]:d}"
        self._fore: Color = color
        self._fore_str: str = temp

    @string.setter
    def string(self, data: str) -> None:
        """
        Overwrites the uncolored and unformatted text currently assigned to this String instance.
        """
        self.data = data

    @style.setter
    def style(self, style: Optional[str] = None) -> None:
        """
        Sets the style to a new value.
        """
        if style is None:
            self._style_str: str = ""
        elif style not in Data.styles.keys():
            styles_str: str = ", ".join(Data.styles.keys())
            msg = (
                f"\n\nAttempt to pass unknown key `{style}` to argument `style` in constructor for <class 'String'>. "
                f"Use one of the following styles: {styles_str}.\n"
            )
            raise ValueError(msg)
        else:
            style: str = style.lower()
            self._style_str: str = f"{Data.styles[style]};"
        self._style: str = style

    """PUBLIC METHODS"""

    def capitalize(self, *args, **kwargs) -> "String":
        """
        Wrapper for `UserString` method `capitalize`.
        """
        new_str: str = super().capitalize(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def casefold(self, *args, **kwargs) -> "String":
        """
        Wrapper for `UserString` method `casefold`.
        """
        new_str: str = super().casefold(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def center(self, *args, **kwargs) -> "String":
        """
        Wrapper for `UserString` method `center`.
        """
        new_str: str = super().center(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def expandtabs(self, *args, **kwargs) -> "String":
        """
        Wrapper for `UserString` method `expandtabs`.
        """
        new_str: str = super().expandtabs(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def format(self, *args, **kwargs) -> "String":
        """
        Wrapper for `UserString` method `format`.
        """
        new_str: str = super().format(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def format_map(self, *args, **kwargs) -> "String":
        """
        Wrapper for `UserString` method `format_map`.
        """
        new_str: str = super().format_map(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def join(self, *args, **kwargs) -> "String":
        """
        Wrapper for `UserString` method `join`.
        """
        new_str: str = super().join(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def ljust(self, *args, **kwargs) -> "String":
        """
        Wrapper for `UserString` method `ljust`.
        """
        new_str: str = super().ljust(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def lower(self, *args, **kwargs) -> "String":
        """
        Wrapper for `UserString` method `lower`.
        """
        new_str: str = super().lower(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def lstrip(self, *args, **kwargs) -> "String":
        """
        Wrapper for `UserString` method `lstrip`.
        """
        new_str: str = super().lstrip(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def partition(self, *args, **kwargs) -> list["String", ...]:
        """
        Wrapper for `UserString` method `partition`.
        """
        new_list: list = []
        for i in super().partition(*args, **kwargs):
            new_list.append(self.__class__(new_str, self._fore, self._back, self._style))
        return tuple(new_list)

    def removeprefix(self, *args, **kwargs) -> "String":
        """
        Wrapper for `UserString` method `removeprefix`.
        """
        new_str: str = super().removeprefix(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def removesuffix(self, *args, **kwargs) -> "String":
        """
        Wrapper for `UserString` method `removesuffix`.
        """
        new_str: str = super().removesuffix(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def replace(self, *args, **kwargs) -> "String":
        """
        Wrapper for `UserString` method `replace`.
        """
        new_str: str = super().replace(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def rjust(self, *args, **kwargs) -> "String":
        """
        Wrapper for `UserString` method `rjust`.
        """
        new_str: str = super().rjust(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def rpartition(self, *args, **kwargs) -> "String":
        """
        Wrapper for `UserString` method `rpartition`.
        """
        new_list: list = []
        for i in super().rpartition(*args, **kwargs):
            new_list.append(self.__class__(new_str, self._fore, self._back, self._style))
        return tuple(new_list)

    def rsplit(self, *args, **kwargs) -> "String":
        """
        Wrapper for `UserString` method `rsplit`.
        """
        new_list: list = []
        for i in super().rsplit(*args, **kwargs):
            new_list.append(self.__class__(new_str, self._fore, self._back, self._style))
        return new_list

    def rstrip(self, *args, **kwargs) -> "String":
        """
        Wrapper for `UserString` method `rstrip`.
        """
        new_str: str = super().rstrip(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def split(self, *args, **kwargs) -> list["String", ...]:
        """
        Wrapper for `UserString` method `split`.
        """
        new_list: list = []
        for i in super().split(*args, **kwargs):
            new_list.append(self.__class__(new_str, self._fore, self._back, self._style))
        return new_list

    def splitlines(self, *args, **kwargs) -> list["String", ...]:
        """
        Wrapper for `UserString` method `splitlines`.
        """
        new_list: list = []
        for i in super().splitlines(*args, **kwargs):
            new_list.append(self.__class__(new_str, self._fore, self._back, self._style))
        return new_list

    def strip(self, *args, **kwargs) -> "String":
        """
        Wrapper for `UserString` method `strip`.
        """
        new_str: str = super().strip(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def swapcase(self, *args, **kwargs) -> "String":
        """
        Wrapper for `UserString` method `swapcase`.
        """
        new_str: str = super().swapcase(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def title(self, *args, **kwargs) -> "String":
        """
        Wrapper for `UserString` method `title`.
        """
        new_str: str = super().title(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def translate(self, *args, **kwargs) -> "String":
        """
        Wrapper for `UserString` method `translate`.
        """
        new_str: str = super().translate(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def upper(self, *args, **kwargs) -> "String":
        """
        Wrapper for `UserString` method `upper`.
        """
        new_str: str = super().upper(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)

    def zfill(self, *args, **kwargs) -> "String":
        """
        Wrapper for `UserString` method `zfill`.
        """
        new_str: str = super().zfill(*args, **kwargs)
        return self.__class__(new_str, self._fore, self._back, self._style)
