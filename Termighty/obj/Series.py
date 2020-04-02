import numpy as np

from ..data import str_types, int_types, arr_types
from ..utils import checkers
from .Grid import Grid

class Series:

    def __init__(self, grids = None):
        '''
            PURPOSE
            Manages a series of homogenous-shaped 'Grid' instances

            OPTIONAL PARAMETERS
            grids           instance/sequence of 'Grid'
        '''
        if grids is not None:
            checkers.check_type(grids, arr_types + (Grid, Series))
            if isinstance(grids, Grid):
                self.grids = np.array([grids], dtype = Grid)
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
            elif isinstance(grids, Series):
                return grids.copy()
