from ..utils import interpreters, checkers
from ..data import styles as ANSI_styles
from ..data import str_types, int_types
from .Pixel_Fast import Pixel_Fast

class Pixel(Pixel_Fast):

    '''
        Subclass of 'Pixel_Fast' that includes type-checking.  Safer and with
        more informative exceptions than 'Pixel_Fast', but a lot slower.
    '''

    '''CONSTRUCTOR'''

    def __init__(self, color_t = None, color_b = None, style = None, char = None):
        '''
            PURPOSE
            Basic unit of all graphics displayed in the terminal – may contain
            a foreground color, background color, text style, and character.

            PARAMETERS
            color_t         <tuple> of 3 <int> values in range [0,255] OR
                            instance of 'Color_Fast' OR a <str> color label
            color_b         <tuple> of 3 <int> values in range [0,255] OR
                            instance of 'Color_Fast' OR a <str> color label
            style           <str>, <list> of <str>, or instance of 'Style_Fast'
            char            <str>

            WARNING
            Be aware that pixels are twice as tall as they are wide
        '''
        if color_t is not None:
            color_t = interpreters.get_color(color_t)

        if color_b is not None:
            color_b = interpreters.get_color(color_b)

        if style is not None:
            style = interpreters.get_style(style)

        if char is not None:
            self.is_char(char)

        super().__init__(color_t, color_b, style, char)

    '''INSTANTIATORS'''

    @classmethod
    def from_arr(cls, arr):
        '''
            PURPOSE
            Returns a new 'Pixel' instance based on the values given in 'arr'

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
            Instance of 'Pixel'
        '''
        checkers.check_type_arr(arr, int_types, 'arr', 'from_arr')
        checkers.check_shape_arr(arr, (7+len(ANSI_styles),), 'arr', 'from_arr')
        return super().from_arr(arr)

    '''SETTERS'''

    def set_color_t(self, color):
        '''
            PURPOSE
            Sets the text color 'self.color_t_obj' to a new value and updates
            all necessary attributes

            PARAMETERS
            color           <tuple> of 3 <int> values in range [0, 255] OR
                            instance of 'Color' OR a <str> color label
        '''
        color = interpreters.get_color(color)
        super().set_color_t(color)

    def set_color_b(self, color):
        '''
            PURPOSE
            Sets the background color 'self.color_b_obj' to a new value and
            updates all necessary attributes

            PARAMETERS
            color           <tuple> of 3 <int> values in range [0, 255] OR
                            instance of 'Color' OR a <str> color label
        '''
        color = interpreters.get_color(color)
        super().set_color_b(color)

    def set_style(self, style):
        '''
            PURPOSE
            Sets the background color 'self.style_obj' to a new value and
            updates all necessary attributes

            PARAMETERS
            style           Instance of 'Style' OR a <str> style label
        '''
        style = interpreters.get_style(style)
        super().set_style(style)

    def set_char(self, char):
        '''
            PURPOSE
            Sets the background color 'self.char_obj' to a new value and
            updates all necessary attributes

            PARAMETERS
            char           <str> of length 1
        '''
        self.is_char(char)
        super().set_char(char)
