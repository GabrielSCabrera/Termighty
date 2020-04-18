import numpy as np

from ...data import styles_clear, styles_to_int, int_to_styles
from ...data import int_types, str_types, arr_types
from ...config import escape_sequence as esc
from ...data import styles as ANSI_styles
from ...utils.format import bold

clear_str = ''
for style in styles_clear.values():
    clear_str += f'{style};'
clear_str = clear_str[:-1]
clear_str = esc.format(clear_str)

cdef class Style_Fast(object):

    '''CONSTRUCTORS'''

    def __init__(self, *styles):
        '''
            PURPOSE
            Manages styles that can be applied to text in the terminal

            PARAMETERS
            styles          Any number of <str>
        '''
        if styles is None:
            styles = []
        self.styles_list = sorted(styles)
        self.update()

    '''INSTANTIATORS'''

    @classmethod
    def from_arr(cls, arr):
        '''
            PURPOSE
            Returns a new 'Style_Fast' instance based on the values given in
            'arr'

            PARAMETERS
            arr         <np.ndarray> of integers

            RETURNS
            Instance of 'Style_Fast'
        '''
        styles = []
        for n,i in enumerate(arr):
            if i == 1:
                styles.append(int_to_styles[n])
        return cls(*styles)

    def copy(self):
        '''
            Purpose
            Returns a deep copy of the current instance

            RETURNS
            Instance of 'Style_Fast'
        '''
        return self.__class__(*self.styles())

    '''SETTERS'''

    def add(self, *styles):
        '''
            PURPOSE
            Adds new styles to the current instance

            PARAMETERS
            styles          Any number of <str>
        '''
        self.styles_list += styles
        self.update()

    def remove(self, *styles):
        '''
            PURPOSE
            Removes styles in the current instance

            PARAMETERS
            styles          Any number of <str>
        '''
        for style in styles:
            idx = self.styles_list.index(style)
            del self.styles_list[idx]
        self.update()

    '''GETTERS'''

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

    cpdef np.uint8_t[:] as_arr(self):
        '''
            PURPOSE
            Returns the current instance as an array of integers as given by
            ANSI.py

            RETURNS
            <ndarray> of <uint8>
        '''
        return self.arr

    @classmethod
    def clear(cls):
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
        sample_text = self.sequence + 'Aa Zz 0123' + clear_str
        out = bold('STYLES')
        length = max(len(key) for key in ANSI_styles.keys()) + 1
        length = max(len(out), length)
        out = bold(out) + '\t'

        if not self.styles_list:
            out += 'None'
            return out

        for code, style in zip(self.codes, self.styles_list):
            space = ' '*(length-len(style))
            out += esc.format(code) + style + clear_str + ' '

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
            To return a unique hash for the combined properties of a
            'Style_Fast' instance

            RETURNS
            <int>
        '''
        ID = ''.join(f'{code:02d}' for code in self.codes)
        return int(ID)

    def __len__(self):
        '''
            PURPOSE
            Returns the number of styles in the current instance

            RETURNS
            <int>
        '''
        return len(self.styles_list)

    '''SETTERS'''

    @classmethod
    def arr_len(cls):
        '''
            PURPOSE
            Returns the length of the array returned from 'as_arr'

            RETURNS
            <int>
        '''
        return len(ANSI_styles.keys())

    '''ACCESSORS'''

    cpdef list styles(self):
        '''
            PURPOSE
            Returns a copy of the list of styles currently implemented

            RETURNS
            <list> of <str>
        '''
        return self.styles_list.copy()

    '''MANAGERS'''

    cpdef void update(self):
        '''
            PURPOSE
            Update the ANSI escape sequence that is returned from this instance
        '''
        cdef Py_ssize_t i,j,k
        if not self.styles_list:
            self.sequence = clear_str
            self.codes = []
        else:
            self.styles_list = sorted(list(set(self.styles_list)))
            codes = [ANSI_styles[style] for style in self.styles_list]
            fmt = ''
            for i in range(len(codes)):
                fmt += f'{codes[i]};'
            self.sequence = esc.format(fmt[:-1])
            self.codes = [ANSI_styles[style] for style in self.styles_list]

        self.arr = np.zeros(len(ANSI_styles.keys()), dtype = np.uint8)
        for j in range(len(self.styles_list)):
            k = styles_to_int[self.styles_list[j]]
            self.arr[k] = 1

    '''COMPARATORS'''

    cpdef bint eq(self, style):
        '''
            PURPOSE
            Checks if the given parameter 'style' has the same set of
            applied styles as the current 'Style' instance

            PARAMETERS
            style           Instance of <class 'Style_Fast'>

            RETURNS
            <bool>
        '''
        if self.styles() == style.styles():
            return True
        else:
            return False

    cpdef bint ne(self, style):
        '''
            PURPOSE
            Checks if the given parameter 'style' has a different set of
            applied styles to that of the current 'Style_Fast' instance

            PARAMETERS
            style           Instance of <class 'Style_Fast'>

            RETURNS
            <bool>
        '''
        return not self.eq(style)

    '''COMPARATOR WRAPPERS'''

    def __eq__(self, style):
        '''
            PURPOSE
            Magic method wrapper for method eq().
            Checks if the given parameter 'style' has the same set of
            applied styles as the current 'Style' instance

            PARAMETERS
            style           Instance of <class 'Style_Fast'>

            RETURNS
            <bool>
        '''
        return self.eq(style)

    def __ne__(self, style):
        '''
            PURPOSE
            Magic method wrapper for method ne().
            Checks if the given parameter 'style' has a different set of
            applied styles to that of the current 'Style_Fast' instance

            PARAMETERS
            style           Instance of <class 'Style_Fast'>

            RETURNS
            <bool>
        '''
        return self.ne(style)
