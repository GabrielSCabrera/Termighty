import numpy as np

def calibrate_Color():
    '''
        PURPOSE
        Runs tests for class 'Color' that must be visually inspected
    '''
    # Importing class 'Color' locally
    from ..backend import Color

    msg = ('TESTS FOR CLASS COLOR')
    print(f'\n\033[30;47;4m{msg:^80s}\033[m\n')

    # Rainbow Calibration
    msg = ('\033[1mRainbow Calibration – Confirm Next Three Rows Are Identical'
           '\033[m\n')
    colors = {'red'     :   (255,0,0),
              'orange'  :   (255,127,0),
              'yellow'  :   (255,255,0),
              'green'   :   (0,255,0),
              'blue'    :   (0,0,255),
              'indigo'  :   (73,0,130),
              'violet'  :   (142,0,255)
             }

    row1 = '\033[1mROW 1:\033[m '
    row2 = '\033[1mROW 2:\033[m '
    row3 = '\033[1mROW 3:\033[m '
    labels = '      '
    for color, rgb in colors.items():
        labels += f'{color:^8s} '
        row1 += f'{Color.palette(color).sample}'*8 + ' '
        row2 += f'{Color(rgb).sample}'*8 + ' '
        row3 += f'\033[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m \033[m'*8 + ' '

    msg += row1 + '\n' + row2 + '\n' + row3 + '\n' + labels
    print(msg)

    # Fade from Black
    msg = ('\n\033[1mColor Gradients – Confirm RGB Colors Fade Smoothly In From '
           'Black\033[m\n')
    length = 69
    fmt_len = 11
    length -= fmt_len
    gradient = np.linspace(0, 255, length, dtype = np.uint8)

    reds = np.zeros((length, 3), dtype = np.uint8)
    greens = np.zeros((length, 3), dtype = np.uint8)
    blues = np.zeros((length, 3), dtype = np.uint8)

    reds[:,0] = gradient
    greens[:,1] = gradient
    blues[:,2] = gradient

    msg += f'\033[1m{"RED:":{fmt_len}s}\033[m'
    msg += ''.join(f'\033[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m ' for rgb in reds)
    msg += '\033[m\n' + ' '*fmt_len + ''.join(Color(rgb).sample for rgb in reds)
    msg += f'\033[m\n\033[1m{"GREEN:":{fmt_len}s}\033[m'
    msg += ''.join(f'\033[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m ' for rgb in greens)
    msg += '\033[m\n' + ' '*fmt_len + ''.join(Color(rgb).sample for rgb in greens)
    msg += f'\033[m\n\033[1m{"BLUE:":{fmt_len}s}\033[m'
    msg += ''.join(f'\033[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m ' for rgb in blues)
    msg += '\033[m\n' + ' '*fmt_len + ''.join(Color(rgb).sample for rgb in blues)
    msg += '\033[m\n'

    print(msg)

    # Fade Between
    msg = ('\n\033[1mColor Gradients – Confirm RGB Colors Fade Smoothly '
           'Between Each Other\033[m\n')
    length = 69
    fmt_len = 11
    length -= fmt_len
    gradient = np.linspace(0, 255, length, dtype = np.uint8)

    RG = np.zeros((length, 3), dtype = np.uint8)
    GB = np.zeros((length, 3), dtype = np.uint8)
    BR = np.zeros((length, 3), dtype = np.uint8)

    RG[:,0] = gradient[::-1]
    RG[:,1] = gradient
    GB[:,1] = gradient[::-1]
    GB[:,2] = gradient
    BR[:,2] = gradient[::-1]
    BR[:,0] = gradient

    msg += f'\033[1m{"RED>GREEN:":{fmt_len}s}\033[m'
    msg += ''.join(f'\033[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m ' for rgb in RG)
    msg += '\033[m\n' + ' '*fmt_len + ''.join(Color(rgb).sample for rgb in RG)
    msg += f'\033[m\n\033[1m{"GREEN>BLUE:":{fmt_len}s}\033[m'
    msg += ''.join(f'\033[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m ' for rgb in GB)
    msg += '\033[m\n' + ' '*fmt_len + ''.join(Color(rgb).sample for rgb in GB)
    msg += f'\033[m\n\033[1m{"BLUE>RED:":{fmt_len}s}\033[m'
    msg += ''.join(f'\033[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m ' for rgb in BR)
    msg += '\033[m\n' + ' '*fmt_len + ''.join(Color(rgb).sample for rgb in BR)
    msg += '\033[m'

    print(msg)

