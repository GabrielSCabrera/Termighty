import numpy as np

from ..data import int_types, str_types, arr_types
from ..config import escape_sequence as esc
from ..data import styles as ANSI_styles
from ..utils.format import bold
from .cython import Style_Fast
from ..utils import checkers

class Style(Style_Fast):

    '''
        Subclass of 'Style_Fast' that includes type-checking.  Safer and with
        more informative exceptions than 'Style_Fast', but a lot slower.
    '''

    '''CONSTRUCTORS'''

    def __init__(self, *styles):
        '''
            PURPOSE
            Manages styles that can be applied to text in the terminal

            PARAMETERS
            styles          Any number of <str>
        '''
        styles = list(set(self.check_styles(styles)))
        super().__init__(*styles)

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

    '''SAMPLERS'''

    @classmethod
    def list_styles(cls):
        '''
            PURPOSE
            Returns a human-readable description of all available styles

            RETURNS
            out         <str>
        '''
        out = 'STYLES'
        length = max(len(key) for key in ANSI_styles.keys()) + 1
        length = max(len(out), length)
        out = bold(out) + '\n'
        for key, value in ANSI_styles.items():
            space = ' '*(length-len(key))
            out += space + esc.format(value) + key + cls.clear() + '\n'
        return out

    '''COMPARATORS'''

    @classmethod
    def check_styles(cls, styles):
        '''
            PURPOSE
            Checks that parameter 'styles' is a <str> or list thereof, whose
            elements are also members of the set of keys in ANSI.styles

            PARAMETERS
            styles          <str>

            RETURNS
            <list> of <str>
        '''
        options = list(ANSI_styles.keys())
        if styles in [[], (), None]:
            return []
        elif isinstance(styles, arr_types):

            for style in styles:

                if not isinstance(style, str_types):
                    msg = ('\n\nParameter \'styles\' in \'Style.__init__\' must'
                           ' contain <str> elements that take one or more of '
                           'the following values:\n')
                    for o in options:
                        msg += f'\'{o}\', '
                    msg = msg[:-2]
                    raise TypeError(msg)

                elif style not in options:
                    msg = ('\n\nParameter \'styles\' in \'Style.__init__\' must'
                           ' contain <str> elements that take one or more of '
                           'the following values:\n')
                    for o in options:
                        msg += f'\'{o}\', '
                    msg = msg[:-2]
                    raise ValueError(msg)

            return list(set((styles)))

        elif isinstance(styles, str_types):

            if styles not in options:
                msg = ('\n\nParameter \'styles\' in \'Style.__init__\' must be '
                       'a <str> (or list thereof) that takes one (or more) '
                       'of the following values:\n')
                for o in options:
                    msg += f'\'{o}\', '
                msg = msg[:-2]
                raise ValueError(msg)

            return [styles]

        else:

            msg = ('\n\nParameter \'styles\' in \'Style.__init__\' must be '
                   'a <str> (or list thereof) that takes one (or more) '
                   'of the following values:\n')
            for o in options:
                msg += f'\'{o}\', '
            msg = msg[:-2]

            raise TypeError(msg)
