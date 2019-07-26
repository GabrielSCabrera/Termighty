from .config import *
from .exceptions import *

# Processing Tools

def process_idx(idx, arr_len):
    """
        Processes an index, which can be given either as an int or slice.
        Requires the length of the array it will be used on, since processing
        includes:

            [1]     Checking the indices are of type <int> or type <slice>.
            [2]     Checking the indices are not out of bounds.
            [3]     Replacing None values with the explicit indices they
                    represent.
    """

    # Checking that "idx" is of type <int> or type <slice>
    check_type_function((slice, int), idx, "range_idx", "idx")

    # Checks that "arr_len" is of type <int> and greater than one
    msg = "\n\nExpected \"arr_len\" > 0 of type <int>, got {} instead."\
    .format(type(arr_len))
    if not isinstance(arr_len, int):
        raise TypeError(msg)
    elif arr_len < 1:
        raise ValueError(msg)

    if isinstance(idx, int):
        if idx < -arr_len or idx >= arr_len:
            # If the index is of type <int>, will check that it is within the
            # bounds of the array in question and raises an error if it is not.
            msg = "\n\nInvalid attempt to access index {:d}".format(idx)
            msg += " of a length {:d} array".format(arr_len)
            raise IndexError(msg)
        else:
            # If it is in bounds, will set the start stop step parameters values
            # such that applying these to "range" will give a single iteration
            # at index "idx"
            if idx < 0:
                start = arr_len + idx + 1
                stop = arr_len + idx + 2
                step = 1
            else:
                start = idx
                stop = idx + 1
                step = 1

    elif isinstance(idx, slice):
        # Initializing values for "start", "stop", and "step".  Any None
        # values in idx will be replaced by defaults which explicitly define
        # the range of the iteration.

        if idx.start is None:
            start = 0
        else:
            start = idx.start

        if idx.stop is None:
            stop = arr_len
        else:
            stop = idx.stop

        if idx.step is None:
            step = 1
        else:
            step = idx.step

        idx_min = min(start, stop)
        idx_max = max(start, stop)

        # Checking that the indices are not out of bounds by comparing their
        # lowest and highest values to "arr_len".
        msg = "\n\nAttempting to access index "
        msg2 = " for an array of length {:d}.".format(arr_len)
        if idx_min < -arr_len:
            msg += "{:d}".format(idx_min) + msg2
            raise IndexError(msg)
        elif idx_max > arr_len:
            msg += "{:d}".format(idx_max) + msg2
            raise IndexError(msg)

    if start < 0:
        start = arr_len + start
    if stop < 0:
        stop = arr_len + stop

    return start, stop, step

def range_idx(idx, arr_len):
    """
        Creates a generator that will yield each given index one at a time.
    """
    check_type_function((slice, int), idx, "range_idx", "idx")

    # Checks that "arr_len" is of type <int> and greater than one
    msg = "\n\nExpected \"arr_len\" > 0 of type <int>, got {} instead."\
    .format(type(arr_len))
    if not isinstance(arr_len, int):
        raise TypeError(msg)
    elif arr_len < 1:
        raise ValueError(msg)

    start, stop, step = process_idx(idx, arr_len)
    for i in range(start, stop, step):
        yield i

# Filesystem Tools

def file_exists(filename, directory = None):
    """
        Checks if a given file exists in the specified directory.
        Directory must be an absolute path!
    """
    if directory is None:
        directory = os.path.dirname(os.path.abspath(__file__))[:-16]
    path = os.path.join(directory, filename)
    return os.path.isfile(path)

# Interface Tools

def clear():
    """
        Clears the screen, selecting the best method depending on whether
        Windows or a Linux-based system is being used.  If the Linux method
        fails, simply prints a blank line a "term_h" number of times.
    """
    if os_nt is True:
        os.system('cls')
    else:
        try:
            term_command(cmd = 'clear', exit = False)
        except:
            print('\n'*(term_h+1))