def calibrate_Style():
    '''
        PURPOSE
        Runs tests for class 'Style' that must be visually inspected
    '''
    # Importing class 'Style' locally
    from ..backend import Style

    msg = ('TESTS FOR CLASS STYLE')
    print(f'\n\033[30;47;4m{msg:^80s}\033[m\n')

    # Single Style Calibration
    msg = ('\033[1mSingle Style Calibration – Confirm Next Two Rows Are '
           'Identical\033[m\n')

    styles = {
              'bold':         1,
              'faint':        2,
              'italic':       3,
              'underline':    4,
              'blink':        5,
              'reverse':      7,
              'crossed out':  9,
              'overlined':    53
             }

    row1 = '\033[1mROW 1:\033[m '
    row2 = '\033[1mROW 2:\033[m '
    labels = '      '
    for style, code in styles.items():
        row1 += f'{Style(style)(style)} '
        row2 += f'\033[{code}m{style}\033[m '

    msg += row1 + '\n' + row2
    print(msg)

    # Double Style Calibration
    msg = ('\n\033[1mDouble Style Calibration – Confirm Next Two Rows Are '
           'Identical\033[m\n')

    styles = (
              (('bold', 'italic'),           (1,3)),
              (('faint', 'bold'),            (2,1)),
              (('italic', 'faint'),          (3,2)),
              (('underline', 'reverse'),     (4,7)),
              (('blink', 'crossed out'),     (5,9)),
              (('reverse', 'blink'),         (7,5)),
              (('crossed out', 'overlined'), (9,53)),
              (('overlined', 'faint'),       (53,2))
             )

    row1 = '\033[1mROW 1:\033[m '
    row2 = '\033[1mROW 2:\033[m '
    labels = '      '
    for (style, codes) in styles:
        codes_fmt = ';'.join(str(code) for code in codes)
        row1 += f'{Style(*style)("sample")} '
        row2 += f'\033[{codes_fmt}msample\033[m '

    msg += row1 + '\n' + row2
    print(msg)

    # Triple Style Calibration
    msg = ('\n\033[1mTriple Style Calibration – Confirm Next Two Rows Are '
           'Identical\033[m\n')

    styles = (
              (('bold', 'italic', 'underline'),         (1,3,4)),
              (('faint', 'bold', 'reverse'),            (2,1,7)),
              (('italic', 'faint', 'blink'),            (3,2,5)),
              (('underline', 'reverse', 'faint'),       (4,7,2)),
              (('blink', 'crossed out', 'bold'),        (5,9,1)),
              (('reverse', 'blink', 'italic'),          (7,5,3)),
              (('crossed out', 'overlined', 'bold'),    (9,53,1)),
              (('overlined', 'faint', 'reverse'),       (53,2,7))
             )

    row1 = '\033[1mROW 1:\033[m '
    row2 = '\033[1mROW 2:\033[m '
    labels = '      '
    for (style, codes) in styles:
        codes_fmt = ';'.join(str(code) for code in codes)
        row1 += f'{Style(*style)("sample")} '
        row2 += f'\033[{codes_fmt}msample\033[m '

    msg += row1 + '\n' + row2
    print(msg)

