from ..utils.exceptions import *
from ..utils.config import *
from ..utils.utils import *
from ..obj import Char

class Charray:
    """
        An array of Char objects, can modify individual array elements using
        indexing.  Row-major; indices take the form (row, column), or in other
        words (height, width).
    """

    def __init__(self, height = None, width = None, t_color = "default",
    b_color = "default", style = "default", arr = None):

        msg = "\n\nCustom array must be a list, tuple, or Charray.\n"
        msg += "It must also only consist of Char objects, and be rectangular."

        # Generating the array Char elements
        if arr is None:

            check_char_args_method(t_color, b_color, style, "Charray",
            "__init__()")


            # Setting "h" and "w" if they aren't defined
            if height is None:
                h = term_h
            else:
                h = height

            if width is None:
                w = term_w
            else:
                w = width

            # If no array is passed through "arr", generates the array based on
            # the other parameters.
            arr = []
            for i in range(h):
                sub_arr = []
                for j in range(w):
                    sub_arr.append(Char(t_color = t_color, b_color = b_color,
                    style = style))
                arr.append(sub_arr)

        elif arr is not None and (width is not None or height is not None or\
        t_color != "default" or  b_color != "default" or style != "default"):

            # If an array is passed in through "arr", none of the other
            # parameters may be given values otherwise there is a conflict.
            # These conflicts are determined and shown to the user.
            conflicts = []
            if width is not None:
                conflicts.append("\"width\"")
            if height is not None:
                conflicts.append("\"height\"")
            if t_color != "default":
                conflicts.append("\"t_color\"")
            if b_color != "default":
                conflicts.append("\"b_color\"")
            if style != "default":
                conflicts.append("\"style\"")
            if len(conflicts) > 2:
                conflicts.append(conflicts[-1])
                conflicts[-2] = " and "
                conflicts = ", ".join(conflicts[:-2]) + conflicts[-2]\
                + conflicts[-1]
            elif len(conflicts) == 2:
                conflicts = " and ".join(conflicts)
            elif len(conflicts) == 1:
                conflicts = conflicts[0]

            msg = "\n\nIf you wish to generate a Charray by passing another"
            msg += " Charray,\na list, or a tuple via the argument \"arr\","
            msg += " there cannot be any\nconflicting parameters.\n\n"
            msg += "Currently conflicting parameters:\t"
            msg += conflicts + "."

            raise Exception(msg)

        elif not isinstance(arr, (Charray, list, tuple)):

            # Checking if "arr" is not a Charray, list or tuple.  These are
            # the only accepted types.
            raise TypeError(msg)

        elif isinstance(arr, (list, tuple)):
            if len(arr) == 0:
                msg = "Argument \"arr\" in the Charray constructor cannot "
                msg += "be an empty array."
                raise ValueError(msg)

            # If "arr" is a list or tuple, checks it is rectangular and
            # if confirmed, determines the dimensions of "arr" and checks that
            # all elements are Char objects
            if isinstance(arr[0], Char):
                w = 1
                for i in arr[1:]:
                    if not isinstance(i, Char):
                        raise TypeError(msg)
                    w += 1
                h = 1
            elif isinstance(arr[0], (list, tuple)):
                w = len(arr[0])
                h = 1
                for i in arr[1:]:
                    if not isinstance(i, (list, tuple)) or len(i) != w:
                        raise TypeError(msg)
                    for j in i:
                        if not isinstance(j, Char):
                            raise TypeError(msg)
                    h += 1

        self.h = h
        self.w = w
        self.arr = list(arr)
        self.size = (h, w)

    def __getitem__(self, idx):

        if isinstance(idx, int):

            # If the index contains a single integer, returns the subarray
            # at the given index "idx".

            if idx < -self.h or idx >= self.h:
                msg = "\n\nIndex ({:d}, :) is out of bounds for a".format(idx)
                msg += " Charray of size ({:d}, {:d})".format(self.h, self.w)
                raise IndexError(msg)

            if isinstance(self.arr[idx], Char):
                return self.arr[idx]
            else:
                return Charray(arr = self.arr[idx])

        elif isinstance(idx, slice):

            new_arr = []
            for i in range_idx(idx, self.h):
                sub_arr = []
                for j in self.arr[i]:
                    sub_arr.append(j)
                new_arr.append(sub_arr)
            if len(new_arr) == 1 and len(new_arr[0]) == 1:
                return new_arr[0][0]
            else:
                return Charray(arr = new_arr)

        elif isinstance(idx, tuple):

            if len(idx) == 2:
                new_arr = []
                for i in range_idx(idx[0], self.h):
                    sub_arr = []
                    for j in range_idx(idx[1], self.w):
                        sub_arr.append(self.arr[i][j])
                    new_arr.append(sub_arr)
                if len(new_arr) == 1 and len(new_arr[0]) == 1:
                    return new_arr[0][0]
                else:
                    return Charray(arr = new_arr)
            else:
                # If the index given is a tuple, but not of length 2, raises
                # an error which informs that Charrays are 2-D
                msg = "\n\nCharray objects are restricted to 2-Dimensions.\n"
                msg += "Attempted to access with {:d}".format(len(idx))
                msg += "-D index."
                raise IndexError(msg)
        else:
            # If the index is not a tuple or int, informs of this requirement
            msg = "\n\nAttempting to access Charray with invalid index "
            msg += "\"{}\" of {}".format(idx, type(idx))
            raise IndexError(msg)

    def __setitem__(self, idx, new):
        """
            Given an index, replaces a portion of this Charray with the
            Charray or Char "new".
        """
        sub_arr = self.__getitem__(idx)
        if type(sub_arr) != type(new):

            # Making sure the selected sub_array is of the same type as the new
            # replacement sub_array
            msg = "\n\nAttempting to set object of type {}"\
            .format(type(sub_arr))
            msg += " with object of type {}".format(type(new))
            raise TypeError(msg)

        elif isinstance(sub_arr, Char) and isinstance(new, Char):

            # If both are of type Char, wraps around the Char overwrite method
            sub_arr.overwrite(new)

        elif isinstance(new, Charray):

            # If both are of type Charray, checks their dimensions match
            if sub_arr.h != new.h or sub_arr.w != new.w:
                msg = "\n\nDimension mismatch: Expected Charray with shape "
                msg += "({:d}, {:d})".format(sub_arr.h, sub_arr.w)
                msg += "\ninstead got Charray with shape ({:d}, {:d})"\
                .format(new.h, new.w)
                raise ValueError(msg)

            # Runs the overwrite method on each Char that is to be replaced
            for i,j in zip(sub_arr.arr, new.arr):
                for k,l in zip(i,j):
                    k.overwrite(l)

    def __str__(self):
        text = ""
        for i in self.arr:
            for n,j in enumerate(i):
                text += str(j)
            text += "\n"
        return text[:-1]

    def __repr__(self):
        """
            Machine-readable string output
        """
        return self.__str__()

    def __iter__(self):
        """
            Iterates through each element in this Charray, yielding a tuple
            of coordinates followed by the value at that coordinate:

                    C = Charray(...)
                    for (height, width), value in C:
                        ...
        """
        for m,i in enumerate(self.arr):
            for n,j in enumerate(i):
                yield (m,n),j

    def copy(self):
        """
            Returns a copy of the current object.  Use this to avoid issues
            with pointers referring to the same memory location.
        """
        new_arr = []
        for i in range(self.h):
            sub_arr = []
            for j in range(self.w):
                sub_arr.append(self.arr[i][j].copy())
            new_arr.append(sub_arr)
        return Charray(arr = new_arr)

    def save(self):
        """
            Saves the array data to a file, which can be loaded using the
            global function "Load()"
        """
        save_loc = "./data/char_arr/"
        idx = 0
        file1 = None
        file2 = None
        extension1 = ".chs"         # Color and style binary file
        extension2 = ".chc"         # Text data plaintext file

        # Finding a unique filename for a pair of new .chs and .chc files
        while True:
            idx += 1
            file1 = "a{:d}{}".format(idx, extension1)
            file2 = "a{:d}{}".format(idx, extension2)
            if file_exists(file1, save_loc) or file_exists(file2, save_loc):
                continue
            else:
                break

        b = bytearray(0)
        b.append(self.h)
        b.append(self.w)
        text = ""
        for (i,j), k in self.__iter__():
            compact = k.compact()
            text += k.char
            for l in range(3):
                b.append(compact[l])
            if j == self.w-1:
                text += "\n"
        with open(save_loc + file1, "w+b") as outfile:
            outfile.write(b)
        with open(save_loc + file2, "w+") as outfile:
            outfile.write(text)
        return "a{:d}".format(idx)

    def display(self):
        print(self.__str__(), end = "")

