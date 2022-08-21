from termutils.data import Data
from typing import Optional, Sequence

import numpy as np

class Color:

    """CONSTRUCTOR"""

    def __init__(self, rgb: Sequence[int], name: str = "Unnamed Color") -> None:
        """
        Returns a new instance of class `Color`.  Argument `rgb` should be a sequence containing three integers in range
        0-255.
        """
        self._rgb = np.zeros(3, np.uint8)
        self.set_name(name)
        self.set_rgb(rgb)

    """INSTANTIATORS"""

    @classmethod
    def palette(cls, name: str) -> "Color":
        """
        To initialize a `Color` instance using a color name; only succeeds if the name is found in '/data/rgb.json'
        """
        if not cls._is_color(name):
            msg = (
                f"\n\nAttempt to pass unknown color `{name}` to argument `name` in classmethod `Color.palette`.  Use "
                f"a known color (see classmethod Color.list_colors()).\n"
            )
            raise ValueError(f"\n\nSelected color `{name}` is unknown.\n")
        return cls(Data.colors[name], name)

    def negative(self) -> "Color":
        """
        Returns the color negative of the current instance, which is the element-wise difference (255-R, 255-G, 255-B),
        where `R`, `G`, and `B` are the current instance's color channels.
        """
        rgb = np.full(3, 255, dtype=np.uint8)
        rgb = rgb - self._rgb
        return self.__class__(rgb=rgb)

    def copy(self) -> "Color":
        """
        Returns a deep copy of the current instance
        """
        return self.__class__(self._rgb, self._name)

    """SETTER METHODS"""

    def set_name(self, name: str) -> None:
        """
        To rename the `Color` instance
        """
        self._name = name

    def set_rgb(self, rgb: Sequence[int]) -> None:
        """
        To reset the rgb values of the `Color` instance. Argument `rgb` should be a sequence containing three integers
        in range 0-255.
        """
        for i in range(3):
            self._rgb[i] = rgb[i]

    def set_r(self, r: int) -> None:
        """
        To set the red color in the rgb array to a new value.  Expects an integer in range 0 to 255.
        """
        self._rgb[0] = r

    def set_g(self, g: int) -> None:
        """
        To set the green color in the rgb array to a new value.  Expects an integer in range 0 to 255.
        """
        self._rgb[1] = g

    def set_b(self, b: int) -> None:
        """
        To set the blue color in the rgb array to a new value.  Expects an integer in range 0 to 255.
        """
        self._rgb[2] = b

    """GETTER METHODS"""

    def __call__(self, s: str) -> str:
        """
        Returns the given string `s`, but with the text colored using the current instance's RGB values.  Escape codes
        are unsupported, use at your own risk.
        """
        out = f"\033[38;2;{self._rgb[0]:d};{self._rgb[1]:d};{self._rgb[2]:d}m" f"{s}\033[m"
        return out

    def __str__(self) -> str:
        """
        Returns the color name, RGB value, and a sample of the color.
        """
        out = (
            f"Color Name – {self._name.title()}"
            f"RGB Values – {self._rgb[0]:03d} {self._rgb[1]:03d} "
            f"{self._rgb[2]:03d}"
            f"    Sample – {self.sample*11}"
        )
        return out

    def __repr__(self) -> str:
        """
        Returns a color sample that is machine-readable
        """
        out = f"Color({self._rgb[0]:03d} {self._rgb[1]:03d} {self._rgb[2]:03d})"
        return out

    def __hash__(self) -> int:
        """
        To return a unique hash for the rgb values of a `Color` instance.
        """
        return hash(f"{self._rgb[0]:03d}{self._rgb[1]:03d}{self._rgb[2]:03d}")

    @property
    def name(self) -> str:
        """
        Returns an instance's color name.
        """
        return self._name

    @property
    def rgb(self) -> tuple[int]:
        """
        Returns an instance's RGB values.
        """
        return (int(self._rgb[0]), int(self._rgb[1]), int(self._rgb[2]))

    @property
    def r(self) -> int:
        """
        Returns an instance's red RGB value.
        """
        return int(self._rgb[0])

    @property
    def g(self) -> int:
        """
        Returns an instance's green RGB value.
        """
        return int(self._rgb[1])

    @property
    def b(self) -> int:
        """
        Returns an instance's blue RGB value.
        """
        return int(self._rgb[2])

    def brightness(self) -> int:
        """
        Returns the mean of the RGB values.
        """
        return int(np.mean(self._rgb))

    def lightness(self, weighted: bool = True) -> float:
        """
        Returns the norm of the RGB vector as fraction of 255.  Should return a float in the range 0 to 1.

        If weighted, will multiply the squares of R, G, and B with 0.299, 0.587, and 0.114, respectively.

        Source of weights: http://alienryderflex.com/hsp.html
        """
        if weighted:
            weights = np.array([0.299, 0.587, 0.114], dtype=np.float64)
        else:
            weights = np.ones(3, dtype=np.float64)
        return np.sum(weights * self._rgb.astype(np.float64) ** 2) / 65025

    def hsv(self):
        """
        Returns the current color in HSV form.
        """
        rgb = self._rgb.astype(np.float64) / 255
        add = [360, 120, 240]

        idx_max = np.argmax(rgb)
        idx_min = np.argmin(rgb)
        diff = np.max(rgb) - np.min(rgb)

        if diff == 0:
            h = 0
        else:
            h = (rgb[(idx_max + 1) % 3] - rgb[(idx_max + 2) % 3]) / diff
            h = (60 * h + add[idx_max]) % 360

        if np.max(rgb) == 0:
            s = 0
        else:
            s = 100 * diff / np.max(rgb)

        v = 100 * np.max(rgb)

        return (h, s, v)

    """SAMPLER METHODS"""

    @property
    def sample(self) -> str:
        """
        Returns a color sample in the form of a printable string.
        """
        out = f"\033[48;2;{self._rgb[0]:d};{self._rgb[1]:d};{self._rgb[2]:d}m " f"\033[m"
        return out

    @staticmethod
    def chart(r: Optional[int] = None, g: Optional[int] = None, b: Optional[int] = None, term_width: int = 80) -> str:
        """
        Return a terminal-printable color chart – must set exactly ONE of the parameters `r`, `g`, and `b` to a value in
        range 0 to 255.  The others must remain set to None.

        Argument `term_width` should be a positive nonzero integer.
        """
        if r is not None and g is None and b is None:
            idx = 0
            val = r
        elif r is None and g is not None and b is None:
            idx = 1
            val = g
        elif r is None and g is None and b is not None:
            idx = 2
            val = b
        else:
            msg = (
                f"\n\nArguments `r`, `g`, and `b` in Color.chart cannot be assigned simultaneously.  Only one argument "
                f"can take a value; the others should be `None`.\n"
            )
            raise ValueError(msg)

        step = 256 // term_width + 1
        colors = np.arange(0, 256, step)
        color_grid = np.meshgrid(colors, colors[::2])
        out = ""
        char = "\033[38;2;{:d};{:d};{:d}m█\033[m"
        rgb = np.zeros(3, dtype=np.uint8)
        for m, n in zip(*color_grid):
            for i, j in zip(m, n):
                rgb[idx] = val
                rgb[(idx + 1) % 3] = j
                rgb[(idx + 2) % 3] = i
                out += char.format(rgb[0], rgb[1], rgb[2])
            out += "\033[m\n"
        out = out[:-1]
        return out

    @classmethod
    def list_colors(cls, sort_by="step") -> str:
        """
        Returns a list of all available colors and their names.
        """
        out = "\nList of Available Colors\n\n"
        colors = [cls(j, i) for i, j in Data.colors.items()]
        rgb_str = "{:03d}{:03d}{:03d}"
        if sort_by.lower() == "rgb":

            sorted_list = []
            rgb_vals = [int(rgb_str.format(*i._rgb)) for i in colors]
            idx = np.argsort(rgb_vals)
            for i in idx:
                sorted_list.append(colors[i])
            colors = sorted_list

        elif sort_by.lower() == "step":

            repetitions = 8

            sorted_list = []
            weights = np.array([0.241, 0.691, 0.068], dtype=np.float64)
            lum_vals = np.array([np.sqrt(np.sum(weights * i._rgb)) for i in colors])
            hsv_vals = np.array([i.hsv() for i in colors])

            h = (hsv_vals[:, 0] * repetitions).astype(np.int64)[:, np.newaxis]
            lum = (lum_vals * repetitions).astype(np.int64)[:, np.newaxis]
            v = (hsv_vals[:, 2] * repetitions).astype(np.int64)[:, np.newaxis]

            sort_keys = np.concatenate([h, lum, v], axis=1)
            sort_keys = np.lexsort((sort_keys[:, 2], sort_keys[:, 1], sort_keys[:, 0]), axis=0)
            for i in sort_keys:
                sorted_list.append(colors[i])
            colors = sorted_list

        elif sort_by.lower() == "light":

            sorted_list = []
            rgb_vals = [i.lightness for i in colors]
            idx = np.argsort(rgb_vals)
            for i in idx:
                sorted_list.append(colors[i])
            colors = sorted_list

        elif sort_by.lower() != "alpha":

            msg = (
                f"Argument `sort_by` in method `Color.list_colors` must take the value `step` for step sorting "
                f"(default), `alpha` for alphabetical sorting, `rgb` for sorting by color, or `light` for sorting by "
                f"color lightness."
            )
            raise ValueError(msg)

        for color in colors:
            temp = (
                f"{color.sample*2} {color._rgb[0]:03d} {color._rgb[1]:03d} {color._rgb[2]:03d} {color._name.title()}\n"
            )
            out += temp

        return out

    """OPERATORS"""

    def __add__(self, color: "Color") -> "Color":
        """
        To add colors together by summing over their RGB values.  Values greater than 255 are set to 255.
        """
        rgb = self._rgb.astype(np.int64) + color._rgb.astype(np.int64)
        rgb[rgb > 255] = 255
        return self.__class__(rgb)

    def __sub__(self, color: "Color") -> "Color":
        """
        To subtract colors from each other by subtracting their RGB values. Values less than 0 are set to 0.
        """
        rgb = self._rgb.astype(np.int64) - color._rgb.astype(np.int64)
        rgb[rgb < 0] = 0
        return self.__class__(rgb)

    """PRIVATE METHODS"""

    @classmethod
    def _is_color(cls, name: str) -> bool:
        """
        Returns True if /data/rgb.json contains the given string.
        """
        return name in Data.colors.keys()
