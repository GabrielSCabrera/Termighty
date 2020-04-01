from ..config import escape_sequence as esc
from ..utils import interpreters, checkers
from ..data import styles as ANSI_styles
from ..config import defaults
from .Color import Color
from .Style import Style

import numpy as np

class Pixel:

    '''CONSTRUCTOR'''

    def __init__(self, color_t = None, color_b = None, style = None, char = None):
        '''
            PURPOSE
            Basic unit of all graphics displayed in the terminal – may contain
            a foreground color, background color, text style, and character.

            PARAMETERS
            color_t         <tuple> of 3 <int> values in range [0,255] OR
                            instance of <class 'Color'> OR a <str> color label
            color_b         <tuple> of 3 <int> values in range [0,255] OR
                            instance of <class 'Color'> OR a <str> color label
            style           <str>, <list> of <str>, or instance of class 'Style'
            char            <str>

            WARNING
            Be aware that pixels are twice as tall as they are wide
        '''
        if color_t is None:
            self.color_t_obj =\
            Color.palette(defaults.color_t)
        else:
            self.color_t_obj =\
            interpreters.get_color(color_t)

        if color_b is None:
            self.color_b_obj =\
            Color.palette(defaults.color_b)
        else:
            self.color_b_obj =\
            interpreters.get_color(color_b)

        if style is None:
            self.style_obj = Style()
        else:
            self.style_obj =\
            interpreters.get_style(style)

        if char is None:
            self.char_str = ' '
        else:
            self.is_char(char)
            self.char_str = char

        self.update()

    @staticmethod
    def is_char(char):
        '''
            PURPOSE
            Confirms that 'char' is a single-character <str>, or raises an
            Exception

            RETURNS
            True
        '''
        checkers.check_type(char, str, 'char', 'is_char')
        if len(char.__repr__()) != 3:
            msg = '\n\nParameter \'char\' should be a one-character <str>'
            raise ValueError(msg)
        return True

    @staticmethod
    def from_arr(arr):
        '''
            PURPOSE
            Given an array of TBDDDDD
        '''

    '''UPDATERS'''

    def set_color_t(self, color):
        '''
            PURPOSE
            Sets the text color 'self.color_t_obj' to a new value and updates
            all necessary attributes

            PARAMETERS
            color           <tuple> of 3 <int> values in range [0, 255] OR
                            instance of <class 'Color'> OR a <str> color label
        '''
        self.color_t_obj = interpreters.get_color(color)
        self.update()

    def set_color_b(self, color):
        '''
            PURPOSE
            Sets the background color 'self.color_b_obj' to a new value and
            updates all necessary attributes

            PARAMETERS
            color           <tuple> of 3 <int> values in range [0, 255] OR
                            instance of <class 'Color'> OR a <str> color label
        '''
        self.color_b_obj = interpreters.get_color(color)
        self.update()

    def set_style(self, style):
        '''
            PURPOSE
            Sets the background color 'self.style_obj' to a new value and
            updates all necessary attributes

            PARAMETERS
            style           Instance of <class 'Style'> OR a <str> style label
        '''
        self.style_obj = interpreters.get_style(style)
        self.update()

    def set_char(self, char):
        '''
            PURPOSE
            Sets the background color 'self.char_obj' to a new value and
            updates all necessary attributes

            PARAMETERS
            char           <str> of length 1
        '''
        self.is_char(char)
        self.char_str = char
        self.update()

    def update(self):
        '''
            PURPOSE
            To update the value of the saved output string based on the current
            instance attributes 'color_t_obj', 'color_b_obj', 'style_obj', and
            'char_obj'
        '''
        self.out = self.end_seq + self.color_t_seq + self.color_b_seq
        self.out += self.style_seq + self.char_str + self.end_seq

    '''FORMATTERS'''

    @property
    def color_t_seq(self):
        '''
            PURPOSE
            Returns the ANSI escape sequence that sets the text color to the
            attribute 'self.color_t_obj'

            RETURNS
            out         <str>
        '''
        out = \
        esc.format(f'38;2;{self.color_t.R};{self.color_t.G};{self.color_t.B}')
        return out

    @property
    def color_b_seq(self):
        '''
            PURPOSE
            Returns the ANSI escape sequence that sets the background color to
            attribute 'self.color_b_obj'

            RETURNS
            out         <str>
        '''
        out = \
        esc.format(f'48;2;{self.color_b.R};{self.color_b.G};{self.color_b.B}')
        return out

    @property
    def style_seq(self):
        '''
            PURPOSE
            Returns the ANSI escape sequence that sets the text style to
            attribute 'self.style_obj'

            RETURNS
            <str>
        '''
        if self.style.styles:
            values = ';'.join(str(ANSI_styles[i]) for i in self.style.styles)
            return esc.format(values)
        else:
            return ''

    @property
    def end_seq(self):
        '''
            PURPOSE
            To reset the terminal to its default values (i.e. remove all
            custom-implemented colors or styles)

            RETURNS
            <str>
        '''
        return esc.format('')

    '''GETTERS'''

    @property
    def color_t(self):
        '''
            PURPOSE
            Return the 'Color' instance used to color the terminal text

            RETURNS
            Instance of 'Color'
        '''
        return self.color_t_obj

    @property
    def color_b(self):
        '''
            PURPOSE
            Return the 'Color' instance used to color the terminal text

            RETURNS
            Instance of 'Color'
        '''
        return self.color_b_obj

    @property
    def style(self):
        '''
            PURPOSE
            Return the 'Style' instance used to style the terminal text

            RETURNS
            Instance of 'Style
        '''
        return self.style_obj

    @property
    def char(self):
        '''
            PURPOSE
            Return the current value of attribute 'char_var'

            RETURNS
            <str>
        '''
        return self.char_str

    def copy(self):
        '''
            PURPOSE
            Returns a deep copy of the current 'Pixel' instance

            RETURNS
            Instance of class 'Pixel'
        '''
        params = {
                  'color_t':self.color_t.copy(),
                  'color_b':self.color_b.copy(),
                  'style':self.style.copy(),
                  'char':self.char,
                 }
        return Pixel(**params)

    @property
    def as_arr(self):
        '''
            PURPOSE
            Returns the current 'Pixel' instance as an array, which can be used
            to recreate the instance at a later time.

            NOTE
            The output array consists of eight elements, mapped as follows:

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
        arr = np.zeros(7 + len(ANSI_styles.keys()), dtype = np.uint32)
        arr[0:3] = self.color_t.RGB
        arr[3:6] = self.color_b.RGB
        arr[6] = ord(self.char)
        arr[7:] = self.style.as_arr
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
        RGBt = (f'({self.color_t.R:03d} {self.color_t.G:03d} '
                f'{self.color_t.B:03d})')
        RGBb = (f'({self.color_b.R:03d} {self.color_b.G:03d} '
                f'{self.color_b.B:03d})')

        if self.style.styles:
            styles = ','.join(self.style.styles)
        else:
            styles = 'Empty'

        char = self.char

        out = (f'Pixel(Color_t{RGBt}, Color_b{RGBt}, Style({styles}, '
               f'Char({char})))')

        return out

    def __hash__(self):
        '''
            PURPOSE
            To return a unique hash for the combined properties of a Pixel
            instance

            RETURNS
            <int>
        '''
        ID = sum(map(hash, (self.color_t, self.color_t, self.style, self.char)))
        return hash(ID)

    def __eq__(self, pixel):
        '''
            PURPOSE
            Confirms that the current 'Pixel' instance has the same properties
            as another instance

            RETURNS
            <bool>
        '''
        if not isinstance(pixel, Pixel) or self.color_t != pixel.color_t or\
           self.color_b != pixel.color_b or self.style != pixel.style or\
           self.char != pixel.char:
           return False
        else:
           return True
