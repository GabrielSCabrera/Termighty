from ..utils import interpreters, checkers
from ..config import defaults
from .Color import Color

class Pixel:

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
            self.color_t = defaults.color_t
        else:
            self.color_t =\
            interpreters.get_color(color_t)

        if color_b is None:
            self.color_b = defaults.color_b
        else:
            self.color_b =\
            interpreters.get_color(color_b)

        if style is None:
            self.style = None

        if char is None:
            self.char = ' '
        else:
            self.char = checkers.check_type(char, str, 'char', '__init__')
            if len(self.char) != 1:
                msg = 'Parameter \'char\' should be a one-character <str>'
                raise ValueError(msg)

        self.update_str()

    def update_color_t(self, color):
        '''
            PURPOSE
            Sets the text color 'self.color_t' to a new value and updates all
            necessary attributes

            PARAMETERS
            color           <tuple> of 3 <int> values in range [0, 255] OR
                            instance of <class 'Color'> OR a <str> color label
        '''
        self.color_t = interpreters.get_color(color)
        self.update_str()

    def update_color_b(self, color):
        '''
            PURPOSE
            Sets the background color 'self.color_b' to a new value and updates
            all necessary attributes

            PARAMETERS
            color           <tuple> of 3 <int> values in range [0, 255] OR
                            instance of <class 'Color'> OR a <str> color label
        '''
        self.color_b = interpreters.get_color(color)
        self.update_str()

    @property
    def color_t_seq(self):
        '''
            PURPOSE
            Returns the ANSI escape sequence that sets the text color to the
            attribute 'self.color_t'

            RETURNS
            <str>
        '''
        return f'\033[38;2;{self.color_t.R};{self.color_t.G};{self.color_t.B}m'

    @property
    def color_b_seq(self):
        '''
            PURPOSE
            Returns the ANSI escape sequence that sets the background color to
            attribute 'self.color_b'

            RETURNS
            <str>
        '''
        return f'\033[48;2;{self.color_b.R};{self.color_b.G};{self.color_b.B}m'

    @property
    def style_seq(self):
        '''
            PURPOSE
            Returns the ANSI escape sequence that sets the text style to
            attribute 'self.style'

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

    def update_str(self):
        '''
            PURPOSE
            To update the value of the saved output string based on the current
            instance attributes 'color_t', 'color_b', 'style', and 'char'
        '''
        self.out = self.end_seq + self.color_t_seq + self.color_b_seq
        self.out += self.char + self.end_seq

    def __str__(self):
        '''
            PURPOSE
            To return a printable string that displays all the instance's
            aspects (colors, styles, chars.)

            RETURNS
            <str>
        '''
        return self.out