def delete_Charray(filename, directory = "./"):
    """
        Given a "filename" (and an optional "directory") will attempt to delete
        the .chc and .chs files associated with the name.

        Returns a tuple (bool, bool) which informs whether or not the files
        existed in the first place, for the .chc and .chs respectively.
    """
    check_type_function(str, filename, "delete_Charray()", "filename")
    check_type_function(str, directory, "delete_Charray()", "directory")

    chc_removed = False
    chs_removed = False

    if file_exists("{}.chc".format(filename), directory):
        os.remove("{}{}.chc".format(directory, filename))
        chc_removed = True

    if file_exists("{}.chs".format(filename), directory):
        os.remove("{}{}.chs".format(directory, filename))
        chs_removed = True

    return chc_removed, chs_removed

def load_Charray(filename, directory = "./"):
    """
        Given a pair of files with extensions .chc and .chs, will load these
        files and return the Char Array saved in these files.
    """

    # Loading color and style data from a .chs file
    with open("{}{}.chs".format(directory, filename), "rb") as infile:
        b = bytearray(infile.read())

    # Loading text data from a .chc file
    text = []
    with open("{}{}.chc".format(directory, filename), "r") as infile:
        for n, line in enumerate(infile):
            text.append(list(line))

    colors = ["k", "r", "g", "y", "b", "p", "c", "w", "d"]
    styles = ["d", "b", "f", "i", "u", "n", "s"]
    i = 0
    C = Charray(height = b[0], width = b[1])
    for h in range(b[0]):
        for w in range(b[1]):
            idx_t = b[2 + 3*i]
            idx_b = b[3 + 3*i]
            idx_s = b[4 + 3*i]
            c = text[h][w]
            C[h,w] = Char(c, colors[idx_t], colors[idx_b], styles[idx_s])
            i += 1
    return C

