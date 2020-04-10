import numpy as np

from ..data import int_types, str_types, arr_types
from ..data import styles as ANSI_styles
from .Style_Fast import Style_Fast
from ..utils import checkers

class Style(Style_Fast):

    '''
        Subclass of 'Style_Fast' that includes type-checking.  Safer and with
        more informative exceptions than 'Style_Fast', but a lot slower.
    '''

    '''INSTANTIATORS'''

    @classmethod
    def from_arr(cls, arr):
        '''
            PURPOSE
            Returns a new 'Style' instance based on the values given in 'arr'

            PARAMETERS
            arr         <np.ndarray> of integers

            RETURNS
            Instance of 'Style'
        '''
        checkers.check_type_arr(arr, int_types, 'arr', 'from_arr')
        checkers.check_range_arr(arr, 0, 1, 'arr', 'from_arr')
        checkers.check_shape_arr(arr, (len(ANSI_styles),), 'arr', 'from_arr')
        return super().from_arr(arr)

    '''SETTERS'''

    def add(self, *styles):
        '''
            PURPOSE
            Adds new styles to the current instance

            PARAMETERS
            styles          Any number of <str>
        '''
        self.styles_list += self.check_styles(styles)
        self.styles_list = sorted(list(set(self.styles_list)))
        self.update()

    def remove(self, *styles):
        '''
            PURPOSE
            Removes styles in the current instance

            PARAMETERS
            styles          Any number of <str>
        '''
        styles = self.check_styles(styles)
        super().remove(*styles)
