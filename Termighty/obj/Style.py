from numba import jitclass, int8

from ..data import styles_clear, styles_to_int, int_to_styles
from ..data import int_types, str_types, arr_types
from ..config import escape_sequence as esc
from ..utils import interpreters, checkers
from ..data import styles as ANSI_styles
from ..utils.format import bold

import numpy as np

class Style:

    '''CONSTRUCTOR'''

    def __init__(self, *styles):
        '''
            PURPOSE
            Manages styles that can be applied to text in the terminal

            PARAMETERS
            styles          Any number of <str>
        '''
        self.styles_list = sorted(list(set(self.check_styles(styles))))
        self.update()

    def from_arr(arr):
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
        styles = []
        for n,i in enumerate(arr):
            if i == 1:
                styles.append(int_to_styles[n])
        return Style(*styles)

    '''SETTER METHODS'''

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
        for style in styles:
            if style in self.styles_list:
                idx = self.styles_list.index(style)
                del self.styles_list[idx]
        self.update()

    def update(self):
        '''
            PURPOSE
            Update the ANSI escape sequence that is returned from this instance
        '''
        if not self.styles_list:
            self.sequence = self.clear()
            self.codes = []
        else:
            codes = [ANSI_styles[style] for style in self.styles_list]
            fmt = ''
            for code in codes:
                fmt += f'{code};'
            fmt = fmt[:-1]
            self.sequence = esc.format(fmt)
            self.codes = [ANSI_styles[style] for style in self.styles_list]

        self.arr = np.zeros(len(ANSI_styles.keys()), dtype = np.uint8)
        for style in self.styles_list:
            n = styles_to_int[style]
            self.arr[n] = 1

    '''GETTER METHODS'''

    @staticmethod
    def list_styles():
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
            out += space + esc.format(value) + key + Style.clear() + '\n'
        return out

    @property
    def styles(self):
        '''
            PURPOSE
            Returns a copy of the list of styles currently implemented

            RETURNS
            <list> of <str>
        '''
        return self.styles_list.copy()

    def copy(self):
        '''
            Purpose
            Returns a deep copy of the current instance

            RETURNS
            Instance of 'Style'
        '''
        return Style(*self.styles)

    def __call__(self, string):
        '''
            PURPOSE
            Returns the given string with the current style configuration

            PARAMETERS
            string      <str>

            RETURNS
            out         <str>
        '''
        out = self.sequence + string + self.clear()
        return out

    @property
    def as_arr(self):
        '''
            PURPOSE
            Returns the current instance as an array of integers as given by
            ANSI.py

            RETURNS
            <ndarray> of <uint8>
        '''
        return self.arr

    @staticmethod
    def clear():
        '''
            PURPOSE
            Return an ANSI escape sequence that clears all styles

            RETURNS
            out         <str>
        '''
        fmt = ''
        for style in styles_clear.values():
            fmt += f'{style};'
        fmt = fmt[:-1]
        return esc.format(fmt)

    def __str__(self):
        '''
            PURPOSE
            Returns a human-readable description of the styles implemented
            in the instance

            RETURNS
            out         <str>
        '''
        sample_text = self.sequence + 'Aa Zz 0123' + self.clear()
        out = bold('STYLES')
        length = max(len(key) for key in ANSI_styles.keys()) + 1
        length = max(len(out), length)
        out = bold(out) + '\t'

        if not self.styles_list:
            out += 'None'
            return out

        for code, style in zip(self.codes, self.styles_list):
            space = ' '*(length-len(style))
            out += esc.format(code) + style + self.clear() + ' '

        out += f'\n{bold("SAMPLE")}\t{sample_text}'

        return out

    def __repr__(self):
        '''
            PURPOSE
            Machine readable string output with instance information

            RETURNS
            <str>
        '''
        if not self.styles_list:
            return f'Style(Empty)'
        else:
            return f'Style({", ".join(self.styles_list)})'

    def __hash__(self):
        '''
            PURPOSE
            To return a unique hash for the combined properties of a Style
            instance

            RETURNS
            <int>
        '''
        ID = ''.join(f'{code:02d}' for code in self.codes)
        return hash(ID)

    '''COMPARATORS'''

    @staticmethod
    def check_styles(styles):
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

    def __eq__(self, style):
        '''
            PURPOSE
            Checks if the given parameter 'style' has the same set of
            applied styles as the current 'Style' instance

            PARAMETERS
            style           Instance of <class 'Style'>

            RETURNS
            <bool>
        '''
        if self.styles == style.styles:
            return True
        else:
            return False

    def __neq__(self, style):
        '''
            PURPOSE
            Checks if the given parameter 'style' has a different set of
            applied styles to that of the current 'Style' instance

            PARAMETERS
            style           Instance of <class 'Style'>

            RETURNS
            <bool>
        '''
        if self.styles != style.styles:
            return True
        else:
            return False

    def __len__(self):
        '''
            PURPOSE
            Returns the number of styles in the current instance

            RETURNS
            <int>
        '''
        return len(self.styles_list)
