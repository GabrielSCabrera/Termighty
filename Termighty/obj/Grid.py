import numpy as np

from ..utils import interpreters, checkers
from ..config import defaults
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
        self.height_val = self.shape_arr[0]
        self.width_val = self.shape_arr[1]

        # The grid that will contain each 'Pixel' instance
        self.data = np.empty((self.height_val, self.width_val), dtype = Pixel)

    @classmethod
    def empty(self, shape):
        '''
            PURPOSE
            Returns a 'Grid' instance that contains empty 'Pixel' instances and
            is of given shape 'shape'.

            PARAMETERS
            shape       <tuple> containing two elements of <class 'int'>

            RETURNS
            grid            Instance of class 'Grid'
        '''
        checkers.check_type_arr(shape, (int, np.int64), 'shape', '__init__')
        checkers.check_range_arr(shape, 1, None, 'shape', '__init__')

        if len(shape) != 2:
            msg = ('Parameter \'shape\' in \'__init__\' must be a <tuple> of '
                   'length 2 containing integer values greater than zero.')
            raise ValueError(msg)

        data = [[Pixel() for i in range(shape[1])] for j in range(shape[0])]
        return Grid(data)

    '''GETTERS'''

    @property
    def shape(self):
        '''
            PURPOSE
            Returns the shape of the current instance

            RETURNS
            shape       <tuple> of length 2 with <int> values
        '''
        return self.shape_arr.copy

    @property
    def height(self):
        '''
            PURPOSE
            Returns the shape of the current instance

            RETURNS
            <int>
        '''
        return self.height_val

    @property
    def width(self):
        '''
            PURPOSE
            Returns the shape of the current instance

            RETURNS
            <int>
        '''
        return self.width_val

    def __getitem__(self, idx):
        '''
            PURPOSE
            Retrieve an element or sub-grid
        '''
