import numpy as np

from ..data import str_types, int_types, arr_types, path_types
from .cython import Series_Fast
from .cython import Grid_Fast
from ..config import defaults
from ..utils import checkers
from .Style import Style
from .Pixel import Pixel
from .Grid import Grid

class Series(Series_Fast):

    '''CONSTRUCTOR'''

    def __init__(self, grids = None):
        '''
            PURPOSE
            Manages a series of homogenous-shaped 'Grid' instances

            OPTIONAL PARAMETERS
            grids           instance/sequence of class 'Grid'
        '''
        if grids is not None:
            checkers.check_type(grids, arr_types + (Grid_Fast,))
            if isinstance(grids, arr_types):
                checkers.check_type_arr(grids, Grid_Fast, 'grids', '__init__')
                shape = None
                for grid in grids:
                    if shape is None:
                        shape = grid.shape
                    elif not np.array_equal(shape, grid.shape):
                        msg = ('Inconsistent \'Grid\' shapes in parameter '
                               '\'grids\'.')
                        raise ValueError(msg)

        super().__init__(grids)

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
        return super().load(filename)

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
        try:
            super().__setitem__(idx, value)
        except IndexError:
            msg = f'Attempt to access Series at invalid index {idx}'
            raise IndexError(msg)

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
        try:
            return super().__getitem__(idx)
        except IndexError:
            msg = f'Attempt to access Series at invalid index {idx}'
            raise IndexError(msg)

    '''SAVING'''

    def save(self, filename):
        '''
            PURPOSE
            Saves the current 'Series' instance to file

            PARAMETERS
            filename        <str>
        '''
        checkers.check_type(filename, path_types, 'filename', 'save')
        super().save(filename)
