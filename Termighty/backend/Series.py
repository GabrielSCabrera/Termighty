import numpy as np

from ..data import str_types, int_types, arr_types, path_types
from ..config import defaults
from ..utils import checkers
from .Style import Style
from .Pixel import Pixel
from .Grid import Grid

class Series:

    '''CONSTRUCTOR'''

    def __init__(self, grids = None):
        '''
            PURPOSE
            Manages a series of homogenous-shaped 'Grid' instances

            OPTIONAL PARAMETERS
            grids           instance/sequence of class 'Grid'
        '''
        if grids is not None:
            checkers.check_type(grids, arr_types + (Grid,))
            if isinstance(grids, Grid):
                self.grids = [grids]
            elif isinstance(grids, arr_types):
                checkers.check_type_arr(grids, Grid, 'grids', '__init__')
                shape = None
                for grid in grids:
                    if shape is None:
                        shape = grid.shape
                    elif not np.array_equal(shape, grid.shape):
                        msg = ('Inconsistent \'Grid\' shapes in parameter '
                               '\'grids\'.')
                        raise ValueError(msg)
                self.grids = list(grids)
            self.shape_arr = (len(self.grids),) + self.grids[0].shape
        else:
            self.grids = []
            self.shape_arr = (0,0,0)

        self.update()

    '''INSTANTIATORS'''

    @classmethod
    def load(cls, filename):
        '''
            PURPOSE
            To load an already saved 'Series' instance from the default 'series'
            directory denoted in 'defaults.py'.

            PARAMETERS
            path        <str> or <pathlib> instance
        '''
        checkers.check_type(filename, path_types, 'filename', 'save')
        if not str(filename).endswith('.npy'):
            filename += '.npy'
        path = defaults.save_dirs['series'] / filename
        arr = np.load(path).astype(np.uint32)
        series = np.empty(arr.shape[0], dtype = Grid)
        for i in range(arr.shape[0]):
            series[i] = Grid.from_arr(arr[i])
        return cls(series)

    '''ITERATORS'''

    def __iter__(self):
        '''
            PURPOSE
            See __next__
        '''
        self.iter_idx = -1
        return self

    def __next__(self):
        '''
            PURPOSE
            Allows iteration over the 'Grid' instances in 'self.grids'

            RETURNS
            instances of 'Grid'
        '''
        self.iter_idx += 1
        if self.iter_idx >= self.length_val:
            raise StopIteration
        else:
            return self.grids.__getitem__(self.iter_idx)

    '''SETTER METHODS'''

    def __setitem__(self, idx, value):
        '''
            PURPOSE
            To set an individual frame (or 'Grid' instance) or set of frames
            in a Series

            PARAMETERS
            idx         <int> or <slice>
            value       instance of 'Grid' or 'Series'
        '''
        checkers.check_type(value, (Grid, Series) + arr_types)

        idx_map = np.arange(0, self.length_val, dtype = np.int64)[idx]
        if isinstance(idx_map, np.int64) and isinstance(value, Grid):
            return self.grids.__setitem__(idx, value)
        elif isinstance(idx_map, np.ndarray) and\
             isinstance(value, (Series,) + arr_types):
            for n, idx in enumerate(idx_map):
                self.grids.__setitem__(idx, value[n])

    '''GETTER METHODS'''

    def __getitem__(self, idx):
        '''
            PURPOSE
            To access an individual frame (or 'Grid' instance) from a Series,
            or a subset of the given series.

            PARAMETERS
            idx         <int> or <slice>

            RETURNS
            instance of 'Grid' or 'Series'
        '''
        idx_map = np.arange(0, self.length_val, dtype = np.int64)[idx]
        if isinstance(idx_map, np.int64):
            return self.grids.__getitem__(idx)
        else:
            out = []
            for idx in idx_map:
                out.append(self.grids.__getitem__(idx))
            return Series(out)

    def __len__(self):
        '''
            PURPOSE
            Returns the length (in Grids) of the current instance

            RETURNS
            <int>
        '''
        return self.length_val

    @property
    def as_arr(self):
        '''
            PURPOSE
            Returns an array representative of the current grid, as a 4-D numpy
            array with elements given by 'Pixel.as_arr'

            RETURNS
            <ndarray>
        '''
        arr = np.zeros((*self.shape, 7 + Style.arr_len()))
        for i in range(self.shape[0]):
            arr[i] = self.grids[i].as_arr
        return arr

    '''ACCESSORS'''

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
        return np.prod(self.shape_arr)

    @property
    def length(self):
        '''
            PURPOSE
            Returns the length (in Grids) of the current instance

            RETURNS
            <int>
        '''
        return self.length_val

    @property
    def height(self):
        '''
            PURPOSE
            Returns the height (per Grid) of the current instance

            RETURNS
            <int>
        '''
        return self.height_val

    @property
    def width(self):
        '''
            PURPOSE
            Returns the width (per Grid) of the current instance

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
        self.length_val = self.shape_arr[0]
        self.height_val = self.shape_arr[1]
        self.width_val = self.shape_arr[2]

    '''SAVING'''

    def save(self, filename):
        '''
            PURPOSE
            Saves the current 'Series' instance to file

            PARAMETERS
            filename        <str>
        '''
        checkers.check_type(filename, path_types, 'filename', 'save')
        path = defaults.save_dirs['series'] / filename
        np.save(path, self.as_arr)
