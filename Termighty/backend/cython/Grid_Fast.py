from multiprocessing import Pool
import numpy as np

from .Style_Fast import Style_Fast
from .Pixel_Fast import Pixel_Fast
from ...config import defaults
from ...data import arr_types

class Grid_Fast:

    '''CONSTRUCTOR'''

    def __init__(self, data):
        '''
            PURPOSE
            To store and manage a 2-D rectangular grid of 'Pixel' instances

            PARAMETERS
            data            2-D rectangular iterable of Pixels
        '''
        self.data = np.array(data)
        self.shape_arr = self.data.shape
        self.update()

    '''INSTANTIATORS'''

    @classmethod
    def empty(cls, shape):
        '''
            PURPOSE
            Returns a 'Grid_Fast' instance that contains empty 'Pixel_Fast'
            instances and is of given shape 'shape'.

            PARAMETERS
            shape       <tuple> containing two elements of <class 'int'>

            RETURNS
            grid            Instance of class 'Grid_Fast'
        '''
        data = [[Pixel_Fast() for i in range(shape[1])] for j in range(shape[0])]
        return cls(data)

    def copy(self):
        '''
            PURPOSE
            Returns a deep copy of the current 'Grid_Fast' instance

            RETURNS
            Instance of 'Grid_Fast'
        '''
        new_data = np.empty_like(self.data)
        for i in range(new_data.shape[0]):
            for j in range(new_data.shape[1]):
                new_data[i,j] = self.data[i,j].copy()
        return self.__class__(new_data)

    @classmethod
    def load(cls, filename):
        '''
            PURPOSE
            To load an already saved 'Grid_Fast' instance from the default grid
            directory denoted in 'defaults.py'.

            PARAMETERS
            filename        <str> or <pathlib> instance
        '''
        if not filename.endswith('.npy'):
            filename += '.npy'
        path = defaults.save_dirs['grid'] / filename
        arr = np.load(path).astype(np.uint32)
        return cls.from_arr(arr)

    @classmethod
    def from_arr(cls, arr):
        '''
            PURPOSE
            To load a 'Grid_Fast' instance from an array.

            PARAMETERS
            arr        <ndarray>
        '''
        pool = Pool()
        grid = np.empty(arr.shape[:-1], dtype = Pixel_Fast)
        for i in range(arr.shape[0]):
            for n,j in enumerate(pool.imap(Pixel_Fast.from_arr, arr[i])):
                grid[i,n] = j
        return cls(grid)

    '''SETTER METHODS'''

    def __setitem__(self, idx, value):
        '''
            PURPOSE
            Replaces an element or sub-grid of the current instance

            PARAMETERS
            idx             Length 1 or 2 <tuple> containing <int> or <slice>
            value           Instance of 'Pixel_Fast' or 'Grid_Fast'
        '''
        if isinstance(value, Pixel_Fast):
            self.data[idx] = value
        elif isinstance(value, Grid_Fast):
            self.data[idx] = value.data
        elif isinstance(value, arr_types):
            self.data[idx] = value

    '''GETTER METHODS'''

    def __getitem__(self, idx):
        '''
            PURPOSE
            Retrieve an element or sub-grid of the current instance

            PARAMETERS
            idx             Length 1 or 2 <tuple> containing <int> or <slice>

            RETURNS
            Instance of 'Pixel_Fast' or 'Grid_Fast'
        '''

        subdata = self.data[idx]

        if isinstance(subdata, Pixel_Fast):
            return subdata
        elif subdata.ndim == 1:
            return self.__class__(subdata[None,:])
        else:
            return self.__class__(subdata)

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
        arr = np.zeros((*self.shape, 7 + Style_Fast.arr_len()))
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
            Saves the current 'Grid_Fast' instance to file

            PARAMETERS
            filename        <str>
        '''
        path = defaults.save_dirs['grid'] / filename
        np.save(path, self.as_arr)

    '''COMPARATORS'''

    def __eq__(self, grid):
        '''
            PURPOSE
            Checks if all the attributes in 'grid' are the same as the current
            'Grid_Fast' instance

            PARAMETERS
            grid            Instance of class 'Grid_Fast'

            RETURNS
            <bool>
        '''
        if not np.array_equal(self.shape, grid.shape):
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
            current 'Grid_Fast' instance

            PARAMETERS
            grid            Instance of class 'Grid_Fast'

            RETURNS
            <bool>
        '''
        return not self.__eq__(grid)
