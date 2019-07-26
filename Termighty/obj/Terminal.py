from ..utils.exceptions import *
from ..utils.config import *
from ..utils.utils import *
from ..utils.charrays import *
from .Char import Char
from .Charray import Charray
from .String import String

class Terminal:

    """
        An intermediary for the terminal that allows for easier graphics
        visualization and interactivity.

        All actions are "live" in this object; for example, using __setitem__
        will both reassign one (or more) elements AND display the changes on
        the terminal.
    """

    def __init__(self, height = None, width = None, skip_logo = False):
        """
            Initializes the terminal wrapper by generating text and background
            color arrays representing the terminal's coordinates.
        """
        clear()

        # Setting up the default terminal height and width if the arguments
        # in question are ommitted
        if height is None:
            self.h = term_h
        else:
            self.h = height

        if width is None:
            self.w = term_w
        else:
            self.w = width

        # Preventing User Input
        cursor(False)
        allow_input(False)

        # Displaying the Termighty logo and resizing
        check_type_method(bool, skip_logo, "Terminal", "__init__()",
        "skip_logo")
        if skip_logo is False:
            display_logo(self.h, self.w)
        elif skip_logo is True:
            clear()
            set_terminal_size(self.h, self.w)

        # Initializing the grid
        self.grid = Charray(width = self.w, height = self.h)

    def display(self):
        """
            Calls the "grid" attribute's "display()" method
        """
        self.grid.display()

    def __getitem__(self, idx):
        """
            Gets the "grid" attribute's elements at index/indices "idx"
        """
        return self.grid[idx]

    def __setitem__(self, idx, value):
        """
            Resets the Char or Chars at the given coordinates.
            Accepts <int> or <slice> objects.
            Prints the result onto the screen
        """
        self.grid[idx] = value
        check_type_method((int, slice, tuple), idx, "Terminal",
        "Terminal.refresh()", "idx")
        if isinstance(idx, (int, slice)):
            for i in range_idx(idx):
                print("\033[{};{}H".format(i+1, j+1) + str(self.grid[i,j]))
        elif isinstance(idx, tuple):
            for i in range_idx(idx[0], self.h):
                for j in range_idx(idx[1], self.w):
                    print("\033[{};{}H".format(i+1, j+1) + str(self.grid[i,j]))
        print("\033[{};{}H".format(self.h-1, self.w-1))
