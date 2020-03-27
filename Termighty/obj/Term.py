import numpy as np
import shutil

from ..utils import interpreters, checkers
from ..config import term_width, term_height
from .Color import Color
from .Style import Style
from .Pixel import Pixel
from .Grid import Grid

class Term:

    lock_bool = False       # Set to True when a single instance is made live

    def __init__(self, shape = None):
        '''
            PURPOSE
            Displays and manages instances of class 'Grid'.

            PARAMETERS
            shape       <tuple> containing two elements of <class 'int'>
        '''
        if shape is not None:
            checkers.check_type_arr(shape, (int, np.int64), 'shape', '__init__')
            if len(shape) != 2:
                msg = 'Parameter \'shape\' in \'__init__\' must be of length 2'
                raise ValueError(msg)
        else:
            shape = (term_height, term_width)

        self.data = Grid.empty(shape)
        self.term_shape = shutil.get_terminal_size()
        self.shape_arr = self.data.shape
        self.height_val = self.shape_arr[0]
        self.width_val = self.shape_arr[1]
        self.live_bool = False
        self.update()

    @staticmethod
    def from_grid(grid):
        '''
            PURPOSE
            Initializes an instance of 'Term' from a 'Grid' instance

            PARAMETERS
            grid        Instance of class 'Grid'

            RETURNS
            Instance of class 'Term'
        '''
        checkers.check_type(grid, Grid, 'grid', 'from_grid')
        term = Term(grid.shape)
        term.data[:,:] = grid
        term.update()
        return term

    @staticmethod
    def locked():
        '''
            PURPOSE
            Returns True if the console is locked (because an instance of
            'Term' is currently live) or False if the console is available for
            writing.

            RETURNS
            <bool>
        '''
        return Term.lock_bool

    @staticmethod
    def resize_console(shape):
        '''
            PURPOSE
            Resizes the terminal to the new dimensions given in 'shape'

            PARAMETERS
            shape       <tuple> containing two elements of <class 'int'>
        '''
        checkers.check_type_arr(shape, (int, np.int64), 'shape', '__init__')
        if len(shape) != 2:
            msg = 'Parameter \'shape\' in \'__init__\' must be of length 2'
            raise ValueError(msg)
        print(f'\033[8;{shape[0]};{shape[1]}t', end = '')

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

    @property
    def live(self):
        '''
            PURPOSE
            Returns True if the current 'Term' instance is live, False otherwise

            RETURNS
            <bool>
        '''
        return self.live_bool

    def update(self):
        '''
            PURPOSE
            Updates the console if current 'Term' instance is live
        '''
        pass

    def copy(self):
        '''
            PURPOSE
            Returns a deep copy of the current 'Term' instance

            RETURNS
            Instance of class 'Term'
        '''
        return Term.from_grid(self.data.copy())

    def __getitem__(self, idx):
        '''
            PURPOSE
            Retrieve an element or sub-grid of the current 'Term' instance

            PARAMETERS
            idx             Length 1 or 2 <tuple> containing <int> or <slice>

            RETURNS
            Instance of 'Pixel' or 'Grid'
        '''

        try:
            subdata = self.grid.data[idx]
        except IndexError:
            msg = f'Attempt to access Pixel or sub-Grid at invalid index {idx}'
            raise IndexError(msg)

        if isinstance(subdata, Pixel):
            return subdata
        elif subdata.ndim == 1:
            return Grid(subdata[None,:])
        else:
            return Grid(subdata)

    def __setitem__(self, idx, value):
        '''
            PURPOSE
            Replaces an element or sub-grid of the current instance

            PARAMETERS
            idx             Length 1 or 2 <tuple> containing <int> or <slice>
            value           Instance of 'Pixel' or 'Grid'
        '''
        if not isinstance(value, (Pixel, Grid, list, tuple, np.ndarray)):
            msg = ('Parameter \'value\' in \'__setitem__\' must be an instance '
                   'of class \'Pixel\'/\'Grid\', or an iterable of \'Pixels\'')
            raise ValueError(msg)

        try:
            if isinstance(value, Pixel):
                self.grid.data[idx] = value
            elif isinstance(value, Grid):
                self.grid.data[idx] = value.data
            elif isinstance(value, (list, tuple, np.ndarray)):
                self.grid.data[idx] = value
        except IndexError:
            msg = f'Attempt to access Pixel or sub-Grid at invalid index {idx}'
            raise IndexError(msg)

        self.update()

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

    def __enter__(self):
        '''
            PURPOSE
            Makes the current 'Term' instance live.  Only one instance may be
            live at a time.

            RETURNS
            self
        '''
        if self.locked():
            msg = ('Attempt to call method \'__enter__\' on instance of '
                   '\'Term\' while another instance is currently live.')
            raise IOError(msg)

        Term.lock_bool = True
        self.live_bool = True
        self.resize_console(self.shape)
        self.update()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        '''
            PURPOSE
            Kills the current 'Term' instance after closing of context manager.
        '''
        self.resize_console(self.term_shape)
        Term.lock_bool = False
        self.live_bool = False
