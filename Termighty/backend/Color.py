import numpy as np

from ..data import int_types, str_types
from ..utils import format, checkers
from .cython import Color_Fast
from .. import data

class Color(Color_Fast):

    '''INSTANTIATORS'''
    def  __init__(self, RGB, name = 'Unnamed Color'):
        '''
            PURPOSE
            Subclass of 'Color_Fast' that includes type-checking.  Safer and
            with more informative exceptions than 'Color_Fast', but slower.

            PARAMETERS
            RGB         <tuple> of 3 integers in range 0-255

            OPTIONAL PARAMETERS
            name        <str>
        '''
        self.RGB_arr = np.zeros(3, dtype = np.uint8)
        self.set_name(name)
        self.set_RGB(RGB)

    @classmethod
    def palette(cls, name):
        '''
            PURPOSE
            To initialize a 'Color' instance using a color name; only
            succeeds if the name is found in '/data/RGB.py'

            PARAMETERS
            name        <str>

            RETURNS
            Instance of 'Color'
        '''
        checkers.check_type(name, str_types, 'name', 'palette')
        return super().palette(name)

    '''SETTER METHODS'''

    def set_name(self, name):
        '''
            PURPOSE
            To rename the 'Color' instance

            PARAMETERS
            name        <str>
        '''
        checkers.check_type(name, str_types, 'name', 'rename')
        super().set_name(name)

    def set_RGB(self, RGB):
        '''
            PURPOSE
            To reset the RGB values of the 'Color' instance

            PARAMETERS
            RGB         iterable yielding 3 integers in range 0-255
        '''
        checkers.check_type_arr(RGB, int_types, 'RGB', 'reset_RGB')
        checkers.check_range_arr(RGB, 0, 255, 'RGB', 'reset_RGB')
        checkers.check_shape_arr(RGB, (3,), 'RGB', 'reset_RGB')
        super().set_RGB(RGB)

    def set_R(self, R):
        '''
            PURPOSE
            To set the red color in the RGB array to a new value

            PARAMETERS
            R           <int> in range 0 up to and including 255
        '''
        checkers.check_type(R, int_types, 'R', 'set_R')
        checkers.check_range(R, 0, 255, 'R', 'set_R')
        super().set_R(R)

    def set_G(self, G):
        '''
            PURPOSE
            To set the green color in the RGB array to a new value

            PARAMETERS
            G           <int> in range 0 up to and including 255
        '''
        checkers.check_type(G, int_types, 'G', 'set_G')
        checkers.check_range(G, 0, 255, 'G', 'set_G')
        super().set_G(G)

    def set_B(self, B):
        '''
            PURPOSE
            To set the blue color in the RGB array to a new value

            PARAMETERS
            B           <int> in range 0 up to and including 255
        '''
        checkers.check_type(B, int_types, 'B', 'set_B')
        checkers.check_range(B, 0, 255, 'B', 'set_B')
        super().set_B(B)

    '''SAMPLER METHODS'''

    @classmethod
    def chart(cls, R = None, G = None, B = None, term_width = 80):
        '''
            PURPOSE
            Return a terminal-printable color chart

            PARAMETERS
            R               <nonetype> or <int> in range [0,255]
            G               <nonetype> or <int> in range [0,255]
            B               <nonetype> or <int> in range [0,255]
            term_width      <int>

            WARNING
            Must set exactly one of the parameters 'R', 'G', and 'B' to a value
            in range [0, 255].  The others must be set to None.

            RETURNS
            out         <str>
        '''
        if R is not None and G is None and B is None:
            checkers.check_range(R, 0, 255, 'R', 'chart')
            idx = 0
            val = R
            name = 'Red'
        elif R is None and G is not None and B is None:
            checkers.check_range(G, 0, 255, 'G', 'chart')
            idx = 1
            val = G
            name = 'Green'
        elif R is None and G is None and B is not None:
            checkers.check_range(B, 0, 255, 'B', 'chart')
            idx = 2
            val = B
            name = 'Blue'
        else:
            msg = ('Must set exactly one of the parameters \'R\', \'G\', and '
                   '\'B\' to a value in range [0, 255].  The others must be set'
                   ' to None.')
            raise ValueError(msg)

        checkers.check_type(term_width, int_types, 'term_width', 'chart')

        step = 256//term_width + 1
        colors = np.arange(0, 256, step)
        color_grid = np.meshgrid(colors, colors[::2])
        out = ''
        for m,n in zip(*color_grid):
            for i,j in zip(m,n):
                RGB = [0,0,0]
                RGB[idx] = val
                RGB[(idx+1)%3] = j
                RGB[(idx+2)%3] = i
                out += f'\033[38;2;{RGB[0]:d};{RGB[1]:d};{RGB[2]:d}m'
                out += '█\033[m'
            out += '\n'
        return out

    @classmethod
    def list_colors(cls):
        '''
            PURPOSE
            Returns a list of all the available colors and their names

            RETURNS
            out         <str>
        '''
        out = format.bold('LIST OF ALL AVAILABLE COLORS') + '\n\n'
        colors = [cls(j,i) for i,j in data.colors.items()]
        colors = sorted(colors)
        for color in colors:
            RGB = f'{color.R():>03d} {color.G():>03d} {color.B():>03d}'
            out += f'{color.sample} {RGB} {color.name().upper()}\n'
        return out

    '''OPERATORS'''

    def __add__(self, color):
        '''
            PURPOSE
            To add colors together by summing over their RGB values

            PARAMETERS
            color       Instance of 'Color_Fast'

            RETURNS
            out         Instance of 'Color'
        '''
        checkers.check_type(color, Color_Fast, 'color', '__add__')
        return super().__add__(color)

    def __sub__(self, color):
        '''
            PURPOSE
            To subtract colors from each other by subtracting their RGB values

            PARAMETERS
            color       Instance of 'Color_Fast'

            RETURNS
            out         Instance of 'Color'
        '''
        checkers.check_type(color, Color_Fast, 'color', '__sub__')
        return super().__sub__(color)

    '''COMPARATORS'''

    def __lt__(self, color):
        '''
            PURPOSE
            Checks if the given parameter 'color' has the an RGB value that is
            less (in order R-G-B) than that of the current instance

            PARAMETERS
            color           Instance of <class 'Color_Fast'>

            RETURNS
            <bool>
        '''
        checkers.check_type(color, Color_Fast)
        return super().__lt__(color)

    def __gt__(self, color):
        '''
            PURPOSE
            Checks if the given parameter 'color' has the an RGB value that is
            greater (in order R-G-B) than that of the current instance

            PARAMETERS
            color           Instance of <class 'Color_Fast'>

            RETURNS
            <bool>
        '''
        checkers.check_type(color, Color_Fast)
        return super().__gt__(color)

    def __le__(self, color):
        '''
            PURPOSE
            Checks if the given parameter 'color' has the an RGB value that is
            less (in order R-G-B) than or equal to that of the current instance

            PARAMETERS
            color           Instance of <class 'Color_Fast'>

            RETURNS
            <bool>
        '''
        checkers.check_type(color, Color_Fast)
        return super().__le__(color)

    def __ge__(self, color):
        '''
            PURPOSE
            Checks if the given parameter 'color' has the an RGB value that is
            greater (in order R-G-B) than or equal to that of the current
            instance

            PARAMETERS
            color           Instance of <class 'Color_Fast'>

            RETURNS
            <bool>
        '''
        checkers.check_type(color, Color_Fast)
        return super().__ge__(color)