def calibrate_Pixel():
    '''
        PURPOSE
        Runs tests for class 'Pixel' that must be visually inspected
    '''
    # Importing class 'Pixel' locally
    from ..backend import Pixel

    msg = ('TESTS FOR CLASS PIXEL')
    print(f'\n\033[30;47;4m{msg:^80s}\033[m\n')

    # Rainbow Calibration
    msg = ('\033[1mRainbow Calibration – Confirm Next Three Rows Are Identical'
           '\033[m\n')
    colors = {'red'     :   (255,0,0),
              'orange'  :   (255,127,0),
              'yellow'  :   (255,255,0),
              'green'   :   (0,255,0),
              'blue'    :   (0,0,255),
              'indigo'  :   (73,0,130),
              'violet'  :   (142,0,255)
             }

    row1 = '\033[1mROW 1:\033[m '
    row2 = '\033[1mROW 2:\033[m '
    row3 = '\033[1mROW 3:\033[m '
    labels = '      '
    for color, rgb in colors.items():
        labels += f'{color:^8s} '
        px_1 = Pixel(char = color[0], color_b = color, color_t = 'black')
        px_2 = Pixel(char = color[0], color_b = rgb, color_t = (0,0,0))
        row1 += f'{px_1}'*8 + f'{px_1.end_seq} '
        row2 += f'{px_2}'*8 + f'{px_2.end_seq} '
        row3 += (f'\033[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m\033[30m{color[0]}'
                 '\033[m')*8 + ' '

    msg += row1 + '\n' + row2 + '\n' + row3 + '\n' + labels
    print(msg)


    # Fade from Black
    msg = ('\n\033[1mColor Gradients – Confirm RGB Colors Fade Smoothly In From '
           'Black\033[m\n')
    length = 69
    fmt_len = 11
    length -= fmt_len
    gradient = np.linspace(0, 255, length, dtype = np.uint8)

    reds = np.zeros((length, 3), dtype = np.uint8)
    greens = np.zeros((length, 3), dtype = np.uint8)
    blues = np.zeros((length, 3), dtype = np.uint8)

    reds[:,0] = gradient
    greens[:,1] = gradient
    blues[:,2] = gradient

    msg += f'\033[1m{"RED:":{fmt_len}s}\033[m'
    msg += ''.join(f'\033[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m\033[30mX' \
                   for rgb in reds)
    msg += '\033[m\n' + ' '*fmt_len
    msg += ''.join(Pixel(char = 'X', color_t = 'black', color_b = rgb)\
                                              .__str__() for rgb in reds)

    msg += f'\033[m\n\033[1m{"GREEN:":{fmt_len}s}\033[m'
    msg += ''.join(f'\033[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m\033[30mX' \
                   for rgb in greens)
    msg += '\033[m\n' + ' '*fmt_len
    msg += ''.join(Pixel(char = 'X', color_t = 'black', color_b = rgb)\
                                              .__str__() for rgb in greens)

    msg += f'\033[m\n\033[1m{"BLUE:":{fmt_len}s}\033[m'
    msg += ''.join(f'\033[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m\033[30mX' \
                   for rgb in blues)
    msg += '\033[m\n' + ' '*fmt_len
    msg += ''.join(Pixel(char = 'X', color_t = 'black', color_b = rgb)\
                                              .__str__() for rgb in blues)
    msg += '\033[m\n'

    print(msg)

    # Fade Between
    msg = ('\n\033[1mColor Gradients – Confirm RGB Colors Fade Smoothly '
           'Between Each Other\033[m\n')
    length = 69
    fmt_len = 11
    length -= fmt_len
    gradient = np.linspace(0, 255, length, dtype = np.uint8)

    RG = np.zeros((length, 3), dtype = np.uint8)
    GB = np.zeros((length, 3), dtype = np.uint8)
    BR = np.zeros((length, 3), dtype = np.uint8)

    RG[:,0] = gradient[::-1]
    RG[:,1] = gradient
    GB[:,1] = gradient[::-1]
    GB[:,2] = gradient
    BR[:,2] = gradient[::-1]
    BR[:,0] = gradient

    msg += f'\033[1m{"RED>GREEN:":{fmt_len}s}\033[m'
    msg += ''.join(f'\033[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m\033[30mX' \
                   for rgb in RG)
    msg += '\033[m\n' + ' '*fmt_len
    msg += ''.join(Pixel(char = 'X', color_t = 'black', color_b = rgb)\
                         .__str__() for rgb in RG)

    msg += f'\033[m\n\033[1m{"GREEN>BLUE:":{fmt_len}s}\033[m'
    msg += ''.join(f'\033[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m\033[30mX' \
                   for rgb in GB)
    msg += '\033[m\n' + ' '*fmt_len
    msg += ''.join(Pixel(char = 'X', color_t = 'black', color_b = rgb)\
                         .__str__() for rgb in GB)

    msg += f'\033[m\n\033[1m{"BLUE>RED:":{fmt_len}s}\033[m'
    msg += ''.join(f'\033[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m\033[30mX' \
                   for rgb in BR)
    msg += '\033[m\n' + ' '*fmt_len
    msg += ''.join(Pixel(char = 'X', color_t = 'black', color_b = rgb)\
                         .__str__() for rgb in BR)
    msg += '\033[m'

    print(msg)