def display_logo(h = None, w = None):
    """
        Displays the animated termighty logo, and resizes terminal to (h,w)
    """
    # Resize the terminal to the logo size
    set_terminal_size(15, 63)

    # Setting Default Values
    if h is None:
        h = term_h
    if w is None:
        w = term_w

    # Checking that "h" and "w" are of type <int>
    check_type_function(int, h, "display_logo(h,w)", "h")
    check_type_function(int, w, "display_logo(h,w)", "w")

    # Logo Text Layer
    termite  = "                                                               \n"
    termite += "                                                               \n"
    termite += "        _                       _       _     _                \n"
    termite += "       | |                     (_)     | |   | |               \n"
    termite += "       | |_ ___  _ __ _ __  __  _  __ _| |__ | |_ _   _        \n"
    termite += "       | __/ _ \| /_/| '_ \/_ \| |/ _` | '_ \| __| | | |       \n"
    termite += "       | ||  __/| |  | | | | | | | (_| | | | | |_| |_| |       \n"
    termite += "        \__\___||_|  |_| |_| |_|_|\__, |_| |_|\__|\__, |       \n"
    termite += "                                   __/ |           __/ |       \n"
    termite += "                                  |___/           |___/        \n"
    termite += "                                                               \n"
    termite += "                  GUI AND TERMINAL INTERFACE                   \n"
    termite += "                                                               \n"
    termite += "                     Gabriel Cabrera 2018                      "

    # Logo Text Color Layer
    t_color  = "ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd\n"
    t_color += "ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd\n"
    t_color += "ddddddddydddddddddddddddddddddddydddddddydddddydddddddddddddddd\n"
    t_color += "dddddddydydddddddddddddddddddddyyydddddydydddydyddddddddddddddd\n"
    t_color += "dddddddydyydyyyddydyydydyyddyyddyddyydyydyyydydyydydddydddddddd\n"
    t_color += "dddddddydyyydydyydyyyydyydyyydyydyydyydydyydyydyyydydydyddddddd\n"
    t_color += "dddddddydyyddyyyydyddydydydydydydydyyydydydydydyyydyyydyddddddd\n"
    t_color += "ddddddddyyyyyyyyyyyddyyydyyydyyyyyyyyydyyydyyyyyyyyyyydyddddddd\n"
    t_color += "dddddddddddddddddddddddddddddddddddyyydydddddddddddyyydyddddddd\n"
    t_color += "ddddddddddddddddddddddddddddddddddyyyyydddddddddddyyyyydddddddd\n"
    t_color += "ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd\n"
    t_color += "ddddddddddddddddddwwwdwwwdwwwwwwwwdwwwwwwwwwddddddddddddddddddd\n"
    t_color += "ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd\n"
    t_color += "ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd"

    # Logo Background Color Layer
    b_color  = "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy\n"
    b_color += "drpbydddddddddddddddddddddddddddddddddddddddddddddddddddddybprd\n"
    b_color += "drpycdddddddddddddddddddddddddddddddddddddddddddddddddddddcyprd\n"
    b_color += "drybcdddddddddddddddddddddddddddddddddddddddddddddddddddddcbyrd\n"
    b_color += "dypbcdddddddddddddddddddddddddddddddddddddddddddddddddddddcbpyd\n"
    b_color += "drpbcdddddddddddddddddddddddddddddddddddddddddddddddddddddcbprd\n"
    b_color += "drpbcdddddddddddddddddddddddddddddddddddddddddddddddddddddcbprd\n"
    b_color += "drpbcdddddddddddddddddddddddddddddddddddddddddddddddddddddcbprd\n"
    b_color += "drpbcdddddddddddddddddddddddddddddddddddddddddddddddddddddcbprd\n"
    b_color += "drpbydddddddddddddddddddddddddddddddddddddddddddddddddddddybprd\n"
    b_color += "drpycdddddddddddddddddddddddddddddddddddddddddddddddddddddcyprd\n"
    b_color += "drybcdddddddddddddddddddddddddddddddddddddddddddddddddddddcbyrd\n"
    b_color += "dypbcdddddddddddddddddddddddddddddddddddddddddddddddddddddcbpyd\n"
    b_color += "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"

    # Logo Text Style Layer
    style  = "ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd\n"
    style += "ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd\n"
    style += "ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd\n"
    style += "ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd\n"
    style += "ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd\n"
    style += "ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd\n"
    style += "ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd\n"
    style += "ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd\n"
    style += "ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd\n"
    style += "ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd\n"
    style += "ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd\n"
    style += "dddddddddddddddddduuuuuuuuuuuuuuuuuuuuuuuuuuddddddddddddddddddd\n"
    style += "ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd\n"
    style += "ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd"

    # Creating the (h,w) background array
    C = Charray(height = h, width = w)

    # Creating the logo array, which composed of the four layers
    D = design_Charray(termite, t_color, b_color, style)

    # Extracting the column arrays, to animate their colors
    col_1 = vcat([D[1:4,1], D[5:-2,1]])                 # 1ˢᵗ on left
    col_2 = vcat([D[1:3,2], D[4:-3,2], D[-3,2]])        # 2ⁿᵈ on left
    col_3 = vcat([D[1:2,3], D[3:-4,3], D[-3:-1,3]])     # 3ʳᵈ on left
    col_4 = vcat([D[2:-5,4], D[-4:-1,4]])               # 4ᵗʰ on left
    cols_l = [col_1, col_2, col_3, col_4]

    col_5 = vcat([D[1:4,-3], D[5:-2,-3]])               # 1ˢᵗ from right
    col_6 = vcat([D[1:3,-4], D[4:-3,-4], D[-3,-4]])     # 2ⁿᵈ from right
    col_7 = vcat([D[1:2,-5], D[3:-4,-5], D[-3:-1,-5]])  # 3ʳᵈ from right
    col_8 = vcat([D[2:-5,-6], D[-4:-1,-6]])             # 4ᵗʰ from right
    cols_r = [col_5, col_6, col_7, col_8]

    hC = C.h        # Height of background array
    wC = C.w        # Width of background array
    hD = D.h        # Height of logo array
    wD = D.w        # Width of logo array

    # Checking that the terminal size can fit the logo
    if hD > hC or wD > wC:
        msg = "Terminal of size ({},{}) cannot fit logo of size ({},{})"\
        .format(hC, wC, hD, wD)
        raise ValueError(msg)

    # Centering and placing the logo array in the background array
    h_pos = int((hC-hD)/2)
    w_pos = int((wC-wD)/2)
    C[h_pos:h_pos+hD, w_pos:w_pos+wD] = D

    # Colors to rotate through
    colors = ["r", "p", "b", "c", "w", "r", "p", "b"]
    resized = False
    for m in range(8):                      # Main Animation Loop
        for k in range(5):                  # Loop Through Colors
            l = k
            for col in cols_l:
                for (i,j), ch in col:
                    ch.set_b_color(colors[l])   # Changing the left colors
                l += 1
            l = -(k+1)
            for col in cols_r:
                for (i,j), ch in col:
                    ch.set_b_color(colors[l])   # Changing the right colors
                l -= 1
            if m <= 2:
                clear()
                D.display()                     # Displaying the new frame
            elif m > 3:
                if resized is False:
                    set_terminal_size(h, w)     # Resizing to final size
                    resized = True
                C[h_pos:h_pos+hD, w_pos:w_pos+wD] = D
                clear()
                C.display()                     # Displaying the new frame
            wait(0.1)

