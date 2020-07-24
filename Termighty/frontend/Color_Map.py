import numpy as np

from ..backend import Grid_Fast, Pixel_Fast, Color_Fast
from ..config import defaults
from ..utils import bold

class Color_Map:

    def __init__(self):
        '''
            PURPOSE
            A superclass that can be inherited in order to create a color map,
            which is a set of colors that are mapped to numerical values.

            WARNING
            Must implement method 'set_colors()' in subclass
        '''
        self.set_colors()
        self.set_ranges()

    def set_colors(self):
        '''
            PURPOSE
            User-implemented method that must create an (N,3) <ndarray> of dtype
            <uint8> called 'self.colors'
        '''
        msg = ('\nClass \'Color_Map\' is an abstract superclass that must be '
               'inherited.  Create a subclass with a \'set_colors()\' method '
               'and use that instead.')
        raise NotImplementedError(msg)

    def set_ranges(self):
        '''
            PURPOSE
            Once 'self.colors' is created, will create a range of values (like
            bins of a histogram) which can be used to round down to the nearest
            valid RGB integer.
        '''
        self.ranges = np.linspace(0, 1, len(self.colors)-1, endpoint = False)

    def __call__(self, x):
        '''
            PURPOSE
            Accepts an array of numbers from zero up to and including one, and
            returns a set of corresponding RGB values.

            PARAMETERS
            x           <ndarray> of floats in range [0,1]

            RETURNS
            rgb         <ndarray> of <uint8> with shape (*(x.shape), 3)
        '''
        x = np.array(x)
        shape = x.shape
        idx = np.searchsorted(self.ranges, x.flatten(), side = 'right')
        out = self.colors[idx]
        out = out.reshape((*(x.shape), 3))
        return out

    def sample(self):
        '''
            PURPOSE
            Returns a printable sample <str> with a selection of the range of
            color values for the given instance.
        '''
        out = bold('COLOR MAP SAMPLE') + '\n{}\033[m'
        values = self.__call__(np.linspace(0, 1, defaults.term_width))
        pixels = [[Pixel_Fast(color_b = Color_Fast(rgb)) for rgb in values]]
        grid = Grid_Fast(pixels)
        out = out.format(grid)
        return out