def get_key_press(allowed = "char", case_sensitive = False):
    """
        Overrides the terminal and wait for a key input.  Once the key is
        detected, AND this key is allowed by the "allowed" parameter,
        returns the key.  If it is not allowed, waits until a valid key is
        pressed.

        If "case_sensitive" is False, will ignore SHIFT and CAPSLOCK and simply
        return the lowercase version of the input.

        Options for "allowed":

            [1]     "all"       Anything
            [2]     "char"      Any character
            [3]     "letter"    Any letter
            [4]     "number"    Any number
            [5]     "wasd"      W A S or D
            [6]     "yn"        Y or N
            [7]     <list>      Custom list of single-length strings
    """
    # Checking that case_sensitive is a bool
    check_type_function(bool, case_sensitive, "get_key_press()",
    "case_sensitive")

    # Preparing the allowed inputs
    chars = []
    if allowed == "char":

        # The alphabet and all digits
        chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b",
        "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
        "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D",
        "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R",
        "S", "T", "U", "V", "W", "X", "Y", "Z"]

    elif allowed == "letter":

        # The alphabet
        chars = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
        "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N",
        "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

    elif allowed == "number":

        # All digits
        chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    elif allowed == "wasd":

        # Gaming setup
        chars = ["w", "a", "s", "d", "W", "A", "S", "D"]

    elif allowed == "yn":

        # Confirmation
        chars = ["y", "n", "Y", "N"]

    elif isinstance(allowed, list):

        # Checking if all elements of "allowed" are single-length strings
        msg = "\n\nArgument \"allowed\" in function \"get_key_press()\" expects"
        msg += " a list of length one <str> objects.\n"
        for c in chars:
            if not isinstance(c, str):
                msg += "Got a list with an element of type {}".format(type(c))
                raise TypeError(msg)
            elif len(c) != 1:
                msg += "Got a list with a <str> of length {:d}".format(len(c))
                raise ValueError(msg)

        chars = allowed

    # Value Check
    elif allowed != "all":
        msg = "\n\nArgument \"allowed\" in function \"get_key_press()\""
        msg += " is restricted to the following values:\n\t\"all\", \"char\","
        msg += " \"letter\", \"number\", \"wasd\", and \"yn\"\nA custom list"
        msg += " of single-character <str> objects may also be used."
        raise ValueError(msg)

    os.system("stty raw -echo")
    while True:
        key = sys.stdin.read(1)
        if allowed == "all":
            break
        elif case_sensitive is False:
            if key.lower() in chars:
                break
        elif case_sensitive is True:
            if key in chars:
                break

    os.system("stty -raw echo")
    return key

def confirm(msg = "Proceed? (Y/N)", clear_term = True, numbers = False):
    """
        Asks the user for confirmation to proceed; accepts "y" and "n" by
        default, but can also accept digits if "number" is set to True.
    """
    # Checking if "msg" is a valid string or None
    check_type_function((str, None), msg, "confirm()", "msg")

    #Checking if "clear_term" is a bool:
    check_type_function(bool, clear_term, "confirm()", "clear_term")

    #Checking if "numbers" is a bool:
    check_type_function(bool, numbers, "confirm()", "numbers")

    if clear_term is True:
        clear()
    if msg is not None and msg != "":
        print(msg)
    if numbers is False:
        result = get_key_press(allowed = "yn")
    else:
        result = get_key_press(allowed = ["y", "n", "Y", "N", "0", "1", "2",
        "3", "4", "5", "6", "7", "8", "9"])
    if result == 'y':
        return True
    elif result == 'n':
        return False
    else:
        if numbers is True:
            try:
                return int(result)
            except:
                return None

def wait(t):
    """
        The system sleeps for the given amount of time "t" in seconds
    """
    check_type_function((int, float), t, "wait()", "t")
    time.sleep(t)

# Terminal Modifier

def set_terminal_size(h, w):
    """
        Changes the size of the terminal to the specified arguments height "h"
        and width "w".
    """
    check_type_function(int, h, "set_terminal_size()", "h")
    check_type_function(int, w, "set_terminal_size()", "w")
    sys.stdout.write("\x1b[8;{};{}t".format(h, w))

    # Updating the global variables
    globals()["term_h"] = h
    globals()["term_w"] = w

def allow_input(allow):
    """
        If "allow" is True, displays entered text on terminal,
        if false, intercepts all input and prevents it from displaying.
    """
    check_type_function(bool, allow, "allow_input()", "allow")
    if allow is False:
        os.system("stty -echo")
        globals()["input_allowed"] = False
    elif allow is True:
        os.system("stty echo")
        globals()["input_allowed"] = True

def cursor(display):
    """
        If "display" is True, shows the cursor in the terminal,
        if False, removes the cursor from the terminal.
    """
    check_type_function(bool, display, "cursor()", "display")
    if display is False:
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()
        globals()["cursor_allowed"] = False
    elif display is True:
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
        globals()["cursor_allowed"] = True

def cleanup():
    """
        To be run on exit, clears the screen, allows access to the cursor,
        allows user input, and resets the terminal size.
    """
    import atexit
    def close_Termighty():
        cursor(True)
        allow_input(True)
        set_terminal_size(24, 80)
        os.system("tput reset")
    atexit.register(close_Termighty)        # Runs cleanup() on exit
