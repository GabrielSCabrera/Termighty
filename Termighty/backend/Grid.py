from multiprocessing import Pool
import numpy as np

from ..data import int_types, str_types, arr_types, path_types
from ..utils import interpreters, checkers
from ..config import defaults
from .Style import Style
from .Pixel import Pixel
from .Color import Color

class Grid:

    '''CONSTRUCTOR'''

    def __init__(self, data):
        '''
            PURPOSE
            To store and manage a 2-D rectangular grid of 'Pixel' instances

            PARAMETERS
            data            2-D rectangular iterable of Pixels
        '''
        checkers.check_type_arr_2D(data, Pixel, 'data', 'generate')
        self.data = np.array(data, dtype = Pixel)

        self.shape_arr = self.data.shape
        self.update()

    '''INSTANTIATORS'''

    @classmethod
    def empty(cls, shape):
        '''
            PURPOSE
            Returns a 'Grid' instance that contains empty 'Pixel' instances and
            is of given shape 'shape'.

            PARAMETERS
            shape       <tuple> containing two elements of <class 'int'>

            RETURNS
            grid            Instance of class 'Grid'
        '''
        checkers.check_type_arr(shape, int_types, 'shape', '__init__')
        checkers.check_range_arr(shape, 1, None, 'shape', '__init__')

        if len(shape) != 2:
            msg = ('Parameter \'shape\' in \'__init__\' must be a <tuple> of '
                   'length 2 containing integer values greater than zero.')
            raise ValueError(msg)

        data = [[Pixel() for i in range(shape[1])] for j in range(shape[0])]
        return Grid(data)

    def copy(self):
        '''
            PURPOSE
            Returns a deep copy of the current 'Grid' instance

            RETURNS
            Instance of class 'Grid'
        '''
        new_data = np.empty_like(self.data, dtype = Pixel)
        for i in range(new_data.shape[0]):
            for j in range(new_data.shape[1]):
                new_data[i,j] = self.data[i,j].copy()
        return Grid(new_data)

    @classmethod
    def load(cls, filename):
        '''
            PURPOSE
            To load an already saved 'Grid' instance from the default 'grid'
            directory denoted in 'defaults.py'.

            PARAMETERS
            path        <str> or <pathlib> instance
        '''
        checkers.check_type(filename, path_types, 'filename', 'save')
        if not filename.endswith('.npy'):
            filename += '.npy'
        path = defaults.save_dirs['grid'] / filename
        arr = np.load(path).astype(np.uint32)
        return cls.from_arr(arr)

    @classmethod
    def from_arr(cls, arr):
        '''
            PURPOSE
            To load a 'Grid' instance from an array.

            PARAMETERS
            path        <str> or <pathlib> instance
        '''
        pool = Pool()
        grid = np.empty(arr.shape[:-1], dtype = Grid)
        for i in range(arr.shape[0]):
            for n,j in enumerate(pool.imap(Pixel.from_arr, arr[i])):
                grid[i,n] = j
        return Grid(grid)

    '''SETTER METHODS'''

    def __setitem__(self, idx, value):
        '''
            PURPOSE
            Replaces an element or sub-grid of the current instance

            PARAMETERS
            idx             Length 1 or 2 <tuple> containing <int> or <slice>
            value           Instance of 'Pixel' or 'Grid'
        '''
        checkers.check_type(value, arr_types + (Pixel, Grid), 'value',
                            '__setitem__')
        try:
            if isinstance(value, Pixel):
                self.data[idx] = value
            elif isinstance(value, Grid):
                self.data[idx] = value.data
            elif isinstance(value, arr_types):
                self.data[idx] = value
        except IndexError:
            msg = f'Attempt to access Pixel or sub-Grid at invalid index {idx}'
            raise IndexError(msg)

    '''GETTER METHODS'''

    def __getitem__(self, idx):
        '''
            PURPOSE
            Retrieve an element or sub-grid of the current instance

            PARAMETERS
            idx             Length 1 or 2 <tuple> containing <int> or <slice>

            RETURNS
            Instance of 'Pixel' or 'Grid'
        '''

        try:
            subdata = self.data[idx]
        except IndexError:
            msg = f'Attempt to access Pixel or sub-Grid at invalid index {idx}'
            raise IndexError(msg)

        if isinstance(subdata, Pixel):
            return subdata
        elif subdata.ndim == 1:
            return Grid(subdata[None,:])
        else:
            return Grid(subdata)

    def __str__(self):
        '''
            PURPOSE
            Returns a printable string that contains the grid data

            RETURNS
            out         <str>
        '''
        out = ''
        for row in self.data:
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
        return f'Grid(h={self.height}, w={self.width})'

    @property
    def as_arr(self):
        '''
            PURPOSE
            Returns an array representative of the current grid, as a 3-D numpy
            array with elements given by 'Pixel.as_arr'

            RETURNS
            <ndarray>
        '''
        arr = np.zeros((*self.shape, 7 + Style.arr_len()))
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                arr[i,j] = self.data[i,j].as_arr
        return arr

    '''ACCESSORS'''

    @property
    def ndim(self):
        '''
            PURPOSE
            Returns the dimensionality of the current 'Grid' instance

            RETURNS
            <int>
        '''
        return self.ndim_val

    @property
    def shape(self):
        '''
            PURPOSE
            Returns the shape of the current instance

            RETURNS
            shape       <tuple> of length 2 with <int> values
        '''
        return self.shape_arr

    @property
    def size(self):
        '''
            PURPOSE
            Returns the size of the current instance

            RETURNS
            <int>
        '''
        return self.data.size

    @property
    def height(self):
        '''
            PURPOSE
            Returns the height of the current instance

            RETURNS
            <int>
        '''
        return self.height_val

    @property
    def width(self):
        '''
            PURPOSE
            Returns the width of the current instance

            RETURNS
            <int>
        '''
        return self.width_val

    '''MANAGERS'''

    def update(self):
        '''
            PURPOSE
            Updates instance attributes based on the state of 'self.shape_arr'
        '''
        self.height_val = self.shape_arr[0]
        self.width_val = self.shape_arr[1]

        if self.height_val == 1:
            self.ndim_val = 1
        else:
            self.ndim_val = 2

    '''SAVING'''

    def save(self, filename):
        '''
            PURPOSE
            Saves the current 'Grid' instance to file

            PARAMETERS
            filename        <str>
        '''
        checkers.check_type(filename, path_types, 'filename', 'save')
        path = defaults.save_dirs['grid'] / filename
        np.save(path, self.as_arr)

    '''COMPARATORS'''

    def __eq__(self, grid):
        '''
            PURPOSE
            Checks if all the attributes in 'grid' are the same as the current
            'Grid' instance

            PARAMETERS
            grid            Instance of class 'Grid'

            RETURNS
            <bool>
        '''
        if not isinstance(grid, Grid):
            return False
        elif not np.array_equal(self.shape, grid.shape):
            return False

        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                if grid[i,j] != self.__getitem__((i,j)):
                    return False

        return True

    def __neq__(self, grid):
        '''
            PURPOSE
            Checks if any of the attributes in 'grid' are different from the
            current 'Grid' instance

            PARAMETERS
            grid            Instance of class 'Grid'

            RETURNS
            <bool>
        '''
        return not self.__eq__(grid)