def design_Charray(chars = None, t_colors = None, b_colors = None,
styles = None):
    """
        Reads three strings containing pseudocode to generate an image.
        This is accomplished with three strings, each arranged in a grid
        with equal sized rows.  Each grid must be of the same size.

        If a single character is passed to any of the arguments, will
        broadcast this character to the dimensions of the image, as long as
        some other string grid is given.

        [1]     "chars":        Contains all the characters in the Charray
                example:
                                "abcd
                                 efgh
                                 ijkl
                                 mnop"

        [2]    "t_colors"      Contains all the individual character colors

                Color codes:
                                black:k    red:r      green:g    yellow:y
                                blue:b     purple:p   cyan:c     white:w

                example:
                                "krgy
                                 bpcw
                                 wwww
                                 gggg"

        [3]     "b_colors"      Contains all the individual background colors

                Color codes:
                                black:k    red:r      green:g    yellow:y
                                blue:b     purple:p   cyan:c     white:w

                example:
                                "wbrb
                                 rcpk
                                 kkkk
                                 wwww"

        [4]     "styles"        Contains the style of each Char in the Array

                Style Codes:
                                bold:b     faded:f    italic:i   underlined:u
                                negative:n            strikethrough:s

                example:
                                "bfiu
                                 bbbb
                                 ffff
                                 iiii"

        Empty spaces leave the default terminal settings in that coordinate.
    """

    # Testing that the arguments are None or of type <str>, and making sure that
    # at least one argument is not None.  Splits <str> args into separate lines.
    func_name = "design_Charray()"
    properties = [chars, t_colors, b_colors, styles]
    names = ["chars", "t_colors", "b_colors", "styles"]
    got_dims = True
    for m,(p,n) in enumerate(zip(properties, names)):
        if p is not None:
            check_type_function(str, p, func_name, n)
            if len(p) != 1:
                got_dims = False
                properties[m] = p.split("\n")
    msg = "Function {} requires at least one <str> argument".format(func_name)
    msg += " of len > 1."
    if got_dims is True:
        raise TypeError(msg)

    # Checking that all arguments are equally sized if not None.
    line_len = None
    lines = None
    msg = "\n\nArgument {} in function {} must be a <str> object"\
    .format(n, func_name)
    msg += "\ncomposed of equal-length lines. Each argument "
    msg += "in {} must also have\nthe same shape as {}.".format(func_name, n)
    for p,n in zip(properties, names):
        if p is not None and len(p) != 1:
            if lines is None:
                lines = len(p)
            elif lines != len(p):
                raise ValueError(msg)
            for line in p:
                if line_len is None:
                    line_len = len(line)
                    continue
                elif line_len != len(line):
                    raise ValueError(msg)

    # Creating an empty Charray to fill with the markdown values
    C = Charray(height = lines, width = line_len)
    chars, t_colors, b_colors, styles = properties
    for i in range(lines):
        for j in range(line_len):

            if chars is not None and len(chars) == 1:
                c = chars[0]
            elif chars is None or chars[i][j] == " ":
                c = None
            else:
                c = chars[i][j]

            if t_colors is not None and len(t_colors) == 1:
                t = t_colors[0]
            elif t_colors is None or t_colors[i][j] == " ":
                t = "default"
            else:
                t = t_colors[i][j]

            if b_colors is not None and len(b_colors) == 1:
                b = b_colors[0]
            elif b_colors is None or b_colors[i][j] == " ":
                b = "default"
            else:
                b = b_colors[i][j]

            if styles is not None and len(styles) == 1:
                s = styles[0]
            elif styles is None or styles[i][j] == " ":
                s = "default"
            else:
                s = styles[i][j]

            C[i,j] = Char(c, t, b, s)
    return C

