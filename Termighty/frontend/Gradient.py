from ..data import int_types, str_types, arr_types, path_types, real_types
from ..backend import Grid_Fast, Pixel_Fast, Color_Fast
from .Color_Map import Color_Map
from ..utils import checkers

class Gradient(Grid_Fast):

    def __init__(self, shape, xrange, yrange, color_map):
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
            xrange      <tuple> containing two elements of <class 'int'>
            yrange      <tuple> containing two elements of <class 'int'>
            color_map   instance of 'Color_Map'
        '''
        checkers.check_type_arr(xrange, real_types, 'xrange', '__init__')
        checkers.check_type_arr(yrange, real_types, 'yrange', '__init__')
        checkers.check_type_arr(shape, int_types, 'shape', '__init__')

        checkers.check_shape_arr(xrange, (2,), 'shape', '__init__')
        checkers.check_shape_arr(yrange, (2,), 'shape', '__init__')
        checkers.check_shape_arr(shape, (2,), 'shape', '__init__')

        if xrange[0] >= xrange[1] or yrange[0] > yrange[1]:
            msg = ('The first elements of \'xrange\' and \'yrange\' must be '
                   'less than their second elements.')
            raise ValueError(msg)

        checkers.check_range_arr(shape, 1, None, 'shape', '__init__')
        checkers.check_type(color_map, Color_Map)

        self.color_map = color_map
        self.xrange = np.linspace(xrange[0], xrange[1], shape[0])
        self.yrange = np.linspace(yrange[0], yrange[1], shape[1])
        data = [[Pixel_Fast() for i in self.xrange] for j in self.yrange]
        super().__init__(data)

    # def set_xrange(self, x_slice):
    #     '''
    #         PURPOSE
    #         To set the values of the instance's x-axis
    #
    #         PARAMETERS
    #         x_slice         <slice>
    #     '''
    #     checkers.check_type(x_slice, slice)
    #     self.x =

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

    def update(self):
        '''
            PURPOSE
            Updates instance attributes based on the state of the instance
            attributes.
        '''
