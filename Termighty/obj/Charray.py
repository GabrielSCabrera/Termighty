from ..utils.exceptions import *
from ..utils.config import *
from ..utils.utils import *
from . import Char

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
                    sub_arr.append(Char.Char(t_color = t_color, b_color = b_color,
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
            if isinstance(arr[0], Char.Char):
                w = 1
                for i in arr[1:]:
                    if not isinstance(i, Char.Char):
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
                        if not isinstance(j, Char.Char):
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

            if isinstance(self.arr[idx], Char.Char):
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

        elif isinstance(sub_arr, Char.Char) and isinstance(new, Char.Char):

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
            Returns a copy of the current object.  Use this to avoid
            unintentionally overwriting other objects' data.
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
            load_Charray(filename, directory = "./") function.
        """
        raise NotImplementedError()
        path = os.path.dirname(os.path.abspath(__file__))
        data_loc = os.path.join(path, "/data/")
        charray_loc = os.path.join(data_loc, "/charray/")

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
            if file_exists(file1, charray_loc) or file_exists(file2, charray_loc):
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

        if not os.path.isdir(charray_loc):
            if not os.path.isdir(data_loc):
                os.mkdir(data_loc)
            os.mkdir(charray_loc)
        with open(charray_loc + file1, "w+b") as outfile:
            outfile.write(b)
        with open(charray_loc + file2, "w+") as outfile:
            outfile.write(text)
        return "a{:d}".format(idx)

    def display(self):
        print(self.__str__(), end = "")
