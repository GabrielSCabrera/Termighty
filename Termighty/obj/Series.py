import numpy as np

from ..data import str_types, int_types
from .Grid import Grid

class Series:

    def __init__(self, grids = None):
        '''
            PURPOSE
            Manages a series of homogenous-shaped 'Grid' instances

            OPTIONAL PARAMETERS
            grids           sequence of 'Grid' instances of equal shape
        '''
        
