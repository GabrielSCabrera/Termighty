import numpy as np
import shutil
import time
import sys
import os

from ..data import int_types, str_types, arr_types
from ..config import term_width, term_height
from ..config import escape_sequence as esc
from ..utils import interpreters, checkers
from .Color import Color
from .Style import Style
from .Pixel import Pixel
from .Grid import Grid

class Term:

    '''CLASS ATTRIBUTES'''

    lock_bool = False       # Set to True when any instance is made live
    cursor_bool = True      # Set to True when the cursor is displayed

    '''CONSTRUCTOR'''

    def __init__(self, shape = None):
        '''
            PURPOSE
            Displays and manages instances of class 'Grid'.

            PARAMETERS
            shape       <tuple> containing two elements of <class 'int'>
        '''
        if shape is not None:
            checkers.check_type(shape, arr_types, 'shape', '__init__')
            checkers.check_type_arr(shape, int_types, 'shape', '__init__')
            checkers.check_range_arr(shape, 1, None, 'shape', '__init__')
            checkers.check_shape_arr(shape, (2,), 'shape', '__init__')
        else:
            shape = (term_height, term_width)

        self.data = Grid.empty(shape)
        self.term_shape = tuple(shutil.get_terminal_size())[::-1]
        self.shape_arr = self.data.shape
        self.height_val = self.shape_arr[0]
        self.width_val = self.shape_arr[1]
        self.live_bool = False
        self.update()

    '''INSTANTIATORS'''

    @classmethod
    def from_grid(cls, grid):
        '''
            PURPOSE
            Initializes an instance of 'Term' from a 'Grid' instance

            PARAMETERS
            grid        Instance of class 'Grid'

            RETURNS
            Instance of class 'Term'
        '''
        checkers.check_type(grid, Grid, 'grid', 'from_grid')
        term = cls(grid.shape)
        term.data[:,:] = grid
        term.update()
        return term

    def copy(self):
        '''
            PURPOSE
            Returns a deep copy of the current 'Term' instance

            RETURNS
            Instance of class 'Term'
        '''
        return Term.from_grid(self.data.copy())

    '''SETTERS'''

    def __setitem__(self, idx, value):
        '''
            PURPOSE
            Replaces an element or sub-grid of the current instance

            PARAMETERS
            idx             Length 1 or 2 <tuple> containing <int> or <slice>
            value           Instance of 'Pixel' or 'Grid'
        '''
        try:
            if isinstance(value, Grid):
                self.grid.__setitem__(idx, value.data)
            else:
                self.grid.__setitem__(idx, value)
        except IndexError:
            msg = f'Attempt to access Pixel or sub-Grid at invalid index {idx}'
            raise IndexError(msg)

        self.update()

    @classmethod
    def cursor_to(cls, idx):
        '''
            PURPOSE
            Returns a string that moves the cursor the the given coordinates
            'idx' when printed

            PARAMETERS
            idx         <tuple> of two non-negative <int> values

            RETURNS
            <str>
        '''
        sys.stdout.write(f"\033[{idx[0]};{idx[1]}H")

    @classmethod
    def write_at(cls, idx, pixel):
        '''
            PURPOSE
            Displays the given 'Pixel' instance at the given coordinates 'idx'.

            PARAMETERS
            idx         <tuple> of two non-negative <int> values
            pixel       instance of class 'Pixel'
        '''
        cls.cursor_to(idx)
        sys.stdout.write(pixel.__str__())

    @classmethod
    def cursor_right(cls, N = 1):
        '''
            PURPOSE
            Moves the cursor to the right by N values
        '''
        sys.stdout.write(f'\033[{N}C')

    '''GETTERS'''

    def __getitem__(self, idx):
        '''
            PURPOSE
            Retrieve an element or sub-grid of the current 'Term' instance

            PARAMETERS
            idx             Length 1 or 2 <tuple> containing <int> or <slice>

            RETURNS
            Instance of 'Pixel' or 'Grid'
        '''

        subdata = self.grid.__getitem__(idx)
        return subdata

    def __str__(self):
        '''
            PURPOSE
            Returns a printable string that contains the 'Term' data

            RETURNS
            out         <str>
        '''
        out = ''
        for row in self.grid.data:
            for pixel in row:
                out += pixel.__str__()
            out += '\n'
        return out[:-1]

    def __repr__(self):
        '''
            PURPOSE
            Returns a machine-readable <str> with instance information

            RETURNS
            <str>
        '''
        return f'Term(h={self.height}, w={self.width})'

    '''ACCESSORS'''

    @property
    def grid(self):
        '''
            PURPOSE
            Returns the 'Grid' data of the current 'Term' instance

            RETURNS
            Instance of 'Grid'
        '''
        return self.data

    @property
    def shape(self):
        '''
            PURPOSE
            Returns the shape of the current 'Term' instance

            RETURNS
            shape       <tuple> of length 2 with <int> values
        '''
        return self.shape_arr

    @property
    def size(self):
        '''
            PURPOSE
            Returns the size of the current 'Term' instance

            RETURNS
            <int>
        '''
        return self.data.size

    @property
    def height(self):
        '''
            PURPOSE
            Returns the shape of the current 'Term' instance

            RETURNS
            <int>
        '''
        return self.height_val

    @property
    def width(self):
        '''
            PURPOSE
            Returns the shape of the current 'Term' instance

            RETURNS
            <int>
        '''
        return self.width_val

    '''MANAGERS'''

    @classmethod
    def clear(cls):
        '''
            PURPOSE
            Clears the terminal
        '''
        sys.stdout.write(esc.format(''))
        sys.stdout.flush()
        os.system('clear')

    @classmethod
    def cursor_hide(cls):
        '''
            PURPOSE
            Hides the cursor in the terminal
        '''
        sys.stdout.write('\033[?25l')
        sys.stdout.flush()
        cls.cursor_bool = False

    @classmethod
    def cursor_show(cls):
        '''
            PURPOSE
            Shows the cursor in the terminal
        '''
        sys.stdout.write('\033[?25h')
        sys.stdout.flush()
        cls.cursor_bool = True

    @classmethod
    def sleep(cls, t):
        '''
            PURPOSE
            Sets the terminal to sleep for the given number of seconds

            PARAMETERS
            t           <float> greater than or equal to zero
        '''
        time.sleep(t)

    @property
    def live(self):
        '''
            PURPOSE
            Returns True if the current 'Term' instance is live, False otherwise

            RETURNS
            <bool>
        '''
        return self.live_bool

    @classmethod
    def locked(cls):
        '''
            PURPOSE
            Returns True if the console is locked (because an instance of
            'Term' is currently live) or False if the console is available for
            writing.

            RETURNS
            <bool>
        '''
        return Term.lock_bool

    @classmethod
    def resize_console(cls, shape):
        '''
            PURPOSE
            Resizes the terminal to the new dimensions given in 'shape'

            PARAMETERS
            shape       <tuple> containing two elements of <class 'int'>
        '''
        checkers.check_type_arr(shape, int_types, 'shape', '__init__')
        checkers.check_shape_arr(shape, (2,), 'shape', '__init__')
        print(f'\033[8;{shape[0]};{shape[1]}t', end = '')

    def update(self):
        '''
            PURPOSE
            Updates the console if current 'Term' instance is live
        '''
        if self.live_bool:
            for i in range(0, self.height):
                self.cursor_to((i,0))
                for j in range(0, self.width):
                    sys.stdout.write(self.data[i,j].__str__())

            sys.stdout.flush()

    def __enter__(self):
        '''
            PURPOSE
            Makes the current 'Term' instance live.  Only one instance may be
            live at a time.

            RETURNS
            self
        '''
        if Term.locked():
            msg = ('Attempt to call method \'__enter__\' on instance of '
                   '\'Term\' while another instance is currently live.')
            raise IOError(msg)

        Term.lock_bool = True
        self.live_bool = True
        self.last_data = self.data.copy()
        self.resize_console(self.shape)
        Term.cursor_hide()
        Term.cursor_to((0,0))
        Term.clear()
        self.update()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        '''
            PURPOSE
            Kills the current 'Term' instance's live session after closing of
            context manager.
        '''
        Term.lock_bool = False
        self.live_bool = False
        self.resize_console(self.term_shape)
        Term.clear()
        Term.cursor_show()
