from ..utils import interpreters, checkers
from ..config import defaults
from .Pixel import Pixel
from .Color import Color

class Grid:

    def __init__(self, shape):
        '''
            PURPOSE
            To store and manage a 2-D rectangular grid of 'Pixel' instances

            PARAMETERS
            shape       <tuple> containing two elements of <class 'int'>
        '''
        self.shape = shape
        self.height = self.shape[0]
        self.width = self.shape[1]

        # The grid that will contain each 'Pixel' instance
        self.data = np.empty((self.height, self.width), dtype = Pixel)