def big_letter(s, t_color = "default", b_color = "default", style = "default"):
    """
        Takes a <str> object "s" and converts it to an ASCII-art
        character.  Accepts letters and numbers.
    """

    check_type_function(str, s, "letter(s)", "s")
    check_char_args_function(t_color, b_color, style, func = "big_letter(s)")

    letters = {}

    letters["a"]  = "       \n"
    letters["a"] += "       \n"
    letters["a"] += "  __ _ \n"
    letters["a"] += " / _` |\n"
    letters["a"] += "| (_| |\n"
    letters["a"] += " \__,_|\n"
    letters["a"] += "       \n"
    letters["a"] += "       "

    letters["b"]  = " _     \n"
    letters["b"] += "| |    \n"
    letters["b"] += "| |__  \n"
    letters["b"] += "| '_ \ \n"
    letters["b"] += "| |_) |\n"
    letters["b"] += "|_.__/ \n"
    letters["b"] += "       \n"
    letters["b"] += "       "

    letters["c"]  = "      \n"
    letters["c"] += "      \n"
    letters["c"] += "  ___ \n"
    letters["c"] += " / __|\n"
    letters["c"] += "| (__ \n"
    letters["c"] += " \___|\n"
    letters["c"] += "      \n"
    letters["c"] += "      "

    letters["d"]  = "     _ \n"
    letters["d"] += "    | |\n"
    letters["d"] += "  __| |\n"
    letters["d"] += " / _` |\n"
    letters["d"] += "| (_| |\n"
    letters["d"] += " \__,_|\n"
    letters["d"] += "       \n"
    letters["d"] += "       "

    letters["e"]  = "      \n"
    letters["e"] += "      \n"
    letters["e"] += "  ___ \n"
    letters["e"] += " / _ \\\n"
    letters["e"] += "|  __/\n"
    letters["e"] += " \___|\n"
    letters["e"] += "      \n"
    letters["e"] += "      "

    letters["f"]  = "  __ \n"
    letters["f"] += " / _|\n"
    letters["f"] += "| |_ \n"
    letters["f"] += "|  _|\n"
    letters["f"] += "| |  \n"
    letters["f"] += "|_|  \n"
    letters["f"] += "     \n"
    letters["f"] += "     "

    letters["g"]  = "       \n"
    letters["g"] += "       \n"
    letters["g"] += "  __ _ \n"
    letters["g"] += " / _` |\n"
    letters["g"] += "| (_| |\n"
    letters["g"] += " \__, |\n"
    letters["g"] += "  __/ |\n"
    letters["g"] += " |___/ "

    letters["h"]  = " _     \n"
    letters["h"] += "| |    \n"
    letters["h"] += "| |__  \n"
    letters["h"] += "| '_ \ \n"
    letters["h"] += "| | | |\n"
    letters["h"] += "|_| |_|\n"
    letters["h"] += "       \n"
    letters["h"] += "       "

    letters["i"]  = " _ \n"
    letters["i"] += "(_)\n"
    letters["i"] += " _ \n"
    letters["i"] += "| |\n"
    letters["i"] += "| |\n"
    letters["i"] += "|_|\n"
    letters["i"] += "   \n"
    letters["i"] += "   "

    letters["j"]  = "   _ \n"
    letters["j"] += "  (_)\n"
    letters["j"] += "   _ \n"
    letters["j"] += "  | |\n"
    letters["j"] += "  | |\n"
    letters["j"] += "  | |\n"
    letters["j"] += " _/ |\n"
    letters["j"] += "|__/ "

    letters["k"]  = " _    \n"
    letters["k"] += "| |   \n"
    letters["k"] += "| | __\n"
    letters["k"] += "| |/ /\n"
    letters["k"] += "|   < \n"
    letters["k"] += "|_|\_\\\n"
    letters["k"] += "      \n"
    letters["k"] += "      "

    letters["l"]  = " _ \n"
    letters["l"] += "| |\n"
    letters["l"] += "| |\n"
    letters["l"] += "| |\n"
    letters["l"] += "| |\n"
    letters["l"] += "|_|\n"
    letters["l"] += "   \n"
    letters["l"] += "   "

    letters["m"]  = "           \n"
    letters["m"] += "           \n"
    letters["m"] += " _ __ ___  \n"
    letters["m"] += "| '_ ` _ \ \n"
    letters["m"] += "| | | | | |\n"
    letters["m"] += "|_| |_| |_|\n"
    letters["m"] += "           \n"
    letters["m"] += "           "

    letters["n"]  = "       \n"
    letters["n"] += "       \n"
    letters["n"] += " _ __  \n"
    letters["n"] += "| '_ \ \n"
    letters["n"] += "| | | |\n"
    letters["n"] += "|_| |_|\n"
    letters["n"] += "       \n"
    letters["n"] += "       "

    letters["o"]  = "       \n"
    letters["o"] += "       \n"
    letters["o"] += "  ___  \n"
    letters["o"] += " / _ \ \n"
    letters["o"] += "| (_) |\n"
    letters["o"] += " \___/ \n"
    letters["o"] += "       \n"
    letters["o"] += "       "

    letters["p"]  = "       \n"
    letters["p"] += "       \n"
    letters["p"] += " _ __  \n"
    letters["p"] += "| '_ \ \n"
    letters["p"] += "| |_) |\n"
    letters["p"] += "| .__/ \n"
    letters["p"] += "| |    \n"
    letters["p"] += "|_|    "

    letters["q"]  = "       \n"
    letters["q"] += "       \n"
    letters["q"] += "  __ _ \n"
    letters["q"] += " / _` |\n"
    letters["q"] += "| (_| |\n"
    letters["q"] += " \__, |\n"
    letters["q"] += "    | |\n"
    letters["q"] += "    |_|"

    letters["r"]  = "      \n"
    letters["r"] += "      \n"
    letters["r"] += " _ __ \n"
    letters["r"] += "| '__|\n"
    letters["r"] += "| |   \n"
    letters["r"] += "|_|   \n"
    letters["r"] += "      \n"
    letters["r"] += "      "

    letters["s"]  = "     \n"
    letters["s"] += "     \n"
    letters["s"] += " ___ \n"
    letters["s"] += "/ __|\n"
    letters["s"] += "\__ \\\n"
    letters["s"] += "|___/\n"
    letters["s"] += "     \n"
    letters["s"] += "     "

    letters["t"]  = " _   \n"
    letters["t"] += "| |  \n"
    letters["t"] += "| |_ \n"
    letters["t"] += "| __|\n"
    letters["t"] += "| |_ \n"
    letters["t"] += " \__|\n"
    letters["t"] += "     \n"
    letters["t"] += "     "

    letters["u"]  = "       \n"
    letters["u"] += "       \n"
    letters["u"] += " _   _ \n"
    letters["u"] += "| | | |\n"
    letters["u"] += "| |_| |\n"
    letters["u"] += " \__,_|\n"
    letters["u"] += "       \n"
    letters["u"] += "       "

    letters["v"]  = "       \n"
    letters["v"] += "       \n"
    letters["v"] += "__   __\n"
    letters["v"] += "\ \ / /\n"
    letters["v"] += " \ V / \n"
    letters["v"] += "  \_/  \n"
    letters["v"] += "       \n"
    letters["v"] += "       "

    letters["w"]  = "          \n"
    letters["w"] += "          \n"
    letters["w"] += "__      __\n"
    letters["w"] += "\ \ /\ / /\n"
    letters["w"] += " \ V  V / \n"
    letters["w"] += "  \_/\_/  \n"
    letters["w"] += "          \n"
    letters["w"] += "          "

    letters["x"]  = "      \n"
    letters["x"] += "      \n"
    letters["x"] += "__  __\n"
    letters["x"] += "\ \/ /\n"
    letters["x"] += " >  < \n"
    letters["x"] += "/_/\_\\\n"
    letters["x"] += "      \n"
    letters["x"] += "      "

    letters["y"]  = "       \n"
    letters["y"] += "       \n"
    letters["y"] += " _   _ \n"
    letters["y"] += "| | | |\n"
    letters["y"] += "| |_| |\n"
    letters["y"] += " \__, |\n"
    letters["y"] += "  __/ |\n"
    letters["y"] += " |___/ "

    letters["z"]  = "     \n"
    letters["z"] += "     \n"
    letters["z"] += " ____\n"
    letters["z"] += "|_  /\n"
    letters["z"] += " / / \n"
    letters["z"] += "/___|\n"
    letters["z"] += "     \n"
    letters["z"] += "     "

    letters[" "]  = "     \n"
    letters[" "] += "     \n"
    letters[" "] += "     \n"
    letters[" "] += "     \n"
    letters[" "] += "     \n"
    letters[" "] += "     \n"
    letters[" "] += "     \n"
    letters[" "] += "     "

    if s not in letters.keys():
        if s.lower() not in letters.keys():
            msg = "Unsupported character \"{}\" in function \"letter(s)\""\
            .format(s)
            raise ValueError(msg)
        else:
            s = s.lower()
    return design_Charray(letters[s], t_color, b_color, style)

