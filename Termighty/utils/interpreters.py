from ..obj.Color import Color
from ..data import RGB
from . import checkers

def get_color(color):
    '''
        PURPOSE
        Confirms that 'color' is a tuple of three integers in range [0,255],
        an instance of <class 'Color'>, or a valid color as defined in RGB.py

        PARAMETER
        color       anything

        RETURNS
        Instance of <class 'color'>
    '''
    if isinstance(color, Color):
        return color
    elif isinstance(color, str) and color.lower() in RGB.keys():
        return Color(RGB[color.lower()], color.lower())
    elif isinstance(color, tuple) and len(color) == 3:
        for c in color:
            if not isinstance(c, int) or c < 0 or c > 255:
                break
        else:
            return Color(color)
    msg = ('Expected a tuple of three integers in range [0,255],'
           'an instance of <class \'Color\'>, or a valid color as defined in '
           'RGB.py')
    raise ValueError(msg)
