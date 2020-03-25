from ..utils import format, checkers
from .. import data
import numpy as np

class Color:

    '''CONSTRUCTOR'''

    def __init__(self, RGB, name = 'Unnamed Color'):
        '''
            PURPOSE
            Base class for the defining of RGB colors, with R, G, and B as
            <int> in the range 0-255

            PARAMETERS
            RGB         <tuple> of 3 integers in range 0-255

            OPTIONAL PARAMETERS
            name        <str>
        '''

        self.set_name(name)
        self.set_RGB(RGB)

    @staticmethod
    def palette(name):
        '''
            PURPOSE
            To initialize a 'Color' instance using a color name; only
            succeeds if the name is found in '/data/RGB.py'

            PARAMETERS
            name        <str>

            RETURNS
            Instance of 'Color'
        '''
        checkers.check_type(name, str, 'name', 'palette')
        if name not in data.colors.keys():
            msg = f'Selected color \'{color}\' is unknown'
            raise ValueError(msg)
        return Color(data.colors[name], name)

    '''SETTER METHODS'''

    def set_name(self, name):
        '''
            PURPOSE
            To rename the 'Color' instance

            PARAMETERS
            name        <str>
        '''
        name_params = {
                       'var'    : name,
                       'name'   : 'name',
                       'types'  : str,
                       'method' : 'rename'
                       }

        checkers.check_type(**name_params)
        self.name_str = name

    def set_RGB(self, RGB):
        '''
            PURPOSE
            To reset the RGB values of the 'Color' instance

            PARAMETERS
            RGB         iterable yielding 3 integers in range 0-255
        '''
        RGB_params = {
                       'arr'    : RGB,
                       'name'   : 'RGB',
                       'types'  : (int, np.uint8, np.int64),
                       'method' : 'reset_RGB'
                       }

        checkers.check_type_arr(**RGB_params)

        del RGB_params['types']
        RGB_params['low'] = 0
        RGB_params['high'] = 255

        checkers.check_range_arr(**RGB_params)

        if len(RGB) != 3:
            msg = ('Parameter \'RGB\' in \'set_RGB\' must be a <tuple> of '
                   'length 3 containing <int> values in range [0,255]')
            raise ValueError

        self.RGB_arr = np.array(RGB, dtype = np.uint8)

    def set_R(self, R):
        '''
            PURPOSE
            To set the red color in the RGB array to a new value

            PARAMETERS
            R           <int> in range 0 up to and including 255
        '''
        checkers.check_type(R, (int, np.uint8), 'R', 'set_R')
        checkers.check_range(R, 0, 255, 'R', 'set_R')
        self.RGB_arr[0] = R

    def set_G(self, G):
        '''
            PURPOSE
            To set the green color in the RGB array to a new value

            PARAMETERS
            G           <int> in range 0 up to and including 255
        '''
        checkers.check_type(G, (int, np.uint8), 'G', 'set_G')
        checkers.check_range(G, 0, 255, 'G', 'set_G')
        self.RGB_arr[1] = G

    def set_B(self, B):
        '''
            PURPOSE
            To set the blue color in the RGB array to a new value

            PARAMETERS
            B           <int> in range 0 up to and including 255
        '''
        checkers.check_type(B, (int, np.uint8), 'B', 'set_B')
        checkers.check_range(B, 0, 255, 'B', 'set_B')
        self.RGB_arr[2] = B

    '''GETTER METHODS'''
    @property
    def name(self):
        '''
            PURPOSE
            Returns an instance's color name

            RETURNS
            self.name_str       <str>
        '''
        return self.name_str

    @property
    def RGB(self):
        '''
            PURPOSE
            Returns an instance's RGB data

            RETURNS
            self.RGB_arr        <ndarray> containing three <uint8> elements
        '''
        return self.RGB_arr.copy()

    @property
    def R(self):
        '''
            PURPOSE
            Returns an instance's red RGB data

            RETURNS
            <uint8>
        '''
        return self.RGB_arr[0]

    @property
    def G(self):
        '''
            PURPOSE
            Returns an instance's green RGB data

            RETURNS
            <uint8>
        '''
        return self.RGB_arr[1]

    @property
    def B(self):
        '''
            PURPOSE
            Returns an instance's blue RGB data

            RETURNS
            <uint8>
        '''
        return self.RGB_arr[2]

    def copy(self):
        '''
            Purpose
            Returns a deep copy of the current instance

            RETURNS
            Instance of 'Color'
        '''
        return Color(self.RGB, self.name)

    def __str__(self):
        '''
            PURPOSE
            Returns the color name, RGB value, and a sample of the color

            RETURNS
            out         <str>
        '''
        out = format.bold('COLOR NAME \t') + self.name_str.upper()
        out += '\n' + format.bold('RGB ')
        out += f'\t\t{self.RGB[0]:03d} {self.RGB[1]:03d} {self.RGB[2]:03d}\n'
        out += format.bold('SAMPLE \t\t') + self.sample*11

        return out

    def __repr__(self):
        '''
            PURPOSE
            Returns a color sample that is machine-readable

            RETURNS
            out         <str>
        '''
        return f'Color(({self.R},{self.G},{self.B}), {self.name_str})'

    '''SAMPLERS METHODS'''

    @property
    def sample(self):
        '''
            PURPOSE
            Returns a color sample in the form of a printable string

            RETURNS
            out         <str>
        '''
        out = f'\033[38;2;{self.RGB[0]:d};{self.RGB[1]:d};{self.RGB[2]:d}m'
        out += '█\033[m'
        return out

    @staticmethod
    def chart(R = None, G = None, B = None, term_width = 80):
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
            idx = 0
            checkers.check_range(R, 0, 255, 'R', 'chart')
            val = R
            name = 'Red'
        elif R is None and G is not None and B is None:
            idx = 1
            checkers.check_range(G, 0, 255, 'G', 'chart')
            val = G
            name = 'Green'
        elif R is None and G is None and B is not None:
            idx = 2
            checkers.check_range(B, 0, 255, 'B', 'chart')
            val = B
            name = 'Blue'
        else:
            msg = ('Must set exactly one of the parameters \'R\', \'G\', and '
                   '\'B\' to a value in range [0, 255].  The others must be set '
                   'to None.')
            raise ValueError(msg)

        checkers.check_type(term_width, int, 'term_width', 'chart')

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

    @staticmethod
    def list_colors():
        '''
            PURPOSE
            Returns a list of all the available colors and their names

            RETURNS
            out         <str>
        '''
        out = format.bold('LIST OF ALL AVAILABLE COLORS') + '\n\n'
        colors = [Color(j,i) for i,j in data.colors.items()]
        colors = sorted(colors)
        for color in colors:
            RGB = f'{color.R:>03d} {color.G:>03d} {color.B:>03d}'
            out += f'{color.sample} {RGB} {color.name.upper()}\n'
        return out

    '''MAGIC METHODS'''

    def __add__(self, color):
        '''
            PURPOSE
            To add colors together by summing over their RGB values

            PARAMETERS
            color       Instance of 'Color'

            RETURNS
            out         Instance of 'Color'
        '''
        name_params = {
                       'var'    : color,
                       'name'   : 'color',
                       'types'  : Color,
                       'method' : '__add__'
                       }

        checkers.check_type(**name_params)
        new_RGB = self.RGB.astype(np.int64) + color.RGB.astype(np.int64)
        new_RGB = tuple(min(int(i), 255) for i in new_RGB)
        return Color(new_RGB)

    def __sub__(self, color):
        '''
            PURPOSE
            To subtract colors from each other by subtracting their RGB values

            PARAMETERS
            color       Instance of 'Color'

            RETURNS
            out         Instance of 'Color'
        '''
        name_params = {
                       'var'    : color,
                       'name'   : 'color',
                       'types'  : Color,
                       'method' : '__sub__'
                       }

        checkers.check_type(**name_params)
        new_RGB = self.RGB.astype(np.int64) - color.RGB.astype(np.int64)
        new_RGB = tuple(max(int(i), 0) for i in new_RGB)
        return Color(new_RGB)

    def __eq__(self, color):
        '''
            PURPOSE
            Checks if the given parameter 'color' has the same RGB value
            as the current instance

            PARAMETERS
            color           Instance of <class 'Color'>

            RETURNS
            <bool>
        '''
        if np.array_equal(color.RGB, self.RGB):
            return True
        else:
            return False

    def __ne__(self, color):
        '''
            PURPOSE
            Checks if the given parameter 'color' has a different RGB value
            than the current instance

            PARAMETERS
            color           Instance of <class 'Color'>

            RETURNS
            <bool>
        '''
        return not self.__eq__(color)

    def __lt__(self, color):
        '''
            PURPOSE
            Checks if the given parameter 'color' has the an RGB value that is
            less (in order R-G-B) than that of the current instance

            PARAMETERS
            color           Instance of <class 'Color'>

            RETURNS
            <bool>
        '''
        if self.R < color.R:
            return True
        elif self.G < color.G and self.R == color.R:
            return True
        elif self.B < color.B and self.G == color.G and self.R == color.R:
            return True
        else:
            return False

    def __gt__(self, color):
        '''
            PURPOSE
            Checks if the given parameter 'color' has the an RGB value that is
            greater (in order R-G-B) than that of the current instance

            PARAMETERS
            color           Instance of <class 'Color'>

            RETURNS
            <bool>
        '''
        if self.R > color.R:
            return True
        elif self.G > color.G and self.R == color.R:
            return True
        elif self.B > color.B and self.G == color.G and self.R == color.R:
            return True
        else:
            return False

    def __le__(self, color):
        '''
            PURPOSE
            Checks if the given parameter 'color' has the an RGB value that is
            less (in order R-G-B) than or equal to that of the current instance

            PARAMETERS
            color           Instance of <class 'Color'>

            RETURNS
            <bool>
        '''
        if self.R > color.R:
            return False
        elif self.G > color.G and self.R == color.R:
            return False
        elif self.B > color.B and self.G == color.G and self.R == color.R:
            return False
        else:
            return True

    def __ge__(self, color):
        '''
            PURPOSE
            Checks if the given parameter 'color' has the an RGB value that is
            greater (in order R-G-B) than or equal to that of the current
            instance

            PARAMETERS
            color           Instance of <class 'Color'>

            RETURNS
            <bool>
        '''
        if self.R < color.R:
            return False
        elif self.G < color.G and self.R == color.R:
            return False
        elif self.B < color.B and self.G == color.G and self.R == color.R:
            return False
        else:
            return True

    def __hash__(self):
        '''
            PURPOSE
            To return a unique hash for the RGB values of a 'Color' instance

            RETURNS
            <int>
        '''
        ID = f'{self.R:03d}{self.G:03d}{self.B:03d}'
        return hash(ID)

    def __is__(self, color):
        '''
            PURPOSE
            Determines whether or not the current instance and given
            parameter 'color' point to the same memory location

            PARAMETERS
            color           Instance of <class 'Color'>

            RETURNS
            <bool>
        '''
        if self is color:
            return True
        else:
            return False
