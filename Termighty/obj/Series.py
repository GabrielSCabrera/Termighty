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
            grids           sequence of equal-shaped 'Grid' instances
        '''
        if grids is not None:
            checkers.check_type(grids, arr_types)
