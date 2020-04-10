import numpy as np

from ...data import int_types, str_types, arr_types, path_types
from ...backend import Grid_Fast, Pixel_Fast, Color_Fast
from ..Color_Map import Color_Map
from ...utils import interpreters

class Linear_Map(Color_Map):

    def __init__(self, color_0, color_1):
        '''
            PURPOSE
            Creates a linear 'Color_Map' that linearly maps values in the range
            [0,1] to the RGB values in 'color_0' and 'color_1'.

            PARAMETERS
            color_0         <tuple> of 3 <int> values in range [0,255] OR
                            instance of 'Color_Fast' OR a <str> color label
            color_1         <tuple> of 3 <int> values in range [0,255] OR
                            instance of 'Color_Fast' OR a <str> color label
        '''
        color_0 = interpreters.get_color(color_0).RGB
        color_1 = interpreters.get_color(color_1).RGB
        diffs = np.zeros(3, dtype = np.int64)

        for i in range(3):
            diffs[i] = color_1[i] - color_0[i]

        signs = np.sign(diffs)
        steps = np.max(np.abs(diffs))
        self.colors = np.zeros((steps, 3), dtype = np.uint8)

        for i in range(3):
            if signs[i] == 1:
                self.colors[:,i] = \
                np.linspace(color_0[i], color_1[i], steps)
            elif signs[i] == -1:
                self.colors[:,i] = \
                np.linspace(color_1[i], color_0[i], steps)[::-1]
        self.ranges = np.linspace(0, 1, steps-1, endpoint = False)
        super().__init__()

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