def big_word(s, t_color = "default", b_color = "default", style = "default"):
    """
        Takes a <str> object "s" and converts it to a series of ASCII-art
        characters using big_letter() and hcat().  Accepts letters and numbers.
    """
    check_type_function(str, s, "big_word()", "s")
    check_char_args_function(t_color, b_color, style, func = "big_word(s)")

    alpha_numerical = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n",
    "o","p","q","r","s","t","u","v","w","x","y","z","0","1","2","3","4","5","6",
    "7","8","9"," "]
    letters = []
    msg = "\n\nArgument \"s\" in function \"big_word()\" must be an "
    msg += "alphanumeric string: it may only contain letters and numbers."
    for i in s:
        if i not in alpha_numerical:
            if i.lower() not in alpha_numerical:
                raise ValueError(msg)
            else:
                i = i.lower()
        letters.append(big_letter(i, t_color, b_color, style))
    if len(letters) == 0:
        msg = "\n\nArgument \"s\" in function \"big_word()\" must be a string"
        msg += " containing at least one letter."
        raise ValueError(msg)
    elif len(letters) == 1:
        return letters[0]
    else:
        return hcat(letters)

def hcat(l):
    """
        Takes a list of Charrays "l" and concatenates them horizontally,
        returning a new Charray.

        Attribute Charray.h must be equal in each element of "l".
    """
    # Checking that "l" is of type <list> or <tuple>
    check_type_function((list, tuple), l, "hcat(l)", "l")

    height = None       # The (as of yet unknown) Charray's heights

    # Checking that "msg" is of type <list> and contains at least two elements,
    # each of which must be Charrays; these must all have the same heights.
    msg = "\n\nArgument \"l\" in function \"hcat(l)\" must be a list of "
    msg += "at least two Charrays of equal height."
    if len(l) < 2:
        raise ValueError(msg)

    new_arrs = []       # Will contain the Charrays

    # Checking that the arrays are of equal heights, if so appends them to
    # new_arrs.
    for n,i in enumerate(l):
        if not isinstance(i, Charray):
            raise TypeError(msg)
        elif height is None:
            height = i.h
            new_arrs.append(i.arr.copy())
        elif height != i.h:
            raise ValueError(msg)
        else:
            new_arrs.append(i.arr.copy())

    new_arr = new_arrs[0]
    for i in new_arrs[1:]:
        for n,j in enumerate(i):
            new_arr[n] = new_arr[n] + j

    return Charray(arr = new_arr)

