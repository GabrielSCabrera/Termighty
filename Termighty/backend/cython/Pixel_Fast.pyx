import numpy as np

from ...config import escape_sequence as esc
from ...data import styles as ANSI_styles
from ...data import str_types, int_types
from .Color_Fast import Color_Fast
from .Style_Fast import Style_Fast
from ...config import defaults

cdef class Pixel_Fast(object):

    '''CONSTRUCTOR'''

    def __init__(self, color_t = None, color_b = None, style = None,
                 character = None):
        '''
            PURPOSE
            Basic unit of all graphics displayed in the terminal – may contain
            a foreground color, background color, text style, and character.

            PARAMETERS
            color_t         instance of 'Color_Fast'
            color_b         instance of 'Color_Fast'
            style           instance of 'Style_Fast'
            character       <str>

            WARNING
            Be aware that pixels are twice as tall as they are wide
        '''
        if color_t is None:
            self.color_t_obj =\
            Color_Fast.palette(defaults.color_t)
        else:
            self.color_t_obj = color_t

        if color_b is None:
            self.color_b_obj =\
            Color_Fast.palette(defaults.color_b)
        else:
            self.color_b_obj = color_b

        if style is None:
            self.style_obj = Style_Fast()
        else:
            self.style_obj = style

        if character is None:
            self.char_str = ' '
        else:
            self.char_str = character

        self.update()

    '''INSTANTIATORS'''

    @classmethod
    def from_arr(cls, arr):
        '''
            PURPOSE
            Returns a new 'Pixel_Fast' instance based on the values given in
            'arr'

            PARAMETERS
            arr         <np.ndarray> of integers

            NOTE
            The input array must consist of 8+ integers, mapped as follows:

            arr = [
                   color_t R          Red part of color_t's RGB array
                   color_t G        Green part of color_t's RGB array
                   color_t B         Blue part of color_t's RGB array
                   color_b R          Red part of color_b's RGB array
                   color_b G        Green part of color_b's RGB array
                   color_b B         Blue part of color_b's RGB array
                   style int        Mapped style integer, see ANSI.py
                   ord(char)          Unicode character as an integer
                   styles_1                          Binary style map
                   styles_2                          Binary style map
                     ⋮
                   styles_N                          Binary style map
                  ]

            Where 'N' in 'styles_N' is the number of styles in 'ANSI.py'

            RETURNS
            Instance of 'Pixel_Fast'
        '''
        color_t = Color_Fast(tuple(arr[0:3]))
        color_b = Color_Fast(tuple(arr[3:6]))
        character = chr(arr[6])
        style = Style_Fast.from_arr(arr[7:])
        return cls(color_t, color_b, style, character)

    def copy(self):
        '''
            PURPOSE
            Returns a deep copy of the current 'Pixel_Fast' instance

            RETURNS
            Instance of class 'Pixel_Fast'
        '''
        return self.__class__(self.color_t().copy(), self.color_b().copy(),
                              self.style().copy(), self.char())

    '''SETTERS'''

    cpdef void set_color_t(self, object color):
        '''
            PURPOSE
            Sets the text color 'self.color_t_obj' to a new value and updates
            all necessary attributes

            PARAMETERS
            color           instance of 'Color_Fast'
        '''
        self.color_t_obj = color
        self.update()

    cpdef void set_color_b(self, object color):
        '''
            PURPOSE
            Sets the background color 'self.color_b_obj' to a new value and
            updates all necessary attributes

            PARAMETERS
            color           instance of 'Color_Fast'
        '''
        self.color_b_obj = color
        self.update()

    cpdef void set_style(self, object style):
        '''
            PURPOSE
            Sets the background color 'self.style_obj' to a new value and
            updates all necessary attributes

            PARAMETERS
            style           Instance of 'Style'
        '''
        self.style_obj = style
        self.update()

    cpdef void set_char(self, str character):
        '''
            PURPOSE
            Sets the background color 'self.char_obj' to a new value and
            updates all necessary attributes

            PARAMETERS
            character     <str> of length 1
        '''
        self.char_str = character
        self.update()

    '''GETTERS'''

    cpdef np.uint64_t[:] as_arr(self):
        '''
            PURPOSE
            Returns the current 'Pixel_Fast' instance as an array, which can be
            used to recreate the instance at a later time.

            NOTE
            The output array consists of eight integers, mapped as follows:

            arr = [
                   color_t R          Red part of color_t's RGB array
                   color_t G        Green part of color_t's RGB array
                   color_t B         Blue part of color_t's RGB array
                   color_b R          Red part of color_b's RGB array
                   color_b G        Green part of color_b's RGB array
                   color_b B         Blue part of color_b's RGB array
                   style int        Mapped style integer, see ANSI.py
                   ord(char)          Unicode character as an integer
                  ]

            RETURNS
            <ndarray> of <uint64>
        '''
        arr = np.zeros(7 + len(ANSI_styles.keys()), dtype = np.uint64)
        arr[0:3] = self.color_t_obj.RGB_arr
        arr[3:6] = self.color_b_obj.RGB_arr
        arr[6] = ord(self.char_str)
        arr[7:] = self.style_obj.as_arr()
        return arr

    def __str__(self):
        '''
            PURPOSE
            To return a printable string that displays all the instance's
            aspects (colors, styles, chars.)

            RETURNS
            <str>
        '''
        return self.out

    def __repr__(self):
        '''
            PURPOSE
            To return a printable string that displays all the instance's
            aspects (colors, styles, chars.)

            RETURNS
            out         <str>
        '''
        RGBt = (f'({self.color_t().R():03d} {self.color_t().G():03d} '
                f'{self.color_t().B():03d})')
        RGBb = (f'({self.color_b().R():03d} {self.color_b().G():03d} '
                f'{self.color_b().B():03d})')

        if self.style().styles():
            styles = ', '.join(self.style().styles())
        else:
            styles = 'Empty'

        out = (f'Pixel(Color_t{RGBt}, Color_b{RGBb}, Style({styles}), '
               f'Char(\'{self.char()}\')))')

        return out

    def __hash__(self):
        '''
            PURPOSE
            To return a unique hash for the combined properties of a Pixel
            instance

            RETURNS
            <int>
        '''
        ID = hash(map(hash, (self.color_t(), self.color_b(), self.style(), self.char())))
        return ID

    '''ACCESSORS'''

    cpdef object color_t(self):
        '''
            PURPOSE
            Return the 'Color' instance used to color the terminal text

            RETURNS
            Instance of 'Color'
        '''
        return self.color_t_obj

    cpdef object color_b(self):
        '''
            PURPOSE
            Return the 'Color' instance used to color the terminal text

            RETURNS
            Instance of 'Color'
        '''
        return self.color_b_obj

    cpdef object style(self):
        '''
            PURPOSE
            Return the 'Style' instance used to style the terminal text

            RETURNS
            Instance of 'Style
        '''
        return self.style_obj

    cpdef str char(self):
        '''
            PURPOSE
            Return the current value of attribute 'char_var'

            RETURNS
            <str>
        '''
        return self.char_str

    '''MANAGERS'''

    cpdef void update(self):
        '''
            PURPOSE
            To update the value of the saved output string based on the current
            instance attributes 'color_t_obj', 'color_b_obj', 'style_obj', and
            'char_obj'
        '''
        self.out = esc.format('') + self.color_t_seq() + self.color_b_seq()
        self.out += self.style_seq() + self.char_str

    '''FORMATTERS'''

    cpdef str color_t_seq(self):
        '''
            PURPOSE
            Returns the ANSI escape sequence that sets the text color to the
            attribute 'self.color_t_obj'

            RETURNS
            out         <str>
        '''
        return esc.format(f'38;2;{self.color_t_obj.RGB_arr[0]};{self.color_t_obj.RGB_arr[1]};{self.color_t_obj.RGB_arr[2]}')

    cpdef str color_b_seq(self):
        '''
            PURPOSE
            Returns the ANSI escape sequence that sets the background color to
            attribute 'self.color_b_obj'

            RETURNS
            out         <str>
        '''
        return esc.format(f'48;2;{self.color_b_obj.RGB_arr[0]};{self.color_b_obj.RGB_arr[1]};{self.color_b_obj.RGB_arr[2]}')

    cpdef str style_seq(self):
        '''
            PURPOSE
            Returns the ANSI escape sequence that sets the text style to
            attribute 'self.style_obj'

            RETURNS
            <str>
        '''
        cdef Py_ssize_t i
        cdef str values = ''
        cdef list styles = self.style_obj.styles_list
        cdef int length = len(styles)
        cdef str number
        for i in range(length):
            number = styles[i]
            values += f'{ANSI_styles[number]}'
            if i < length - 1:
                values += ';'
        if length > 0:
            values = esc.format(values)
        return values

    cpdef str end_seq(self):
        '''
            PURPOSE
            To reset the terminal to its default values (i.e. remove all
            custom-implemented colors or styles)

            RETURNS
            <str>
        '''
        return esc.format('')

    '''COMPARATORS'''

    cpdef bint eq(self, object pixel):
        '''
            PURPOSE
            Confirms that the current 'Pixel_Fast' instance has the same
            properties as another instance

            RETURNS
            <bool>
        '''
        if not isinstance(pixel, Pixel_Fast) or self.color_t_obj.ne(pixel.color_t_obj)\
           or self.color_b_obj.ne(pixel.color_b_obj) or self.style_obj.ne(pixel.style_obj)\
           or self.char_str != pixel.char_str:
           return False
        else:
           return True

    cpdef bint ne(self, object pixel):
        '''
            PURPOSE
            Confirms that the current 'Pixel_Fast' instance has properties
            different to another instance

            RETURNS
            <bool>
        '''
        return not self.eq(pixel)

    '''COMPARATOR WRAPPERS'''

    def __eq__(self, pixel):
        '''
            PURPOSE
            Magic method wrapper for method eq().
            Confirms that the current 'Pixel_Fast' instance has the same
            properties as another instance

            RETURNS
            <bool>
        '''
        return self.eq(pixel)

    def __ne__(self, pixel):
        '''
            PURPOSE
            Magic method wrapper for method ne().
            Confirms that the current 'Pixel_Fast' instance has properties
            different to another instance

            RETURNS
            <bool>
        '''
        return self.ne(pixel)
