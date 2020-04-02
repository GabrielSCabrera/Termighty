from ..data import str_types, int_types, arr_types
from ..obj.Color import Color
from ..obj.Style import Style
from . import checkers
from .. import data

def get_color(color):
    '''
        PURPOSE
        Confirms that 'color' is a tuple of three integers in range [0,255],
        an instance of <class 'Color'>, or a valid color as defined in RGB.py

        PARAMETER
        color

        RETURNS
        Instance of <class 'color'>
    '''
    if isinstance(color, Color):
        return color.copy()
    elif isinstance(color, str_types) and color.lower() in data.colors.keys():
        return Color(data.colors[color.lower()], color.lower())
    elif isinstance(color, arr_types) and len(color) == 3:
        for c in color:
            if not isinstance(c, int_types) or c < 0 or c > 255:
                break
        else:
            return Color(color)
    msg = ('\n\nExpected a tuple of three integers in range [0,255], '
           'an instance of <class \'Color\'>, or a valid color as defined in '
           'RGB.py')
    raise ValueError(msg)

def get_style(style):
    '''
        PURPOSE
        Confirms that 'style' is an instance of <class 'Style'>, or a valid
        style as defined in ANSI.py

        PARAMETER
        style

        RETURNS
        Instance of <class 'Style'>
    '''
    if isinstance(style, Style):
        return style
    elif isinstance(style, str_types) and style.lower() in data.styles.keys():
        return Style(style.lower())
    msg = ('\n\nExpected an instance of <class \'Style\'>, or a valid style as '
           'defined in ANSI.py')
    raise ValueError(msg)
