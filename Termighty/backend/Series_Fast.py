import numpy as np

from ..data import str_types, int_types, arr_types, path_types
from .Style_Fast import Style_Fast
from .Pixel_Fast import Pixel_Fast
from .Grid_Fast import Grid_Fast
from ..config import defaults
from ..utils import checkers

class Series_Fast:

    '''CONSTRUCTOR'''

    def __init__(self, grids = None):
        '''
            PURPOSE
            Manages a series of homogenous-shaped 'Grid_Fast' instances

            OPTIONAL PARAMETERS
            grids           instance/sequence of class 'Grid_Fast'
        '''
        if grids is not None:
            if isinstance(grids, Grid_Fast):
                self.grids = [grids]
            elif isinstance(grids, arr_types):
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
            To load an already saved 'Series_Fast' instance from the default
            series directory denoted in 'defaults.py'.

            PARAMETERS
            path        <str> or <pathlib> instance
        '''
        if not str(filename).endswith('.npy'):
            filename += '.npy'
        path = defaults.save_dirs['series'] / filename
        arr = np.load(path).astype(np.uint32)
        grids = np.empty(arr.shape[0], dtype = Grid_Fast)
        for i in range(arr.shape[0]):
            grids[i] = Grid_Fast.from_arr(arr[i])
        return cls(grids)

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
            Allows iteration over the 'Grid_Fast' instances in 'self.grids'

            RETURNS
            instances of 'Grid_Fast'
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
            To set an individual frame (or 'Grid_Fast' instance) or set of
            frames in a 'Series_Fast' instance

            PARAMETERS
            idx         <int> or <slice>
            value       instance of 'Grid_Fast' or 'Series_Fast'
        '''
        idx_map = np.arange(0, self.length_val, dtype = np.int64)[idx]
        if isinstance(idx_map, np.int64) and isinstance(value, Grid_Fast):
            return self.grids.__setitem__(idx, value)
        elif isinstance(idx_map, np.ndarray) and\
             isinstance(value, (Series_Fast,) + arr_types):
            for n, idx in enumerate(idx_map):
                self.grids.__setitem__(idx, value[n])

    '''GETTER METHODS'''

    def __getitem__(self, idx):
        '''
            PURPOSE
            To access an individual frame (or 'Grid_Fast' instance) from a
            'Series_Fast' instance, or a subset of the given series.

            PARAMETERS
            idx         <int> or <slice>

            RETURNS
            instance of 'Grid_Fast' or 'Series_Fast'
        '''
        idx_map = np.arange(0, self.length_val, dtype = np.int64)[idx]
        if isinstance(idx_map, np.int64):
            return self.grids.__getitem__(idx)
        else:
            out = []
            for idx in idx_map:
                out.append(self.grids.__getitem__(idx))
            return self.__class__(out)

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
            array with elements given by 'Pixel_Fast.as_arr'

            RETURNS
            <ndarray>
        '''
        arr = np.zeros((*self.shape, 7 + Style_Fast.arr_len()))
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
            Saves the current 'Series_Fast' instance to file

            PARAMETERS
            filename        <str>
        '''
        path = defaults.save_dirs['series'] / filename
        np.save(path, self.as_arr)
