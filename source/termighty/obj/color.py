from termighty.settings.data import Data
from termighty.settings.system import System
from typing import Optional, Sequence

import numpy as np


class Color:
    """
    Manages colors in RGB format, such that they may be used in instances of class String, or used to modify terminal
    background and foreground colors directly.  Many operations between colors -- as well as unary operations -- are
    supported, such as adding and subtracting colors (by RGB value), or taking a color's negative.

    Colors can be instantiated directly by inputting an RGB value (and optional color name), or they may be generated
    from a comprehensive catalog of colors using the classmethod Color.palette (the full catalog can be printed as a
    guide by executing the class method Color.list_colors).
    """

    """CLASS METHODS"""

    @classmethod
    def chart(
        cls, r: Optional[int] = None, g: Optional[int] = None, b: Optional[int] = None, term_width: int = 80
    ) -> str:
        """
        Return a terminal-printable color chart – must set exactly ONE of the parameters `r`, `g`, and `b` to a value in
        the range [0, 255].  The others must be set to None as they will be iterated over.

        Argument `term_width` should be a positive nonzero integer.
        """
        if r is not None and g is None and b is None:
            idx: int = 0
            val: int = r
        elif r is None and g is not None and b is None:
            idx: int = 1
            val: int = g
        elif r is None and g is None and b is not None:
            idx: int = 2
            val: int = b
        else:
            error_message: str = (
                f"\n\nArguments `r`, `g`, and `b` in Color.chart cannot be assigned simultaneously.  Only one argument "
                f"can take a value; the others should be `None`.\n"
            )
            System.kill_all = True
            raise ValueError(error_message)

        step: int = 256 // term_width + 1
        colors: np.ndarray = np.arange(0, 256, step)
        color_grid: list[np.ndarray, np.ndarray] = np.meshgrid(colors, colors[::2])
        out: str = ""
        char: str = "\033[38;2;{:d};{:d};{:d}m█\033[m"
        rgb: np.ndarray = np.zeros(3, dtype=np.uint8)
        for m, n in zip(*color_grid):
            for i, j in zip(m, n):
                rgb[idx] = val
                rgb[(idx + 1) % 3] = j
                rgb[(idx + 2) % 3] = i
                out += char.format(rgb[0], rgb[1], rgb[2])
            out += "\033[m\n"
        out: str = out[:-1]
        return out

    @classmethod
    def is_color(cls, name: str) -> bool:
        """
        Return True if /data/rgb.json contains the given string.  Can be used to check whether or not a color you want
        to instantiate is included in Termighty.
        """
        return name in Data.colors.keys()

    @classmethod
    def list_colors(cls, sort_by="step") -> str:
        """
        Return a string containing a list of all available colors (as viewable ANSI escape sequences) and their names.
        Remember to print the outputted string if you want to view the list in the terminal.
        """
        out: str = "\nList of Available Colors\n\n"
        colors: list["Color"] = [cls(j, i) for i, j in Data.colors.items()]
        rgb_str: str = "{:03d}{:03d}{:03d}"
        if sort_by.lower() == "rgb":

            sorted_list: list = []
            rgb_vals: list[int, ...] = [int(rgb_str.format(*i._rgb)) for i in colors]
            idx: int = np.argsort(rgb_vals)
            for i in idx:
                sorted_list.append(colors[i])
            colors: list["Color"] = sorted_list

        elif sort_by.lower() == "step":

            repetitions: int = 8

            sorted_list: list = []
            weights: np.ndarray = np.array([0.241, 0.691, 0.068], dtype=np.float64)
            lum_vals: np.ndarray = np.array([np.sqrt(np.sum(weights * i._rgb)) for i in colors])
            hsv_vals: np.ndarray = np.array([i.hsv() for i in colors])

            h: np.ndarray = (hsv_vals[:, 0] * repetitions).astype(np.int64)[:, np.newaxis]
            lum: np.ndarray = (lum_vals * repetitions).astype(np.int64)[:, np.newaxis]
            v: np.ndarray = (hsv_vals[:, 2] * repetitions).astype(np.int64)[:, np.newaxis]

            sort_keys: np.ndarray = np.concatenate([h, lum, v], axis=1)
            sort_keys: np.ndarray = np.lexsort((sort_keys[:, 2], sort_keys[:, 1], sort_keys[:, 0]), axis=0)
            for i in sort_keys:
                sorted_list.append(colors[i])
            colors: list["Color"] = sorted_list

        elif sort_by.lower() == "light":

            sorted_list: list = []
            rgb_vals: list[float] = [i.lightness(True) for i in colors]
            idx = np.argsort(rgb_vals)
            for i in idx:
                sorted_list.append(colors[i])
            colors: list["Color", ...] = sorted_list

        elif sort_by.lower() != "alpha":

            error_message: str = (
                f"Argument `sort_by` in method `Color.list_colors` must take the value `step` for step sorting "
                f"(default), `alpha` for alphabetical sorting, `rgb` for sorting by color, or `light` for sorting by "
                f"color lightness."
            )
            System.kill_all = True
            raise ValueError(error_message)

        for color in colors:
            temp: str = (
                f"{color.sample*2} {color._rgb[0]:03d} {color._rgb[1]:03d} {color._rgb[2]:03d} {color._name.title()}\n"
            )
            out += temp

        return out

    @classmethod
    def palette(cls, name: str) -> "Color":
        """
        Initialize a `Color` instance using a color name; only succeeds if the name is found in '/data/rgb.json'. These
        can be viewed in the terminal by running the following code snippet:

        from termighty import Color
        print(Color.list_colors())
        """
        if not cls.is_color(name.lower()):
            error_message: str = (
                f"\n\nAttempt to pass unknown color `{name}` to argument `name` in classmethod `Color.palette`.  Use "
                f"a known color (see classmethod Color.list_colors()).\n"
            )
            System.kill_all = True
            raise ValueError(error_message)
        return cls(Data.colors[name.lower()], name.title())

    @property
    def sample(self) -> str:
        """
        Return a color sample in the form of a printable string. The output string consists of a single whitespace
        character with the background color set to that of the current instance of class `Color`.
        """
        out: str = f"\033[48;2;{self._rgb[0]:d};{self._rgb[1]:d};{self._rgb[2]:d}m " f"\033[m"
        return out

    """CONSTRUCTOR"""

    def __init__(self, rgb: Sequence[int], name: str = "Unnamed Color") -> None:
        """
        Return a new instance of class `Color`.  Argument `rgb` should be a sequence containing three integers in the
        range [0, 255].
        """
        # Creating a np.ndarray of zeros that will contain the rgb values as three 8-bit unsigned integers.
        self._rgb: np.ndarray = np.zeros(3, np.uint8)
        # Set the RGB value using the `rgb` property setter.
        self.rgb = rgb
        # Set the name using the `name` property setter.
        self.name = name

    """MAGIC METHODS"""

    def __add__(self, color: "Color") -> "Color":
        """
        Add colors together by summing over their RGB values.  If this results in a value greater than 255 in one or
        more color channels, sets these channels to 255.
        """
        rgb: np.ndarray = self._rgb.astype(np.int64) + color._rgb.astype(np.int64)
        rgb[rgb > 255] = 255
        return self.__class__(rgb)

    def __call__(self, string: str) -> str:
        """
        Return the given `string`, but with the text colored using the current instance's RGB values.  Escape codes
        are unsupported, use at your own risk.
        """
        out: str = f"\033[38;2;{self._rgb[0]:d};{self._rgb[1]:d};{self._rgb[2]:d}m" f"{string}\033[m"
        return out

    def __hash__(self) -> int:
        """
        Return a unique hash for the combination of rgb values of the current `Color` instance.  The hash is generated
        by concatenating the zero-padded red, green, and blue channels into a string, and inputting it into the `hash`
        command.
        """
        return hash(f"{self._rgb[0]:03d}{self._rgb[1]:03d}{self._rgb[2]:03d}")

    def __repr__(self) -> str:
        """
        Return a color sample from the current instance that is machine-readable.

        Example for color `White`:
                                            Color(255 255 255)
        """
        out: str = f"Color({self._rgb[0]:03d} {self._rgb[1]:03d} {self._rgb[2]:03d})"
        return out

    def __str__(self) -> str:
        """
        Return the current instance's color name, RGB value, and a sample of the color as a formatted human-readable
        multiline string.

        Example for color `White`:
                                            Color Name – White
                                            RGB Values – 255 255 255
                                                Sample – ███████████
        """
        out: str = (
            f"Color Name – {self._name.title()}\n"
            f"RGB Values – {self._rgb[0]:03d} {self._rgb[1]:03d} "
            f"{self._rgb[2]:03d}\n"
            f"    Sample – {self.sample*11}"
        )
        return out

    def __sub__(self, color: "Color") -> "Color":
        """
        Subtract colors from each other by subtracting their RGB values. If this results in a negative value in one or
        more color channels, sets these channels to zero.
        """
        rgb: np.ndarray = self._rgb.astype(np.int64) - color._rgb.astype(np.int64)
        rgb[rgb < 0] = 0
        return self.__class__(rgb)

    """PROPERTIES"""

    @property
    def b(self) -> int:
        """
        Return current instance's blue RGB value as an integer in the range [0, 255].
        """
        return int(self._rgb[2])

    @property
    def g(self) -> int:
        """
        Return current instance's green RGB value as an integer in the range [0, 255].
        """
        return int(self._rgb[1])

    @property
    def name(self) -> str:
        """
        Return current instance's color name as a string.
        """
        return self._name

    @property
    def r(self) -> int:
        """
        Return current instance's red RGB value as an integer in the range [0, 255].
        """
        return int(self._rgb[0])

    @property
    def rgb(self) -> tuple[int, int, int]:
        """
        Return the current instance's RGB values as a tuple of integers.
        """
        return (int(self._rgb[0]), int(self._rgb[1]), int(self._rgb[2]))

    """SETTER METHODS"""

    @b.setter
    def b(self, b: int) -> None:
        """
        Set the blue channel in the rgb array to a new value.  Expects an integer in the range [0, 255].
        """
        self._rgb[2] = b

    @g.setter
    def g(self, g: int) -> None:
        """
        Set the green channel in the rgb array to a new value.  Expects an integer in the range [0, 255].
        """
        self._rgb[1] = g

    @name.setter
    def name(self, name: str) -> None:
        """
        Rename the `Color` instance using the given string.
        """
        self._name: str = name

    @r.setter
    def r(self, r: int) -> None:
        """
        Set the red channel in the rgb array to a new value.  Expects an integer in the range [0, 255].
        """
        self._rgb[0] = r

    @rgb.setter
    def rgb(self, rgb: Sequence[int]) -> None:
        """
        Reset the rgb values of the `Color` instance. Argument `rgb` should be a sequence containing three integers in
        the range [0,255].
        """
        for i in range(3):
            self._rgb[i] = rgb[i]

    """PUBLIC METHODS"""

    def brightness(self) -> int:
        """
        Return the mean of the RGB values, which can be considered a measure of the color's brightness.
        """
        return int(np.mean(self._rgb))

    def copy(self) -> "Color":
        """
        Return a deep copy of the current instance -- if you assign an instance of class `Color` to another variable and
        modify it, this will change values of the original variable because they point to the same object.  Using this
        method will create a new object in memory and prevent this issue from occurring.
        """
        return self.__class__(self._rgb, self._name)

    def hsv(self) -> tuple[float, float, float]:
        """
        Return the color of the current instance in HSV form, which converts the red, green, and blue color channels to
        their equivalent hue, saturation, and brightness.  HSV is a representation of color that attempts to more
        closely represent the way that human vision interprets color.
        """
        rgb: np.ndarray = self._rgb.astype(np.float64) / 255
        add: tuple[int, int, int] = (360, 120, 240)

        idx_max: int = np.argmax(rgb)
        idx_min: int = np.argmin(rgb)
        diff: int = np.max(rgb) - np.min(rgb)

        if diff == 0:
            h: int = 0
        else:
            h: float = (rgb[(idx_max + 1) % 3] - rgb[(idx_max + 2) % 3]) / diff
            h: float = (60 * h + add[idx_max]) % 360

        if np.max(rgb) == 0:
            s: int = 0
        else:
            s: float = 100 * diff / np.max(rgb)

        v: float = 100 * np.max(rgb)

        return (h, s, v)

    def lightness(self, weighted: bool = True) -> float:
        """
        Return the norm of the RGB vector as fraction of 255.  Should return a float in the range 0 to 1.

        If weighted, multiply the squares of the `R`, `G`, and `B` color channels by 0.299, 0.587, and 0.114,
        respectively.

        Source of weights: http://alienryderflex.com/hsp.html
        """
        if weighted:
            weights: np.ndarray = np.array([0.299, 0.587, 0.114], dtype=np.float64)
        else:
            weights: np.ndarray = np.ones(3, dtype=np.float64)
        return np.sum(weights * self._rgb.astype(np.float64) ** 2) / 65025

    def negative(self) -> "Color":
        """
        Return the color negative of the current instance, which is the element-wise difference (255-R, 255-G, 255-B),
        where `R`, `G`, and `B` are the current instance's color channels.
        """
        rgb: np.ndarray = np.full(3, 255, dtype=np.uint8)
        rgb: np.ndarray = rgb - self._rgb
        return self.__class__(rgb=rgb)
