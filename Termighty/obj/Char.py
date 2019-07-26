from ..utils.exceptions import *
from ..utils.config import *
from ..utils.utils import *

class Char:

    """
        A single-character "pixel" that can have a custom text and/or
        background color.
    """

    def __init__(self, c = None, t_color = "default", b_color = "default",
    style = "default"):
        """
            Checks that all parameters are valid:

            [1]     c           A single character string
            [2]     t_color     Key in "text_colors"
            [3]     b_color     Key in "back_colors"
            [4]     style       Key in "styles"
        """

        # Checking that "c" is a single-character string
        if c is None:
            c = " "
        elif not isinstance(c, str) or len(c) != 1:
            msg = "\n\nInitialization argument \"c\" in class \"Char\" must be"
            msg += " a <str> of length 1."
            raise ValueError(msg)

        check_char_args_method(t_color, b_color, style, "Char", "__init__()")

        # Extracting the codes for each color and style

        tc_code = globals()["text_colors"][(t_color.lower()).strip()]
        bc_code = globals()["back_colors"][(b_color.lower()).strip()]
        st_code = globals()["styles"][(style.lower()).strip()]

        # Saving the Char properties
        self.char = c                                       # Raw Char

        self.t_color = (t_color.lower()).strip()            # Text Color
        if self.t_color in globals()["aliases_color"].keys():
            self.t_color = globals()["aliases_color"][self.t_color]

        self.b_color = (b_color.lower()).strip()            # Background Color
        if self.b_color in globals()["aliases_color"].keys():
            self.b_color = globals()["aliases_color"][self.b_color]

        self.style = (style.lower()).strip()                # Text Style
        if self.style in globals()["aliases_style"].keys():
            self.style = globals()["aliases_style"][self.style]

        # Formatting the Char string
        div = "{:d};{:d};{:d}".format(st_code, tc_code, bc_code)

        # Saving the formatted Char
        self.disp = '\x1b[{}m'.format(div) + c +'\x1b[0m'   # Formatted Char

    def __str__(self):
        return self.disp

    def __delattr__(self, name):
        """
            Prevents the user from deleting attributes.
        """
        msg = "\n\nUnable to delete attribute \"{}\" in class \"Char\""\
        .format(name)
        raise AttributeError(msg)

    def __eq__(self, new):
        """
            Checks if all the attributes in this Char matches those of another
            Char via the "==" operator.
        """
        condition1 = not isinstance(new, Char)
        condition2 = (self.char == new.char) or (self.t_color == new.t_color)
        condition3 = (self.b_color == new.b_color) or (self.style == new.style)
        if condition1 or condition2 or condition3:
            return False
        else:
            return True

    def set_text(self, c):
        """
            Change the Char text
        """
        check_type_method(str, c, "Char" , "set_text(c)", "c")
        if len(c) != 1:
            msg = "\n\nArgument \"c\" in method \"set_text(c)\" "
            msg += "should be a <str> of length 1."
            raise ValueError(msg)
        self.__init__(c = c, t_color = self.t_color, b_color = self.b_color,
        style = self.style)

    def set_t_color(self, t_color):
        """
            Change the Char text color
        """
        check_type_method(str, t_color, "Char", "set_t_color(t_color)",
        "t_color")
        if t_color not in globals()["text_colors"]:
            msg = "\n\nArgument \"t_color\" in method \"set_t_color(t_color)\" "
            msg += "should be a valid color in the form of a <str>."
            msg += " Available selection:"
            for k,v in globals()["aliases_color"].items():
                msg += "\n\t[{}] – {}".format(v, k)
            raise ValueError(msg)
        self.__init__(c = self.char, t_color = t_color, b_color = self.b_color,
        style = self.style)

    def set_b_color(self, b_color):
        """
            Change the Char background color
        """
        check_type_method(str, b_color,"Char", "set_b_color(b_color)",
        "b_color")
        if b_color not in globals()["back_colors"]:
            msg = "\n\nArgument \"b_color\" in method \"set_b_color(b_color)\" "
            msg += "should be a valid color in the form of a <str>."
            msg += " Available selection:"
            for k,v in globals()["aliases_color"].items():
                msg += "\n\t[{}] – {}".format(v, k)
            raise ValueError(msg)
        self.__init__(c = self.char, t_color = self.t_color, b_color = b_color,
        style = self.style)

    def set_style(self, style):
        """
            Change the Char style
        """
        check_type_method(str, style, "Char", "set_style(style)", "style")
        if style not in globals()["styles"]:
            msg = "\n\nArgument \"style\" in method \"set_style(style)\" "
            msg += "should be a valid color in the form of a <str>."
            msg += " Available selection:"
            for k,v in globals()["aliases_style"].items():
                msg += "\n\t[{}] – {}".format(v, k)
            raise ValueError(msg)
        self.__init__(c = self.char, t_color = self.t_color,
        b_color = self.b_color, style = style)

    def copy(self):
        """
            Copies the current state of the Char object to a new Char object,
            to avoid issues with memory.
        """
        return Char(self.char, self.t_color, self.b_color, self.style)

    def compact(self):
        """
            Returns three integers with the Char's color and style data
        """
        colors = {"k":0, "r":1, "g":2, "y":3, "b":4, "p":5, "c":6, "w":7, "d":8}
        styles = {"d":0, "b":1, "f":2, "i":3, "u":4, "n":5, "s":6}
        t_color = colors[self.t_color]
        b_color = colors[self.b_color]
        style = styles[self.style]
        return t_color, b_color, style

    def overwrite(self, new):
        """
            Re-initialize this object in-place with new properties given by a
            char "new".
        """
        if not isinstance(new, Char):
            msg = "\n\nCan only overwrite \"Char\" objects with another Char."
            msg += "\nAttempted to overwrite with a {} object."\
            .format(type(new))
            raise TypeError(msg)

        self.__init__(c = new.char, t_color = new.t_color,
        b_color = new.b_color, style = new.style)

    def display(self):
        print(self.disp, end = "")
