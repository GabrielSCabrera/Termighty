from ..data import int_types, str_types, arr_types, path_types
from ..backend import Grid_Fast, Pixel_Fast, Color_Fast
from .Color_Map import Color_Map
from ..utils import checkers

class Gradient(Grid_Fast):

    def __init__(self, shape, color_map):
        '''
            PURPOSE
            Wrapper for 'Grid_Fast' that can be used to treat the pixels as
            mathematical points whose values are colors based on a given color
            map and mathematical function.

            WARNING
            Should not be instantiated directly; a subclass should inherit
            'Gradient' and implement a mathematical function that implements the
            '__call__' magic method for two positional parameters 'x' and 'y'
            and an optional time parameter 't'.

            PARAMETERS
            shape       <tuple> containing two elements of <class 'int'>
            color_map   instance of 'Color_Map'
        '''
        checkers.check_type_arr(shape, int_types, 'shape', '__init__')
        checkers.check_shape_arr(shape, (2,), 'shape', '__init__')
        checkers.check_range_arr(shape, 1, None, 'shape', '__init__')
        checkers.check_type(color_map, Color_Map)

        self.color_map = color_map
        data = [[Pixel_Fast() for i in range(shape[1])] for j in range(shape[0])]
        super().__init__(data)

    def __call__(self, x, y, t = 0):
        '''
            PURPOSE
            Not implemented for 'Gradient', which is an abstract superclass.
            Should be implemented in subclasses of 'Gradient' with the same
            parameters as above.

            PARAMETERS
            x           numerical value (implemented by user)
            y           numerical value (implemented by user)
            t           numerical value (implemented by user)

            RETURNS
            z           real-valued number (implemented by user)
        '''
        msg = ('\nClass \'Gradient\' is an abstract class that must be '
               'inherited.  Create a subclass with a \'__call__\' method and '
               'use that instead.')
        raise NotImplementedError(msg)
