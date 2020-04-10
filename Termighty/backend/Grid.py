from ..data import int_types, str_types, arr_types, path_types
from ..utils import interpreters, checkers
from .Style_Fast import Style_Fast
from .Pixel_Fast import Pixel_Fast
from .Grid_Fast import Grid_Fast
from .Pixel import Pixel

class Grid(Grid_Fast):

    '''
        Subclass of 'Grid_Fast' that includes type-checking.  Safer and with
        more informative exceptions than 'Grid_Fast', but a lot slower.
    '''

    '''CONSTRUCTOR'''

    def __init__(self, data):
        '''
            PURPOSE
            To store and manage a 2-D rectangular grid of 'Pixel' instances

            PARAMETERS
            data            2-D rectangular iterable of Pixels
        '''
        checkers.check_type_arr_2D(data, Pixel_Fast, 'data', 'generate')
        super().__init__(data)

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
        return cls(data)

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
        return super().load(filename)

    '''SETTER METHODS'''

    def __setitem__(self, idx, value):
        '''
            PURPOSE
            Replaces an element or sub-grid of the current instance

            PARAMETERS
            idx             Length 1 or 2 <tuple> containing <int> or <slice>
            value           Instance of 'Pixel_Fast' or 'Grid_Fast'
        '''
        checkers.check_type(value, arr_types + (Pixel_Fast, Grid_Fast), 'value',
                            '__setitem__')
        try:
            super().__setitem__(idx, value)
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
            return super().__getitem__(idx)
        except IndexError:
            msg = f'Attempt to access Pixel or sub-Grid at invalid index {idx}'
            raise IndexError(msg)

    '''SAVING'''

    def save(self, filename):
        '''
            PURPOSE
            Saves the current 'Grid' instance to file

            PARAMETERS
            filename        <str>
        '''
        checkers.check_type(filename, path_types, 'filename', 'save')
        super().save(filename)
