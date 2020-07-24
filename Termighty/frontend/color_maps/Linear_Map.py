import numpy as np

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

        self.color_0 = color_0
        self.color_1 = color_1

        super().__init__()

    def set_colors(self):
        '''
            PURPOSE
            Implements the required method 'set_colors()' in superclass
            'Color_Map'
        '''
        diffs = np.zeros(3, dtype = np.int64)

        for i in range(3):
            diffs[i] = self.color_1[i] - self.color_0[i]

        signs = np.sign(diffs)
        steps = np.max(np.abs(diffs))
        self.colors = np.zeros((steps, 3), dtype = np.uint8)

        for i in range(3):
            if signs[i] == 1:
                self.colors[:,i] = \
                np.linspace(self.color_0[i], self.color_1[i], steps)
            elif signs[i] == -1:
                self.colors[:,i] = \
                np.linspace(self.color_1[i], self.color_0[i], steps)[::-1]
