import Termighty as term
from Termighty import *
import time, os

ticker = 0

def run_unit_tests():

    def test(msg = None):
        globals()["ticker"] += 1
        if msg is None:
            msg = "\t{:4d})".format(globals()["ticker"])
        else:
            msg = "\t{:4d})\t".format(globals()["ticker"]) + msg
        print(msg)

    def countdown(msg, t = 3):
        for i in range(t):
            print("\t{} in {}\r".format(msg, 3-i), end = "")
            time.sleep(0.7)
        print("{} done\t\t\t\t".format(msg))

    """                            TEST FOR FUNCTIONS                            """
    # CHECK TYPE
    print("check_type_function(type_exp, obj, func = None, arg = None)")
    test("Single Type Success")
    check_type_function(int, 1)
    test("Multiple Type Success")
    check_type_function((int,float), 1.0)
    test("Single Type Fail")
    try:
        check_type_function(int, "a")
    except TypeError:
        pass
    test("Multiple Type Fail")
    try:
        check_type_function((bool, slice), 2)
    except TypeError:
        pass

    #RANGE IDX
    print("range_idx(idx, arr_len, generator = True)")

    test("\"idx\" as <int> 1")
    expected = [5]
    for i,j in zip(term.range_idx(5, 6), expected):
        assert i == j
    test("\"idx\" as <int> 2")
    expected = [7]
    for i,j in zip(term.range_idx(-1, 7), expected):
        assert i == j
    test("\"idx\" as <int> 3")
    expected = [7]
    try:
        term.range_idx(8, 7)
    except IndexError:
        pass

    test("\"idx\" as <slice> 1")
    expected = [3,4,5,6,7,8]
    for i,j in zip(term.range_idx(slice(3,9), 10), expected):
        assert i == j
    test("\"idx\" as <slice> 2")
    expected = [0,1,2,3,4,5]
    for i,j in zip(term.range_idx(slice(None), 6), expected):
        assert i == j
    test("\"idx\" as <slice> 3")
    expected = [4,5,6,7]
    for i,j in zip(term.range_idx(slice(4,-1, None), 9), expected):
        assert i == j
    test("\"idx\" as <slice> 4")
    expected = [8,7,6,5,4,3]
    for i,j in zip(term.range_idx(slice(8,2,-1), 10), expected):
        assert i == j
    test("\"idx\" as <slice> 5")
    expected = [1,3,5,7]
    for i,j in zip(term.range_idx(slice(1,None,2), 8), expected):
        assert i == j
    test("\"idx\" as <slice> 6")
    expected = [0,1]
    for i,j in zip(term.range_idx(slice(None,-2), 4), expected):
        assert i == j
    test("\"idx\" as <slice> 7")
    expected = [0,2,4]
    for i,j in zip(term.range_idx(slice(None,None,2), 6), expected):
        assert i == j

    # FILE EXISTS
    print("file_exists(filename, directory = \"./\")")
    test("Checking if I exist")
    directory = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(directory, "unit_tests.py")
    assert term.file_exists(path)

    # CLEAR
    print("clear()")
    countdown("Clearing screen")
    term.clear()
    print("\tScreen should have cleared")
    time.sleep(1)

    # GET KEY PRESS
    print("get_key_press(allowed = \"chars\", case_sensitive = False)")
    test("Press a number")
    print("\tEntered: {:s}".format(term.get_key_press("number")))
    test("Press a letter")
    print("\tEntered: {:s}".format(term.get_key_press("letter")))
    test("Press y or n")
    print("\tEntered: {:s}".format(term.get_key_press("yn")))
    test("Press a vowel")
    print("\tEntered: {:s}".format(term.get_key_press(["a","e","i","o","u"])))

    # CONFIRM
    print("confirm(msg = \"Proceed? (Y/N)\", clear_term = True, numbers = False)")
    test("Confirm (y/n)")
    print("\t{}".format(term.confirm("\tYes or No? (Y/N)")))
    test("Confirm (y/n/numbers) ")
    print("\t{}".format(term.confirm("\tENTER A NUMBER or Y/N", numbers = True)))

    # WAIT
    print("wait(t)")
    test("waiting 0 s")
    term.wait(0)
    test("waiting 0.01 s")
    term.wait(0.01)
    test("waiting 0.1 s")
    term.wait(0.1)
    test("waiting 1 s")
    term.wait(1)

    # SET TERMINAL SIZE
    term.clear()
    print("set_terminal_size(h, w)")
    countdown("Shrinking terminal")
    term.set_terminal_size(12, 40)

    countdown("Resetting terminal")
    term.set_terminal_size(24, 80)

    # ALLOW INPUT/CURSOR
    print("allow_input(allow), and cursor(display)")
    test("Disabled cursor and user input")
    term.allow_input(False)
    term.cursor(False)
    countdown("Reenabling")
    test("Reenabled")
    term.allow_input(True)
    term.cursor(True)

    # DISPLAY LOGO
    print("display_logo(h, w)")
    countdown("Displaying logo")
    display_logo(24, 80)
    term.clear()

    # BIG LETTER
    print("big_letter(s, t_color = \"default\", b_color = \"default\", style = \"default\")")
    test("Printing default A")
    big_letter("A").display()
    test("Printing red text R")
    big_letter("R", t_color = "r").display()
    test("Printing blue background with yellow text Z")
    big_letter("Z", t_color = "y", b_color = "b").display()

    # BIG WORD
    print("big_word(s, t_color = \"default\", b_color = \"default\", style = \"default\")")
    test("Printing default Hello World")
    big_word("Hello World").display()
    test("Printing red background black text Haldo")
    big_word("Haldo", t_color = "k", b_color = "r").display()

    # LOAD CHAR ARRAY
    print("load_Charray(filename, directory = \"./\")")
    print("\tFirst should match second:")
    C = Charray(height = 3, width = 60, b_color = "p")
    print(C)
    savename = C.save()
    D = load_Charray(filename = savename, directory = "./data/char_arr/")
    print(D)

    #FILE EXISTS 1
    print("file_exists(filename, directory = \"./\")")
    test("Testing for file that exists")
    assert term.file_exists("{}.chc".format(savename), directory = "./data/char_arr/")
    assert term.file_exists("{}.chs".format(savename), directory = "./data/char_arr/")

    # DELETE CHAR ARRAY
    print("delete_Charray(filename, directory = \"./\")")
    test("Removing the previously generated files")
    delete_Charray(savename, directory = "./data/char_arr/")

    #FILE EXISTS 2
    print("file_exists(filename, directory = \"./\")")
    test("Testing for file that does not exist")
    assert not term.file_exists("{}.chc".format(savename), directory = "./data/char_arr/")
    assert not term.file_exists("{}.chs".format(savename), directory = "./data/char_arr/")

    """                            TESTS FOR CHAR                               """
    print("CHAR TESTS")

    print("\tINITIALIZATION")
    test("Basic")
    c = Char()
    test("Only Char")
    c = Char(c = "C")
    test("All Params")
    c = Char(c = "C", t_color = "b", b_color = "r", style = "u")

    print("\tMETHODS")
    test("Printing")
    print(c)
    test("Copying")
    c2 = c.copy()
    test("Overwriting")
    c.overwrite(c2)
    test("Displaying")
    c.display()
    print()

    """                         TESTS FOR CHAR_ARRAY                            """
    print("CHAR ARRAY TESTS")

    print("\tINITIALIZATION")
    test("Basic")
    C = Charray()
    test("Width and Height")
    C = Charray(width = 10, height = 10)
    test("Text Settings")
    C = Charray(t_color = "r", b_color = "w", style = "b")
    test("All Non-\"arr\" Params")
    C = Charray(10, 10, "k", "c", "s")
    test("Custom 1-D Array")
    arr = [c, c, c, c2, c2, c]
    C = Charray(arr = arr)
    test("Custom 2-D Array")
    arr = [arr, arr, arr]
    C = Charray(arr = arr)

    print("\tGETITEM TESTS")
    test("Integer Single Index")
    a = C[0]
    test("Slice Single Index 0")
    a = C[:]
    test("Slice Single Index 1")
    a = C[0:]
    test("Slice Single Index 2")
    a = C[:3]
    test("Slice Single Index 3")
    a = C[:-1]
    test("Slice Single Index 4")
    a = C[-2:-1]
    test("Slice Single Index 5")
    a = C[0:3]
    test("Slice Single Index 6")
    a = C[0:3:2]
    test("Slice Single Index 7")
    a = C[2:0:-1]

    print("\tSETITEM TESTS")
    test("Setting individual char")
    a[0,0] = c
    flag = Charray(height = 16, width = 44, b_color = "w")
    flag_red_small = Charray(height = 6, width = 12, b_color = "r")
    flag_red_big = Charray(height = 6, width = 24, b_color = "r")
    flag_blue_vert = Charray(height = 16, width = 4, b_color = "b")
    flag_blue_horiz = Charray(height = 2, width = 44, b_color = "b")
    test("Setting Array 1")
    flag[:6, :12] = flag_red_small
    test("Setting Array 2")
    flag[-6:, :12] = flag_red_small
    test("Setting Array 3")
    flag[:6, -24:] = flag_red_big
    test("Setting Array 4")
    flag[-6:, -24:] = flag_red_big
    test("Setting Array 5")
    flag[:, 14:18] = flag_blue_vert
    test("Setting Array 6")
    flag[7:9, :] = flag_blue_horiz

    print("\tMETHODS")
    test("Print")
    print(C)
    test("Copy")
    C.copy()
    test("Display")
    C.display()
    print()

    """COLOR TEST"""
    print("Initializing Color Test: 3\r", end = "")
    time.sleep(1)
    print("Initializing Color Test: 2\r", end = "")
    time.sleep(1)
    print("Initializing Color Test: 1\r", end = "")
    time.sleep(1)
    print("Initializing Color Test")

    colors = ["w", "r", "y", "g", "b", "c", "p", "k"]
    for i in colors:
        a = Charray(b_color = i)
        a.display()
        time.sleep(0.5)
    print()
    flag.display()

    """ALL TESTS SUCCEEDED"""

    print("ALL TESTS SUCCEEDED")
    globals()["ticker"] = 0


if __name__ == "__main__":
    run_unit_tests()
