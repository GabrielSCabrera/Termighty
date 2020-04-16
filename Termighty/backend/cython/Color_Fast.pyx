import numpy as np
cimport numpy as np

from ...utils import format
from ... import data

cdef class Color_Fast(object):

    '''CONSTRUCTOR'''

    def  __init__(self, tuple RGB, name = 'Unnamed Color'):
        '''
            PURPOSE
            Base class for the defining of RGB colors, with R, G, and B as
            <int> in the range 0-255

            PARAMETERS
            RGB         <tuple> of 3 integers in range 0-255

            OPTIONAL PARAMETERS
            name        <str>
        '''
        self.RGB_arr = np.zeros(3, dtype = np.uint8)
        self.set_name(name)
        self.set_RGB(RGB)

    '''INSTANTIATORS'''

    @classmethod
    def palette(cls, str name):
        '''
            PURPOSE
            To initialize a 'Color_Fast' instance using a color name; only
            succeeds if the name is found in '/data/RGB.py'

            PARAMETERS
            name        <str>

            RETURNS
            Instance of 'Color_Fast'
        '''
        if name not in data.colors.keys():
            msg = f'Selected color \'{name}\' is unknown'
            raise ValueError(msg)
        return cls(data.colors[name], name)

    def complement(self):
        '''
            PURPOSE
            Returns the color complement of the current instance, which is the
            element-wise difference (255,255,255) - (R,G,B), with R, G, and B
            being the current instance's color channels.

            RETURNS
            instance of class 'Color_Fast'
        '''
        RGB = np.zeros(3, dtype = np.uint8)
        for i in range(3):
            RGB[i] = 255 - self.RGB_arr[i]
        return self.__class__(RGB = RGB)

    def copy(self):
        '''
            Purpose
            Returns a deep copy of the current instance

            RETURNS
            Instance of 'Color_Fast'
        '''
        return self.__class__(self.RGB(), self.name())

    '''SETTER METHODS'''

    cpdef void set_name(self, str name):
        '''
            PURPOSE
            To rename the 'Color_Fast' instance

            PARAMETERS
            name        <str>
        '''
        self.name_str = name

    cpdef void set_RGB(self, tuple RGB):
        '''
            PURPOSE
            To reset the RGB values of the 'Color_Fast' instance

            PARAMETERS
            RGB         iterable yielding 3 integers in range 0-255
        '''
        cdef Py_ssize_t i
        for i in range(3):
            self.RGB_arr[i] = RGB[i]

    cpdef void set_R(self, int R):
        '''
            PURPOSE
            To set the red color in the RGB array to a new value

            PARAMETERS
            R           <int> in range 0 up to and including 255
        '''
        self.RGB_arr[0] = R

    cpdef void set_G(self, int G):
        '''
            PURPOSE
            To set the green color in the RGB array to a new value

            PARAMETERS
            G           <int> in range 0 up to and including 255
        '''
        self.RGB_arr[1] = G

    cpdef void set_B(self, int B):
        '''
            PURPOSE
            To set the blue color in the RGB array to a new value

            PARAMETERS
            B           <int> in range 0 up to and including 255
        '''
        self.RGB_arr[2] = B

    '''GETTER METHODS'''

    def __str__(self):
        '''
            PURPOSE
            Returns the color name, RGB value, and a sample of the color

            RETURNS
            out         <str>
        '''
        out = format.bold('COLOR NAME \t') + self.name().upper()
        out += '\n' + format.bold('RGB ')
        out += f'\t\t{self.R():03d} {self.G():03d} {self.B():03d}\n'
        out += format.bold('SAMPLE \t\t') + self.sample()*11
        return out

    def __repr__(self):
        '''
            PURPOSE
            Returns a color sample that is machine-readable

            RETURNS
            out         <str>
        '''
        return f'Color({self.R():03d} {self.G():03d} {self.B():03d} | {self.name()})'

    def __hash__(self):
        '''
            PURPOSE
            To return a unique hash for the RGB values of a 'Color_Fast'
            instance

            RETURNS
            <int>
        '''
        ID = f'{self.R():03d}{self.G():03d}{self.B():03d}'
        return hash(ID)

    '''ACCESSOR METHODS'''

    cpdef str name(self):
        '''
            PURPOSE
            Returns an instance's color name

            RETURNS
            self.name_str       <str>
        '''
        return self.name_str

    cpdef tuple RGB(self):
        '''
            PURPOSE
            Returns an instance's RGB data

            RETURNS
            self.RGB_arr        <ndarray> containing three <uint8> elements
        '''
        return (int(self.RGB_arr[0]), int(self.RGB_arr[1]), int(self.RGB_arr[2]))

    cpdef int R(self):
        '''
            PURPOSE
            Returns an instance's red RGB data

            RETURNS
            <uint8>
        '''
        return int(self.RGB_arr[0])

    cpdef int G(self):
        '''
            PURPOSE
            Returns an instance's green RGB data

            RETURNS
            <uint8>
        '''
        return int(self.RGB_arr[1])

    cpdef int B(self):
        '''
            PURPOSE
            Returns an instance's blue RGB data

            RETURNS
            <uint8>
        '''
        return int(self.RGB_arr[2])

    '''SAMPLER METHODS'''

    cpdef str sample(self):
        '''
            PURPOSE
            Returns a color sample in the form of a printable string

            RETURNS
            out         <str>
        '''
        out = f'\033[48;2;{self.RGB_arr[0]:d};{self.RGB_arr[1]:d};{self.RGB_arr[2]:d}m'
        out += ' \033[m'
        return out

    '''OPERATORS'''

    def __add__(self, color):
        '''
            PURPOSE
            To add colors together by summing over their RGB values

            PARAMETERS
            color       Instance of 'Color_Fast'

            RETURNS
            out         Instance of 'Color_Fast'
        '''
        new_RGB = (self.R() + color.R(), self.G() + color.G(), self.B() + color.B())
        new_RGB = tuple(min(int(i), 255) for i in new_RGB)
        return self.__class__(new_RGB)

    def __sub__(self, color):
        '''
            PURPOSE
            To subtract colors from each other by subtracting their RGB values

            PARAMETERS
            color       Instance of 'Color_Fast'

            RETURNS
            out         Instance of 'Color_Fast'
        '''
        new_RGB = (self.R() - color.R(), self.G() - color.G(), self.B() - color.B())
        new_RGB = tuple(max(int(i), 0) for i in new_RGB)
        return self.__class__(new_RGB)

    '''COMPARATORS'''

    def __eq__(self, color):
        '''
            PURPOSE
            Checks if the given parameter 'color' has the same RGB value
            as the current instance

            PARAMETERS
            color           Instance of <class 'Color_Fast'>

            RETURNS
            <bool>
        '''
        if np.array_equal(color.RGB(), self.RGB()):
            return True
        else:
            return False

    def __ne__(self, color):
        '''
            PURPOSE
            Checks if the given parameter 'color' has a different RGB value
            than the current instance

            PARAMETERS
            color           Instance of <class 'Color_Fast'>

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
            color           Instance of <class 'Color_Fast'>

            RETURNS
            <bool>
        '''
        if self.R() < color.R():
            return True
        elif self.G() < color.G() and self.R() == color.R():
            return True
        elif self.B() < color.B() and self.G() == color.G() and self.R() == color.R():
            return True
        else:
            return False

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
        if self.R() > color.R():
            return True
        elif self.G() > color.G() and self.R() == color.R():
            return True
        elif self.B() > color.B() and self.G() == color.G() and self.R() == color.R():
            return True
        else:
            return False

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
        if self.R() > color.R():
            return False
        elif self.G() > color.G() and self.R() == color.R():
            return False
        elif self.B() > color.B() and self.G() == color.G() and self.R() == color.R():
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
            color           Instance of <class 'Color_Fast'>

            RETURNS
            <bool>
        '''
        if self.R() < color.R():
            return False
        elif self.G() < color.G() and self.R() == color.R():
            return False
        elif self.B() < color.B() and self.G() == color.G() and self.R() == color.R():
            return False
        else:
            return True
