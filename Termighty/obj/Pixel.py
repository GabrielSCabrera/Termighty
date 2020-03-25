from ..utils import interpreters, checkers
from ..config import defaults
from .Color import Color
from .Style import Style

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
            style           <str>
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

        self.update_str()

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
        if len(char) != 1:
            msg = '\n\nParameter \'char\' should be a one-character <str>'
            raise ValueError(msg)
        return True

    '''UPDATERS'''

    def update_color_t(self, color):
        '''
            PURPOSE
            Sets the text color 'self.color_t_obj' to a new value and updates
            all necessary attributes

            PARAMETERS
            color           <tuple> of 3 <int> values in range [0, 255] OR
                            instance of <class 'Color'> OR a <str> color label
        '''
        self.color_t_obj = interpreters.get_color(color)
        self.update_str()

    def update_color_b(self, color):
        '''
            PURPOSE
            Sets the background color 'self.color_b_obj' to a new value and
            updates all necessary attributes

            PARAMETERS
            color           <tuple> of 3 <int> values in range [0, 255] OR
                            instance of <class 'Color'> OR a <str> color label
        '''
        self.color_b_obj = interpreters.get_color(color)
        self.update_str()

    def update_style(self, style):
        '''
            PURPOSE
            Sets the background color 'self.style_obj' to a new value and
            updates all necessary attributes

            PARAMETERS
            style           Instance of <class 'Style'> OR a <str> style label
        '''
        raise NotImplementedError()
        self.style_obj = interpreters.get_style(color)
        self.update_str()

    def update_char(self, char):
        '''
            PURPOSE
            Sets the background color 'self.char_obj' to a new value and
            updates all necessary attributes

            PARAMETERS
            char           <str> of length 1
        '''
        self.is_char(char)
        self.char_str = char
        self.update_str()

    def update_str(self):
        '''
            PURPOSE
            To update the value of the saved output string based on the current
            instance attributes 'color_t_obj', 'color_b_obj', 'style_obj', and
            'char_obj'
        '''
        self.out = self.end_seq + self.color_t_seq + self.color_b_seq
        self.out += self.char + self.end_seq

    '''FORMATTERS'''

    @property
    def color_t_seq(self):
        '''
            PURPOSE
            Returns the ANSI escape sequence that sets the text color to the
            attribute 'self.color_t_obj'

            RETURNS
            <str>
        '''
        return f'\033[38;2;{self.color_t.R};{self.color_t.G};{self.color_t.B}m'

    @property
    def color_b_seq(self):
        '''
            PURPOSE
            Returns the ANSI escape sequence that sets the background color to
            attribute 'self.color_b_obj'

            RETURNS
            <str>
        '''
        return f'\033[48;2;{self.color_b.R};{self.color_b.G};{self.color_b.B}m'

    @property
    def style_seq(self):
        '''
            PURPOSE
            Returns the ANSI escape sequence that sets the text style to
            attribute 'self.style_obj'

            RETURNS
            <str>
        '''
        raise NotImplementedError()

    @property
    def end_seq(self):
        '''
            PURPOSE
            To reset the terminal to its default values (i.e. remove all
            custom-implemented colors or styles)

            RETURNS
            <str>
        '''
        return '\033[m'

    '''OUTPUT AND METADATA'''

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

    def __str__(self):
        '''
            PURPOSE
            To return a printable string that displays all the instance's
            aspects (colors, styles, chars.)

            RETURNS
            <str>
        '''
        return self.out

    def __hash__(self):
        '''
            PURPOSE
            To return a unique hash for the combined properties of a Pixel
            instance

            RETURNS
            <int>
        '''
        ID = f'{self.R:03d}{self.G:03d}{self.B:03d}{self.name}'
        return hash(ID)
