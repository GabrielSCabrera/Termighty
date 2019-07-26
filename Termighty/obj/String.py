from ..utils.exceptions import *
from ..utils.config import *
from ..utils.utils import *
from .Char import Char
from .Charray import Charray

class String(Charray):

    """
        Meant to emulate type <str> in the Terminal environment, allows for
        a good deal of <str> operations.

        Automatically copies a new string in memory when obtaining substrings.

        Use with escape sequences at your own risk, as they are not supported!

        All colors and styles must be the same over the course of the String
    """

    def __init__(self, s, t_color = "default", b_color = "default",
    style = "default"):

        self.disallowed = ["\n", "\t", "\r"]

        # Checking that "s" is of type <str> and of non-zero length
        msg = "\n\nInstances of <class 'String'> must be initialized with an "
        msg += "argument of <class 'str'> of non-zero length.\nAttempted to "
        msg += "initialize with "
        if not isinstance(s, str):
            msg += "an argument of {}".format(type(s))
            raise TypeError(msg)
        elif len(s) == 0:
            msg += "a <str> of length zero."
            raise ValueError(msg)

        check_char_args_method(t_color, b_color, style, "String", "__init__()")

        # Will contain the individual Char objects that make up the String
        string_arr = []
        for i in s:
            if i not in self.disallowed:
                string_arr.append(Char(i, t_color, b_color, style))
            else:
                msg = "\n\nObjects of <class 'String'> do not support ANSI "
                msg += "escape sequences."
                raise ValueError(msg)

        Charray.__init__(self, arr = [string_arr])
        self.string = s
        self.t_color = t_color
        self.b_color = b_color
        self.style = style

    def __len__(self):
        """
            Returns the length of the String.
        """
        return len(self.string)

    def __getitem__(self, idx):
        """
            Returns a new String object containing the elements denoted in
            "idx", and is allocated its own memory.
        """
        start, stop, step = process_idx(idx, self.__len__())
        new_string = ""
        for i in range(start, stop, step):
            new_string += self.string[i]
        if len(new_string) == 1:
            return Char(new_string, self.t_color, self.b_color, self.style)
        else:
            return String(new_string, self.t_color, self.b_color, self.style)

    def __setitem__(self, idx, value):
        """
            Replaces the index/indices given in "idx" with the String in
            "value".  Only accepts objects of <class 'String'> and
            <class 'str'>.
        """
        check_type_method((String,str), value, "String", "__setitem__", "value")

        if isinstance(value, String):
            # Checking that "t_color", "b_color", and "style" match both in
            # argument "value" and the current Class instance.
            msg = "\n\nArgument \"value\" in method \"__setitem__\" in class "
            msg += "\"String\" must have same t_color, b_color, and style as "
            msg += "the String instance being called upon."
            if value.t_color != self.t_color or value.b_color != self.b_color\
            or value.style != self.style:
                raise ValueError(msg)

        # Replacing the individual characters
        msg = "\n\nArgument \"value\" in method \"__setitem__\" in class "
        msg += "\"String\" does not match the length of the given index/indices"
        msg += " in \"idx\"."
        n = 0
        try:
            for i in range_idx(idx, self.__len__()):
                if isinstance(value, String):
                    self.arr[0][i].overwrite(value.arr[0][n])
                elif isinstance(value, str):
                    if value[n] not in self.disallowed:
                        self.arr[0][i].overwrite(Char(value[n], self.t_color,
                        self.b_color, self.style))
                    else:
                        msg = "\n\nObjects of <class 'String'> do not support "
                        msg += "ANSI escape sequences."
                        raise ValueError(msg)
                n += 1
        except IndexError:
            raise IndexError(msg)

        # Making sure the entirety of "value" is fitted to the new indices
        if len(value) != n:
            raise ValueError(msg)

    def __iter__(self):
        """
            Returns each Char element in the current String, sequentially.
        """
        for s in self.arr[0]:
            yield s

    def copy(self):
        """
            Returns a copy of the current object.  Use this to avoid issues
            with pointers referring to the same memory location.
        """
        return String(self.string, self.t_color, self.b_color, self.style)

    def set_text(self, text):
        """
            Changes the current text, keeping the other parameters unchanged
        """
        check_type_method(str, text, "String", "set_text(text)", "text")
        self.__init__(text, self.t_color, self.b_color, self.style)

    def set_t_color(self, t_color):
        """
            Changes the current t_color, keeping the other parameters unchanged
        """
        check_char_args_method(t_color, "default", "default", "String",
        "set_t_color(t_color)", "t_color")
        self.__init__(self.string, t_color, self.b_color, self.style)

    def set_b_color(self, b_color):
        """
            Changes the current b_color, keeping the other parameters unchanged
        """
        check_char_args_method("default", b_color, "default", "String",
        "set_b_color(b_color)", "b_color")
        self.__init__(self.string, self.t_color, b_color, self.style)

    def set_style(self, style):
        """
            Changes the current style, keeping the other parameters unchanged
        """
        check_char_args_method("default", "default", style, "String",
        "set_style(style)", "style")
        self.__init__(self.string, self.t_color, self.b_color, style)

    # <class 'str'> method wrappers.  All methods return new String objects.

    def capitalize(self):
        """
            Converts the first character in the current String to uppercase.
        """
        new_str = self.string.capitalize()
        return String(new_str, self.t_color, self.b_color, self.style)

    def casefold(self):
    	"""
    		Converts all characters in the current String to lowercase.
    	"""
    	new_str = self.string.casefold()
    	return String(new_str, self.t_color, self.b_color, self.style)

    def count(self, sub, start = None, end = None):
    	"""
            Returns how many times "sub" occurs in the current String.
    	"""
    	return self.string.count(sub, start, end)

    def endswith(self, suffix, start = None, end = None):
    	"""
    		If the String ends in "suffix", returns True.
    	"""
    	return self.string.endswith(suffix, start, end)

    def find(self, sub, start = None, end = None):
    	"""
            Returns the index of the substring "sub" in the current String,
            if not found, returns False.
    	"""
    	return self.string.find(sub, start, end)

    def index(self, sub, start = None, end = None):
    	"""
            Returns the index of the substring "sub" in the current String,
            if not found, raises an Error.
    	"""
    	return self.string.index(sub, start, end)

    def isalnum(self):
    	"""
            If all Chars in the current String are alphanumeric, returns True.
    	"""
    	return self.string.isalnum()

    def isalpha(self):
    	"""
    		If all Chars in the current String are alphabetic, returns True.
    	"""
    	return self.string.isalpha()

    def isdecimal(self):
        """
            If all Chars in the current String are decimal, returns True.
        """
        return self.string.isdecimal()

    def isdigit(self):
    	"""
    		If all Chars in the current String are digits, returns True.
    	"""
    	return self.string.isdigit()

    def islower(self):
        """
            If all Chars in the current String are lowercase, returns True.
        """
        return self.string.islower()

    def isnumeric(self):
    	"""
    		If all Chars in the current String are numeric, returns True.
    	"""
    	return self.string.isnumeric()

    def isprintable(self):
    	"""
    		If all Chars in the current String are printable, returns True.
    	"""
    	return self.string.isprintable()

    def isspace(self):
    	"""
    		If all Chars in the current String are whitespace, returns True.
    	"""
    	return self.string.isspace()

    def istitle(self):
    	"""
    		If only the first Char of each word is uppercase, returns True.
    	"""
    	return self.string.istitle()

    def isupper(self):
    	"""
    		If every Char is uppercase, returns True.
    	"""
    	return self.string.isupper()

    def lower(self):
    	"""
    		If every Char is lowercase, returns True.
    	"""
    	new_str = self.string.lower()
    	return String(new_str, self.t_color, self.b_color, self.style)

    def lstrip(self, chars = None):
    	"""
    		Returns a String that is stripped of whitespace on its left.
    	"""
    	new_str = self.string.lstrip(chars)
    	return String(new_str, self.t_color, self.b_color, self.style)

    def replace(self, old, new, count = None):
    	"""
            Replaces the subString with the value "old" with "new".
    	"""
    	new_str = self.string.replace(old, new, count)
    	return String(new_str, self.t_color, self.b_color, self.style)

    def rfind(self, sub, start = None, end = None):
    	"""
            Returns the last index of the substring "sub" in the current String,
            if not found, returns False.
    	"""
    	return self.string.rfind(sub, start, end)

    def rindex(self, sub, start = None, end = None):
    	"""
            Returns the last index of the substring "sub" in the current String,
            if not found, raises an Error.
    	"""
    	return self.string.rindex(sub, start, end)

    def rsplit(self, sep = None, maxsplit = 1):
        """
            Given a separator "sep", returns a list of the String split at
            "sep". If "sep" is not specified, splits at whitespace.
        """
        str_list = self.string.rsplit(sep, maxsplit)
        new_list = []
        for i in new_list:
            new_list.append(String(i, self.t_color, self.b_color, self.style))
        return new_list

    def rstrip(self, chars = None):
    	"""
    		Returns a String that is stripped of whitespace on its right
    	"""
    	new_str = self.string.rstrip(chars)
    	return String(new_str, self.t_color, self.b_color, self.style)

    def split(self, sep = None, maxsplit = 1):
        """
            Given a separator "sep", returns a list of the String split at
            "sep". If "sep" is not specified, splits at whitespace.
        """
        str_list = self.string.split(sep, maxsplit)
        new_list = []
        for i in new_list:
            new_list.append(String(i, self.t_color, self.b_color, self.style))
        return new_list

    def startswith(self, prefix, start = None, end = None):
    	"""
            If the String starts with "prefix", returns True.
    	"""
    	return self.string.startswith(prefix, start, end)

    def swapcase(self):
    	"""
            All lowercase subStrings are capitalized, while all uppercase
            elements are lowered.
    	"""
    	new_str = self.string.swapcase()
    	return String(new_str, self.t_color, self.b_color, self.style)

    def title(self):
    	"""
    		Sets the first Char of each word to be uppercase, while others are
            made lowercase.
    	"""
    	new_str = self.string.title()
    	return String(new_str, self.t_color, self.b_color, self.style)

    def upper(self):
    	"""
            Capitalizes all elements of the String.
    	"""
    	new_str = self.string.upper()
    	return String(new_str, self.t_color, self.b_color, self.style)

    def zfill(self, width):
    	"""
            Fills the String with zeros; the number of zeros given by "width".
    	"""
    	new_str = self.string.zfill(width)
    	return String(new_str, self.t_color, self.b_color, self.style)
