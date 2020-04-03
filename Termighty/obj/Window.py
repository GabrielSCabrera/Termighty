from ..data import int_types, arr_types
from ..utils import checkers
from .Term import Term
from .Grid import Grid

class Window:

    def __init__(self, shape):
        '''
            PURPOSE
            Displays and manages instances of class 'Grid' – can be displayed
            as subdivisions of 'Term' live sessions.

            PARAMETERS
            shape       <tuple> with two postive <int> elements
        '''
        checkers.check_type(shape, arr_types, 'shape', '__init__')
        checkers.check_type_arr(shape, int_types, 'shape', '__init__')
        checkers.check_range_arr(shape, 1, None, 'shape', '__init__')
        checkers.check_shape_arr(shape, (2,), 'shape', '__init__')

        self.data = Grid.empty(shape)
        self.shape_arr = self.data.shape
        self.height_val = self.shape_arr[0]
        self.width_val = self.shape_arr[1]
        self.live_bool = False
        self.update()