def vcat(l):
    """
        Takes a list of Charrays "l" and concatenates them vertically,
        returning a new Charray.

        Attribute Charray.w must be equal in each element of "l".
    """
    # Checking that "l" is of type <list> or <tuple>
    check_type_function((list, tuple), l, "vcat(l)", "l")

    # Checking that "msg" is of type <list> and contains at least two elements,
    # each of which must be Charrays; these must all have the same widths.
    msg = "\n\nArgument \"l\" in function \"vcat(l)\" must be a list of "
    msg += "at least two Charrays of equal width."
    if len(l) < 2:
        raise ValueError(msg)

    new_arr = None
    width = None

    # Checking that the arrays are of equal widths, if so appends them to
    # new_arrs.
    for n,i in enumerate(l):
        if not isinstance(i, (Charray, Char)):
            raise TypeError(msg)
        elif isinstance(i, Char):
            if width is None or new_arr is None:
                width = 1
                new_arr = [[i]]
            elif width == 1:
                new_arr.append([i])
            else:
                raise ValueError(msg)
        elif isinstance(i, Charray):
            if width is None or new_arr is None:
                width = i.w
                new_arr = i.arr
            elif width != i.w:
                raise ValueError(msg)
            else:
                new_arr += i.arr
    return Charray(arr = new_arr)
