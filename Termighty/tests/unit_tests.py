from .Tester import Tester
import numpy as np

def test_Color():
    '''
        PURPOSE
        Tests for class Color

        RETURNS
        results         <dict>
    '''
    # Importing class 'Color' locally
    from ..obj import Color

    # Initializing 'Tester' instance
    T = Tester('class Color')

    # New Test
    T.start('Empty Constructor')
    try:
        color = Color()
        T.failed()
    except TypeError:
        T.passed()

    # New Test
    T.start('Constructor: valid RGB arg')
    try:
        blue = Color(RGB = (0, 0, 255))
        T.passed()
    except Exception as e:
        T.failed(e)

    # New Test
    T.start('Constructor: invalid RGB arg [1]')
    try:
        color = Color(RGB = 'A')
        T.failed()
    except TypeError:
        T.passed()

    # New Test
    T.start('Constructor: invalid RGB arg [2]')
    try:
        color = Color(RGB = (0, 0, 'A'))
        T.failed()
    except TypeError:
        T.passed()

    # New Test
    T.start('Constructor: invalid RGB arg [3]')
    try:
        color = Color(RGB = (0, 0, 300))
        T.failed()
    except ValueError:
        T.passed()

    # New Test
    T.start('Constructor: invalid RGB arg [4]')
    try:
        color = Color(RGB = (0, 0, 0, 0))
        T.failed()
    except ValueError:
        T.passed()

    # New Test
    T.start('palette: valid color names')
    try:
        black = Color.palette('black')
        white = Color.palette('white')
        T.passed()
    except Exception as e:
        T.failed(e)

    # New Test
    T.start('palette: invalid color name')
    try:
        color = Color.palette('snicklefritz')
        T.failed(e)
    except NameError:
        T.passed()

    # New Test
    T.start('name')
    try:
        white = Color.palette(name = 'white')
        assert white.name == 'white'
        T.passed()
    except AssertionError as e:
        T.failed(e)

    # New Test
    T.start('RGB')
    try:
        white = Color.palette(name = 'white')
        assert np.array_equal(white.RGB, (255,255,255))
        T.passed()
    except AssertionError as e:
        T.failed(e)

    # New Test
    T.start('R')
    try:
        red = Color.palette(name = 'red')
        assert red.R == 255
        T.passed()
    except AssertionError as e:
        T.failed(e)

    # New Test
    T.start('G')
    try:
        green = Color.palette(name = 'green')
        assert green.G == 255
        T.passed()
    except AssertionError as e:
        T.failed(e)

    # New Test
    T.start('B')
    try:
        blue = Color.palette(name = 'blue')
        assert blue.B == 255
        T.passed()
    except AssertionError as e:
        T.failed(e)

    # New Test
    T.start('set_name: valid name')
    try:
        black = Color(RGB = (0, 0, 0), name = 'white')
        black.set_name('black')
        assert black.name == 'black'
        T.passed()
    except Exception as e:
        T.failed(e)

    # New Test
    T.start('set_name: invalid name')
    try:
        blue = Color.palette('blue')
        blue.set_name(50)
        T.failed()
    except TypeError:
        T.passed()

    # New Test
    T.start('set_RGB: valid tuple')
    try:
        white = Color(RGB = (0, 0, 0), name = 'white')
        white.set_RGB((255,255,255))
        assert np.array_equal(white.RGB, (255, 255, 255))
        T.passed()
    except Exception as e:
        T.failed(e)

    # New Test
    T.start('set_RGB: invalid type')
    try:
        red = Color.palette('red')
        white.set_RGB('A')
        T.failed()
    except TypeError:
        T.passed()

    # New Test
    T.start('set_RGB: invalid tuple [1]')
    try:
        red = Color.palette('red')
        white.set_RGB((0,0,'A'))
        T.failed()
    except TypeError:
        T.passed()

    # New Test
    T.start('set_RGB: invalid tuple [2]')
    try:
        red = Color.palette('red')
        white.set_RGB((0,0,300))
        T.failed()
    except ValueError:
        T.passed()

    # New Test
    T.start('set_RGB: invalid tuple [3]')
    try:
        red = Color.palette('red')
        white.set_RGB((0,0,0,0))
        T.failed()
    except ValueError:
        T.passed()

    # New Test
    T.start('set_R: valid int')
    try:
        red = Color(RGB = (0, 0, 0), name = 'red')
        red.set_R(255)
        assert red.R == 255
        T.passed()
    except Exception as e:
        T.failed(e)

    # New Test
    T.start('set_R: invalid type')
    try:
        red = Color(RGB = (0, 0, 0), name = 'red')
        red.set_R('A')
        T.failed()
    except TypeError:
        T.passed()

    # New Test
    T.start('set_R: invalid value')
    try:
        red = Color(RGB = (0, 0, 0), name = 'red')
        red.set_R(300)
        T.failed()
    except ValueError:
        T.passed()

    # New Test
    T.start('set_G: valid int')
    try:
        green = Color(RGB = (0, 0, 0), name = 'green')
        green.set_G(255)
        assert green.G == 255
        T.passed()
    except Exception as e:
        T.failed(e)

    # New Test
    T.start('set_G: invalid type')
    try:
        green = Color(RGB = (0, 0, 0), name = 'green')
        green.set_G('A')
        T.failed()
    except TypeError:
        T.passed()

    # New Test
    T.start('set_G: invalid value')
    try:
        green = Color(RGB = (0, 0, 0), name = 'green')
        green.set_G(300)
        T.failed()
    except ValueError:
        T.passed()

    # New Test
    T.start('set_B: valid int')
    try:
        blue = Color(RGB = (0, 0, 0), name = 'blue')
        blue.set_B(255)
        assert blue.B == 255
        T.passed()
    except Exception as e:
        T.failed(e)

    # New Test
    T.start('set_B: invalid type')
    try:
        blue = Color(RGB = (0, 0, 0), name = 'blue')
        blue.set_B('A')
        T.failed()
    except TypeError:
        T.passed()

    # New Test
    T.start('set_B: invalid value')
    try:
        blue = Color(RGB = (0, 0, 0), name = 'blue')
        blue.set_B(300)
        T.failed()
    except ValueError:
        T.passed()

    # New Test
    T.start('copy')
    try:
        blue_1 = Color(RGB = (0, 0, 0), name = 'blue')
        blue_2 = blue_1.copy()
        assert blue_1 == blue_2 and blue_1 is not blue_2
        T.passed()
    except ValueError:
        T.failed()

    # New Test
    T.start('__str__')
    try:
        blue = Color(RGB = (0, 0, 0), name = 'blue')
        assert isinstance(blue.__str__(), str)
        T.passed()
    except Exception as e:
        T.failed(e)

    # New Test
    T.start('__repr__')
    try:
        blue = Color(RGB = (0, 0, 0), name = 'blue')
        assert isinstance(blue.__repr__(), str)
        T.passed()
    except Exception as e:
        T.failed(e)

    # New Test
    T.start('sample')
    try:
        blue = Color(RGB = (0, 0, 0), name = 'blue')
        assert isinstance(blue.sample, str)
        T.passed()
    except Exception as e:
        T.failed(e)

    # New Test
    T.start('chart: valid args [1]')
    try:
        assert isinstance(Color.chart(R = 0), str)
        T.passed()
    except Exception as e:
        T.failed(e)

    # New Test
    T.start('chart: valid args [2]')
    try:
        assert isinstance(Color.chart(R = 255), str)
        T.passed()
    except Exception as e:
        T.failed(e)

    # New Test
    T.start('chart: valid args [3]')
    try:
        assert isinstance(Color.chart(G = 0), str)
        T.passed()
    except Exception as e:
        T.failed(e)

    # New Test
    T.start('chart: valid args [4]')
    try:
        assert isinstance(Color.chart(G = 255), str)
        T.passed()
    except Exception as e:
        T.failed(e)

    # New Test
    T.start('chart: valid args [5]')
    try:
        assert isinstance(Color.chart(B = 0), str)
        T.passed()
    except Exception as e:
        T.failed(e)

    # New Test
    T.start('chart: valid args [6]')
    try:
        assert isinstance(Color.chart(B = 255), str)
        T.passed()
    except Exception as e:
        T.failed(e)

    # New Test
    T.start('chart: invalid args [1]')
    try:
        assert isinstance(Color.chart(R = 'A'), str)
        T.failed()
    except TypeError:
        T.passed()

    # New Test
    T.start('chart: invalid args [2]')
    try:
        assert isinstance(Color.chart(G = 'A'), str)
        T.failed()
    except TypeError:
        T.passed()

    # New Test
    T.start('chart: invalid args [3]')
    try:
        assert isinstance(Color.chart(B = 'A'), str)
        T.failed()
    except TypeError:
        T.passed()

    # New Test
    T.start('chart: invalid args [4]')
    try:
        assert isinstance(Color.chart(R = 300), str)
        T.failed()
    except ValueError:
        T.passed()

    # New Test
    T.start('chart: invalid args [5]')
    try:
        assert isinstance(Color.chart(G = 300), str)
        T.failed()
    except ValueError:
        T.passed()

    # New Test
    T.start('chart: invalid args [6]')
    try:
        assert isinstance(Color.chart(B = 300), str)
        T.failed()
    except ValueError:
        T.passed()

    # New Test
    T.start('chart: invalid args [7]')
    try:
        assert isinstance(Color.chart(R = 0, G = 0), str)
        T.failed()
    except ValueError:
        T.passed()

    # New Test
    T.start('list_colors')
    try:
        assert isinstance(Color.list_colors(), str)
        T.passed()
    except Exception as e:
        T.failed(e)

    # New Test
    T.start('__eq__')
    try:
        blue_1 = Color.palette('blue')
        blue_2 = Color.palette('blue')
        assert blue_1 == blue_2
        T.passed()
    except Exception as e:
        T.failed(e)

    # New Test
    T.start('__neq__')
    try:
        blue = Color.palette('blue')
        red = Color.palette('red')
        assert blue != red
        T.passed()
    except Exception as e:
        T.failed(e)

    # New Test
    T.start('__add__')
    try:
        blue = Color.palette('blue')
        red = Color.palette('red')
        purple = Color((255, 0, 255), 'purple')
        assert blue + red == purple
        T.passed()
    except Exception as e:
        T.failed(e)

    # New Test
    pairs = (((0,0,0),(0,0,1),True),
             ((0,0,1),(0,0,2),True),
             ((0,0,2),(0,1,0),True),
             ((0,1,0),(0,2,0),True),
             ((0,2,0),(1,0,0),True),
             ((1,0,0),(2,0,0),True),
             ((0,0,0),(0,0,0),False),
             ((0,0,2),(0,0,1),False),
             ((0,1,0),(0,0,2),False),
             ((0,1,0),(0,1,0),False),
             ((1,0,0),(0,2,0),False),
             ((1,0,0),(1,0,0),False))
    for n, (RGB_1, RGB_2, boolean) in enumerate(pairs):
        T.start(f'__lt__ [{n+1}]')
        try:
            color_1 = Color(RGB_1)
            color_2 = Color(RGB_2)
            assert (color_1 < color_2) is boolean
            T.passed()
        except Exception as e:
            T.failed(e)

    # New Test
    pairs = (((0,0,0),(0,0,1),True),
             ((0,0,0),(0,0,0),True),
             ((0,0,1),(0,0,2),True),
             ((0,0,2),(0,0,2),True),
             ((0,0,2),(0,1,0),True),
             ((0,1,0),(0,2,0),True),
             ((0,2,0),(0,2,0),True),
             ((0,2,0),(1,0,0),True),
             ((1,0,0),(2,0,0),True),
             ((2,0,0),(2,0,0),True),
             ((0,0,2),(0,0,1),False),
             ((0,1,0),(0,0,2),False),
             ((1,0,0),(0,2,0),False))
    for n, (RGB_1, RGB_2, boolean) in enumerate(pairs):
        T.start(f'__le__ [{n+1}]')
        try:
            color_1 = Color(RGB_1)
            color_2 = Color(RGB_2)
            assert (color_1 <= color_2) is boolean
            T.passed()
        except Exception as e:
            T.failed(e)

    # New Test
    pairs = (((0,0,0),(0,0,1),False),
             ((0,0,1),(0,0,2),False),
             ((0,0,2),(0,1,0),False),
             ((0,1,0),(0,2,0),False),
             ((0,2,0),(1,0,0),False),
             ((1,0,0),(2,0,0),False),
             ((0,0,0),(0,0,0),True),
             ((0,0,2),(0,0,1),True),
             ((0,1,0),(0,0,2),True),
             ((0,1,0),(0,1,0),True),
             ((1,0,0),(0,2,0),True),
             ((1,0,0),(1,0,0),True))
    for n, (RGB_1, RGB_2, boolean) in enumerate(pairs):
        T.start(f'__ge__ [{n+1}]')
        try:
            color_1 = Color(RGB_1)
            color_2 = Color(RGB_2)
            assert (color_1 >= color_2) is boolean
            T.passed()
        except Exception as e:
            T.failed(e)

    # New Test
    pairs = (((0,0,0),(0,0,1),False),
             ((0,0,0),(0,0,0),False),
             ((0,0,1),(0,0,2),False),
             ((0,0,2),(0,0,2),False),
             ((0,0,2),(0,1,0),False),
             ((0,1,0),(0,2,0),False),
             ((0,2,0),(0,2,0),False),
             ((0,2,0),(1,0,0),False),
             ((1,0,0),(2,0,0),False),
             ((2,0,0),(2,0,0),False),
             ((0,0,2),(0,0,1),True),
             ((0,1,0),(0,0,2),True),
             ((1,0,0),(0,2,0),True))
    for n, (RGB_1, RGB_2, boolean) in enumerate(pairs):
        T.start(f'__gt__ [{n+1}]')
        try:
            color_1 = Color(RGB_1)
            color_2 = Color(RGB_2)
            assert (color_1 > color_2) is boolean
            T.passed()
        except Exception as e:
            T.failed(e)

    # New Test
    T.start('__is__ [1]')
    try:
        blue_1 = Color.palette('blue')
        blue_2 = blue_1
        assert blue_1 is blue_2
        T.passed()
    except Exception as e:
        T.failed(e)

    # New Test
    T.start('__is__ [2]')
    try:
        blue_1 = Color.palette('blue')
        blue_2 = Color.palette('blue')
        assert blue_1 is not blue_2
        T.passed()
    except Exception as e:
        T.failed(e)

    # New Test
    T.start('__hash__')
    try:
        blue = Color.palette('blue')
        assert isinstance(hash(blue), int)
        T.passed()
    except Exception as e:
        T.failed(e)

    results = T.end()
    return results

def test_Style():
    '''
        PURPOSE
        Tests for class Style

        RETURNS
        results         <dict>
    '''
    # Importing style data
    from ..data import styles

    # Importing class 'Style' locally
    from ..obj import Style

    # Initializing 'Tester' instance
    T = Tester('class Style')

    # New Test
    T.start('Empty Constructor')
    try:
        style = Style()
        T.passed()
    except Exception as e:
        T.failed(e)

    # New Test
    T.start('Constructor: wrong type')
    try:
        style = Style(5)
        T.failed()
    except TypeError:
        T.passed()

    # New Test
    T.start('Constructor: wrong value')
    try:
        style = Style('pineapple express')
        T.failed()
    except ValueError:
        T.passed()

    # New Test
    keys = list(styles.keys())
    for n, key in enumerate(keys):
        T.start(f'Constructor: 1 style [{n+1}]')
        try:
            style = Style(key)
            T.passed()
        except Exception as e:
            T.failed(e)

    # New Test
    for n, key in enumerate(keys):
        T.start(f'Constructor: 2 styles [{n+1}]')
        try:
            style = Style(key, keys[(n+1)%len(keys)])
            T.passed()
        except Exception as e:
            T.failed(e)

    # New Test
    for n, key in enumerate(keys):
        T.start(f'Constructor: 3 styles [{n+1}]')
        try:
            style = Style(key, keys[(n+1)%len(keys)], keys[(n+2)%len(keys)])
            T.passed()
        except Exception as e:
            T.failed(e)

    # New Test
    for n, key in enumerate(keys):
        T.start(f'check_styles: 1 style [{n+1}]')
        try:
            Style.check_styles([key])
            T.passed()
        except Exception as e:
            T.failed(e)

    # New Test
    for n, key in enumerate(keys):
        T.start(f'check_styles: 2 styles [{n+1}]')
        try:
            Style.check_styles([key, keys[(n+1)%len(keys)]])
            T.passed()
        except Exception as e:
            T.failed(e)

    # New Test
    for n, key in enumerate(keys):
        T.start(f'check_styles: 3 styles [{n+1}]')
        try:
            Style.check_styles([key, keys[(n+1)%len(keys)], keys[(n+2)%len(keys)]])
            T.passed()
        except Exception as e:
            T.failed(e)

    # New Test
    for n, key in enumerate(keys):
        T.start(f'add: 1 style [{n+1}]')
        try:
            style = Style()
            assert style.styles == []
            args = [key]
            args = list(set(args))
            style.add(*args)
            assert sorted(style.styles) == sorted(args)
            T.passed()
        except Exception as e:
            T.failed(e)

    # New Test
    for n, key in enumerate(keys):
        T.start(f'add: 2 styles [{n+1}]')
        try:
            style = Style()
            assert style.styles == []
            args = [key, keys[(n+1)%len(keys)]]
            args = list(set(args))
            style.add(*args)
            assert sorted(style.styles) == sorted(args)
            T.passed()
        except Exception as e:
            T.failed(e)

    # New Test
    for n, key in enumerate(keys):
        T.start(f'add: 3 styles [{n+1}]')
        try:
            style = Style()
            assert style.styles == []
            args = [key, keys[(n+1)%len(keys)], keys[(n+2)%len(keys)]]
            args = list(set(args))
            style.add(*args)
            assert sorted(style.styles) == sorted(args)
            T.passed()
        except Exception as e:
            T.failed(e)

    # New Test
    for n, key in enumerate(keys):
        T.start(f'remove: 1 style [{n+1}]')
        try:
            style = Style(*keys)
            style.remove(key)
            assert key not in style.styles
            T.passed()
        except Exception as e:
            T.failed(e)

    # New Test
    for n, key in enumerate(keys):
        T.start(f'remove: 2 styles [{n+1}]')
        try:
            style = Style(*keys)
            style.remove(key, keys[(n+1)%len(keys)])
            assert key not in style.styles
            assert keys[(n+1)%len(keys)] not in style.styles
            T.passed()
        except Exception as e:
            T.failed(e)

    # New Test
    for n, key in enumerate(keys):
        T.start(f'remove: 3 styles [{n+1}]')
        try:
            style = Style(*keys)
            style.remove(key, keys[(n+1)%len(keys)], keys[(n+2)%len(keys)])
            assert key not in style.styles
            assert keys[(n+1)%len(keys)] not in style.styles
            assert keys[(n+2)%len(keys)] not in style.styles
            T.passed()
        except Exception as e:
            T.failed(e)

    # New Test
    T.start('update')
    try:
        style = Style('bold')
        assert style.sequence == '\x1b[1m'
        style.add('italic')
        style.remove('bold')
        style.update()
        assert style.sequence == '\x1b[3m'
        T.passed()
    except Exception as e:
        T.failed(e)

    # New Test
    T.start('copy')
    try:
        bold_1 = Style('bold')
        bold_2 = bold_1.copy()
        assert bold_1 == bold_2
        assert bold_1 is not bold_2
        T.passed()
    except ValueError as e:
        T.failed(e)

    # New Test
    T.start('__call__: valid arg')
    try:
        bold = Style('bold')
        exp = '\x1b[1mhello world!\x1b[21;22;23;24;25;27;29;55m'
        assert bold('hello world!') == exp
        T.passed()
    except ValueError as e:
        T.failed(e)

    # New Test
    T.start('__call__: invalid arg')
    try:
        bold = Style('bold')
        bold(3)
        T.failed()
    except TypeError:
        T.passed()

    # New Test
    T.start('clear')
    try:
        exp = '\x1b[21;22;23;24;25;27;29;55m'
        assert Style.clear() == exp
        T.passed()
    except TypeError as e:
        T.failed(e)

    # New Test
    T.start('__str__')
    try:
        bold = Style('bold')
        assert isinstance(bold.__str__(), str)
        T.passed()
    except TypeError as e:
        T.failed(e)

    # New Test
    T.start('__repr__')
    try:
        bold = Style('bold')
        assert isinstance(bold.__repr__(), str)
        T.passed()
    except TypeError as e:
        T.failed(e)

    # New Test
    T.start('__hash__')
    try:
        bold = Style('bold')
        assert isinstance(bold.__hash__(), int)
        T.passed()
    except TypeError as e:
        T.failed(e)

    # New Test
    T.start('__eq__')
    try:
        bold_1 = Style('bold')
        bold_2 = Style('bold')
        assert bold_1 == bold_2
        T.passed()
    except TypeError as e:
        T.failed(e)

    # New Test
    T.start('__eq__')
    try:
        bold_1 = Style('bold')
        bold_2 = Style('italic')
        assert bold_1 != bold_2
        T.passed()
    except TypeError as e:
        T.failed(e)

    # New Test
    T.start('list_styles')
    try:
        assert isinstance(Style.list_styles(), str)
        T.passed()
    except TypeError as e:
        T.failed(e)

    results = T.end()

    return results

def test_Pixel():
    '''
        PURPOSE
        Tests for class Pixel

        RETURNS
        results         <dict>
    '''
    # Importing class 'Pixel' locally
    from ..obj import Pixel
    # Importing class 'Color' locally
    from ..obj import Color
    # Importing class 'Style' locally
    from ..obj import Style

    # Initializing 'Tester' instance
    T = Tester('class Pixel')

    blue = Color.palette('blue')
    red = Color.palette('red')
    bold = Style('bold')
    args = ((( blue, None, 'bold',  'a'), True),
            (('red',  red,   None, None), True),
            (( None, blue,   bold,  'b'), True),
            (( blue,'red',   bold, None), True),
            (('red',  red,   None, None), True),
            (( blue, None, 'bold', None), True),
            (( None, None,   bold, None), True),
            (( None, None,   None, None), True),
            (('red',  red,   bold, None), True),
            (( None, blue,   bold,  'b'), True),
            (( blue,'red',   bold, None), True),
            (('red',  red, 'bold', None), True),
            (( blue, None, 'bold', None), True),
            (( None, None,   bold, None), True),
            (( None, None,   None,'abc'), ValueError),
            (('red',  red,    red, None), ValueError),
            (( 'rd', blue,   bold,  'b'), ValueError),
            (( blue, 'rd',   bold, None), ValueError),
            (('red',  red,  'bld', None), ValueError),
            (( blue,    5, 'bold', None), ValueError),
            (( None, None,   blue, None), ValueError),
            (( None, None,      0, None), ValueError),
            ((    5, None,   None, None), ValueError)
           )
    for n,arg in enumerate(args):
        # New Test
        T.start(f'Constructor: args [{n+1}]')
        if arg[1] is True:
            try:
                pixel = Pixel(*arg[0])
                T.passed()
            except Exception as e:
                T.failed(e)
        else:
            try:
                pixel = Pixel(*arg[0])
                T.failed()
                print(arg[0])
            except arg[1]:
                T.passed()

    # New Test
    chars = ('a', 'b', ' ', '#', 'Æ', '+', '!')
    for n, char in enumerate(chars):
        T.start(f'is_char: valid args [{n+1}]')
        try:
            assert Pixel.is_char(char)
            T.passed()
        except Exception as e:
            T.failed(e)

    # New Test
    chars = ('aa', ' b', '', '  ', '\n', '\t', '12', 1, True, 5.5)
    for n, char in enumerate(chars):
        T.start(f'is_char: invalid args [{n+1}]')
        try:
            Pixel.is_char(char)
            T.failed()
        except ValueError:
            T.passed()
        except TypeError:
            T.passed()

    # New Test
    T.start('color_t')
    try:
        pixel = Pixel(color_t = 'red')
        assert pixel.color_t.name == 'red'
        T.passed()
    except Exception as e:
        T.failed(e)

    # New Test
    T.start('color_b')
    try:
        pixel = Pixel(color_b = 'red')
        assert pixel.color_b.name == 'red'
        T.passed()
    except Exception as e:
        T.failed(e)

    # New Test
    T.start('style')
    try:
        pixel = Pixel(style = 'bold')
        assert pixel.style.styles[0] == 'bold'
        assert len(pixel.style.styles) == 1
        T.passed()
    except Exception as e:
        T.failed(e)

    # New Test
    T.start('char')
    try:
        pixel = Pixel(char = 'A')
        assert pixel.char == 'A'
        T.passed()
    except Exception as e:
        T.failed(e)

    # New Test
    args = (red, blue, 'red', 'blue', (0,0,0))
    arg_colors = (Color.palette('red'),
                  Color.palette('blue'),
                  Color.palette('red'),
                  Color.palette('blue'),
                  Color.palette('black'))
    for n, (arg, color) in enumerate(zip(args, arg_colors)):
        T.start(f'set_color_t: valid args [{n+1}]')
        try:
            pixel = Pixel()
            pixel.set_color_t(arg)
            assert pixel.color_t == color
            T.passed()
        except Exception as e:
            T.failed(e)

    # New Test
    args = (bold, 'blae', 5, None, (0,0,0,0), (1,2,300))
    for n, arg in enumerate(args):
        T.start(f'set_color_t: invalid args [{n+1}]')
        try:
            pixel = Pixel()
            pixel.set_color_t(arg)
            T.failed()
        except ValueError:
            T.passed()
        except TypeError:
            T.passed()

    # New Test
    args = (red, blue, 'red', 'blue', (0,0,0))
    arg_colors = (Color.palette('red'),
                  Color.palette('blue'),
                  Color.palette('red'),
                  Color.palette('blue'),
                  Color.palette('black'))
    for n, (arg, color) in enumerate(zip(args, arg_colors)):
        T.start(f'set_color_b: valid args [{n+1}]')
        try:
            pixel = Pixel()
            pixel.set_color_b(arg)
            assert pixel.color_b == color
            T.passed()
        except Exception as e:
            T.failed(e)

    # New Test
    args = (bold, 'blae', 5, None, (0,0,0,0), (1,2,300))
    for n, arg in enumerate(args):
        T.start(f'set_color_b: invalid args [{n+1}]')
        try:
            pixel = Pixel()
            pixel.set_color_b(arg)
            T.failed()
        except ValueError:
            T.passed()
        except TypeError:
            T.passed()

    # New Test
    args = (bold, 'italic', 'bold')
    arg_styles = (Style('bold'),
                  Style('italic'),
                  Style('bold'))
    for n, (arg, style) in enumerate(zip(args, arg_styles)):
        T.start(f'set_style: valid args [{n+1}]')
        try:
            pixel = Pixel()
            pixel.set_style(arg)
            assert pixel.style == style
            T.passed()
        except Exception as e:
            T.failed(e)

    # New Test
    args = (red, 'bld', 5, None)
    for n, arg in enumerate(args):
        T.start(f'set_style: invalid args [{n+1}]')
        try:
            pixel = Pixel()
            pixel.set_style(arg)
            T.failed()
        except ValueError:
            T.passed()
        except TypeError:
            T.passed()

    # New Test
    args = ('a', 'b', ' ', '#', 'Æ', '+', '!')
    for n, arg in enumerate(args):
        T.start(f'set_char: valid args [{n+1}]')
        try:
            pixel = Pixel()
            pixel.set_char(arg)
            assert pixel.char == arg
            T.passed()
        except Exception as e:
            T.failed(e)

    # New Test
    T.start('copy')
    try:
        pixel_1 = Pixel('blue', 'red')
        pixel_2 = pixel_1.copy()
        assert pixel_1 == pixel_2
        assert pixel_1 is not pixel_2
        T.passed()
    except ValueError:
        T.failed()

    # New Test
    args = ('aa', ' b', '', '  ', '\n', '\t', '12', 1, True, 5.5)
    for n, arg in enumerate(args):
        T.start(f'set_char: invalid args [{n+1}]')
        try:
            pixel = Pixel()
            pixel.set_char(arg)
            T.failed()
        except ValueError:
            T.passed()
        except TypeError:
            T.passed()

    # New Test
    T.start('__str__')
    try:
        pixel = Pixel()
        assert isinstance(pixel.__str__(), str)
        T.passed()
    except TypeError:
        T.failed()

    # New Test
    T.start('__hash__')
    try:
        pixel = Pixel()
        assert isinstance(pixel.__hash__(), int)
        T.passed()
    except TypeError:
        T.failed()

    # New Test
    T.start('color_t_seq')
    try:
        pixel = Pixel()
        assert isinstance(pixel.color_t_seq(), str)
        T.failed()
    except TypeError:
        T.passed()

    # New Test
    T.start('color_b_seq')
    try:
        pixel = Pixel()
        assert isinstance(pixel.color_b_seq(), str)
        T.failed()
    except TypeError:
        T.passed()

    # New Test
    T.start('style_seq')
    try:
        pixel = Pixel()
        assert isinstance(pixel.style_seq, str)
        T.passed()
    except TypeError:
        T.failed()

    # New Test
    T.start('end_seq')
    try:
        pixel = Pixel()
        assert isinstance(pixel.end_seq(), str)
        T.failed()
    except TypeError:
        T.passed()

    results = T.end()

    return results

def test_Grid():
    '''
        PURPOSE
        Tests for class Grid

        RETURNS
        results         <dict>
    '''
    # Importing class 'Pixel' locally
    from ..obj import Pixel

    # Importing class 'Grid' locally
    from ..obj import Grid

    # Initializing 'Tester' instance
    T = Tester('class Grid')

    # New Test
    T.start('Empty Constructor')
    try:
        grid = Grid()
        T.failed()
    except Exception:
        T.passed()

    # New Test
    T.start('Constructor: valid arg')
    pixels = [[Pixel() for i in range(5)] for j in range(5)]
    try:
        grid = Grid(pixels)
        T.passed()
    except ValueError:
        T.failed()

    # New Test
    T.start('Constructor: invalid arg [1]')
    pixels = [[Pixel() for i in range(5)] for j in range(5)]
    pixels.append([Pixel()])
    try:
        grid = Grid(pixels)
        T.failed()
    except ValueError:
        T.passed()

    # New Test
    T.start('Constructor: invalid arg [2]')
    pixels = [[Pixel() for i in range(5)] for j in range(5)]
    pixels.append(Pixel())
    try:
        grid = Grid(pixels)
        T.failed()
    except TypeError:
        T.passed()

    # New Test
    T.start('Constructor: invalid arg [3]')
    pixels = [['' for i in range(5)] for j in range(5)]
    try:
        grid = Grid(pixels)
        T.failed()
    except TypeError:
        T.passed()

    # New Test
    T.start('Constructor: invalid arg [4]')
    pixels = [['' for i in range(5)] for j in range(5)]
    pixels[0].append(Pixel())
    try:
        grid = Grid(pixels)
        T.failed()
    except TypeError:
        T.passed()

    # New Test
    T.start('empty: valid arg [1]')
    try:
        grid = Grid.empty((1,40))
        T.passed()
    except Exception as e:
        T.failed(e)

    # New Test
    T.start('empty: valid arg [2]')
    try:
        grid = Grid.empty((10,20))
        T.passed()
    except Exception as e:
        T.failed(e)

    # New Test
    T.start('empty: invalid arg [1]')
    try:
        grid = Grid.empty('A')
        T.failed()
    except TypeError:
        T.passed()

    # New Test
    T.start('empty: invalid arg [2]')
    try:
        grid = Grid.empty((20, 'A'))
        T.failed()
    except TypeError:
        T.passed()

    # New Test
    T.start('empty: invalid arg [3]')
    try:
        grid = Grid.empty((20, -2))
        T.failed()
    except ValueError:
        T.passed()

    # New Test
    T.start('empty: invalid arg [4]')
    try:
        grid = Grid.empty((20, 20, 10))
        T.failed()
    except ValueError:
        T.passed()

    # New Test
    T.start('shape')
    try:
        grid = Grid.empty((20, 10))
        shape = grid.shape
        assert np.array_equal(shape, (20, 10))
        T.passed()
    except ValueError:
        T.failed()

    # New Test
    T.start('height')
    try:
        grid = Grid.empty((20, 10))
        height = grid.height
        assert height == 20
        T.passed()
    except ValueError:
        T.failed()

    # New Test
    T.start('width')
    try:
        grid = Grid.empty((20, 10))
        width = grid.width
        assert width == 10
        T.passed()
    except ValueError:
        T.failed()

    # New Test
    T.start('size')
    try:
        grid = Grid.empty((20, 10))
        size = grid.size
        assert size == 200
        T.passed()
    except ValueError:
        T.failed()

    # New Test
    T.start('ndim [1]')
    try:
        grid = Grid.empty((1, 20))
        ndim = grid.ndim
        assert ndim == 1
        T.passed()
    except ValueError:
        T.failed()

    # New Test
    T.start('ndim [2]')
    try:
        grid = Grid.empty((20, 10))
        ndim = grid.ndim
        assert ndim == 2
        T.passed()
    except ValueError:
        T.failed()

    # New Test
    T.start('ndim [3]')
    try:
        grid = Grid.empty((20, 1))
        ndim = grid.ndim
        assert ndim == 2
        T.passed()
    except ValueError:
        T.failed()

    # New Test
    T.start('__eq__[1]')
    try:
        grid_1 = Grid.empty((20, 10))
        grid_2 = Grid.empty((20, 10))
        assert grid_1 == grid_2
        T.passed()
    except ValueError:
        T.failed()

    # New Test
    T.start('__eq__[2]')
    try:
        grid_1 = Grid.empty((20, 10))
        grid_2 = Grid.empty((10, 10))
        assert not (grid_1 == grid_2)
        T.passed()
    except ValueError:
        T.failed()

    # New Test
    T.start('__neq__[1]')
    try:
        grid_1 = Grid.empty((20, 10))
        grid_2 = Grid.empty((20, 10))
        assert not (grid_1 != grid_2)
        T.passed()
    except ValueError:
        T.failed()

    # New Test
    T.start('__neq__[2]')
    try:
        grid_1 = Grid.empty((20, 10))
        grid_2 = Grid.empty((10, 10))
        assert grid_1 != grid_2
        T.passed()
    except ValueError:
        T.failed()

    # New Test
    arr = [[Pixel(char = '1'), Pixel(char = '5'), Pixel(char = '9')],
           [Pixel(char = '2'), Pixel(char = '6'), Pixel(char = 'a')],
           [Pixel(char = '3'), Pixel(char = '7'), Pixel(char = 'b')],
           [Pixel(char = '4'), Pixel(char = '8'), Pixel(char = 'c')]]
    arr = np.array(arr, dtype = Pixel)
    indices = ((0,0),(3,2),(0),(3),(slice(0,None,2)))
    for n,idx in enumerate(indices):
        T.start(f'__getitem__: valid arg [{n+1}]')
        try:
            exp = arr.__getitem__(idx)
            grid = Grid(arr)
            grid = grid.__getitem__(idx)
            if isinstance(grid, Pixel):
                assert np.array_equal(exp, grid)
            elif exp.ndim == 1:
                assert np.array_equal(exp, grid.data.squeeze())
            else:
                assert np.array_equal(exp, grid.data)
            T.passed()
        except Exception as e:
            T.failed(e)


    # New Test
    indices = ((5,0),(-8,2),('A'),(3.2),(slice(0,1,2),40))
    for n,idx in enumerate(indices):
        T.start(f'__getitem__: invalid arg [{n+1}]')
        try:
            grid = Grid(arr)
            exp = grid.__getitem__(idx)
            T.failed()
        except IndexError:
            T.passed()

    # New Test
    arr2 = [[Pixel(char = 'A'), Pixel(char = 'E'), Pixel(char = 'I')],
            [Pixel(char = 'B'), Pixel(char = 'F'), Pixel(char = 'J')],
            [Pixel(char = 'C'), Pixel(char = 'G'), Pixel(char = 'K')],
            [Pixel(char = 'D'), Pixel(char = 'H'), Pixel(char = 'L')]]
    arr2 = np.array(arr2, dtype = Pixel)
    indices = ((0,0),(3,2),(0),(3),(slice(0,None,2)))
    for n,idx in enumerate(indices):
        T.start(f'__setitem__: valid arg [{n+1}]')
        try:
            new_arr = arr2.__getitem__(idx)
            grid = Grid(arr)
            grid.__setitem__(idx, new_arr)
            subgrid = grid.__getitem__(idx)
            if isinstance(new_arr, Pixel):
                assert new_arr == subgrid
            elif new_arr.ndim == 1:
                assert np.array_equal(new_arr, subgrid.data.squeeze())
            else:
                assert np.array_equal(new_arr, subgrid.data)
            T.passed()
        except Exception as e:
            T.failed(e)

    # New Test
    indices = ((0),(3),(slice(0,None,2)),(slice(0,3,2)),(slice(0,3,1)))
    for n,idx in enumerate(indices):
        T.start(f'__setitem__: valid arg [{n+len(indices)+1}]')
        try:
            new_arr = arr2.__getitem__(idx)
            if new_arr.ndim == 1:
                new_arr = new_arr[None,:]
            new_arr = Grid(new_arr)
            grid = Grid(arr)
            grid.__setitem__(idx, new_arr)
            subgrid = grid.__getitem__(idx)
            assert new_arr == subgrid
            T.passed()
        except Exception as e:
            T.failed(e)

    # New Test
    T.start('__setitem__: invalid arg')
    try:
        grid = Grid.empty((20, 20))
        grid.__setitem__(0, 'A')
        T.failed()
    except ValueError:
        T.passed()

    # New Test
    T.start('__setitem__: invalid arg')
    try:
        grid = Grid.empty((20, 20))
        grid.__setitem__('A', 0)
        T.failed()
    except ValueError:
        T.passed()

    # New Test
    T.start('__str__')
    try:
        grid = Grid.empty((20, 10))
        assert isinstance(grid.__str__(), str)
        T.passed()
    except ValueError:
        T.failed()

    # New Test
    T.start('__repr__')
    try:
        grid = Grid.empty((20, 10))
        assert isinstance(grid.__repr__(), str)
        T.passed()
    except ValueError:
        T.failed()

    results = T.end()
    return results

def test_Term():
    '''
        PURPOSE
        Tests for class Term

        RETURNS
        results         <dict>
    '''

    # Importing class 'Pixel' locally
    from ..obj import Pixel

    # Importing class 'Grid' locally
    from ..obj import Grid

    # Importing class 'Term' locally
    from ..obj import Term
    Term.resize_console((24, 80))

    import shutil
    from ..config import term_width, term_height

    # Initializing 'Tester' instance
    T = Tester('class Term')
    # T = Tester('class Term', dev = True)

    # New Test
    T.start('Empty Constructor')
    try:
        term = Term()
        T.passed()
    except Exception as e:
        T.failed(e)

    # New Test
    args = ((10, 20), (5, 5), (1, 2))
    for n,arg in enumerate(args):
        T.start(f'Constructor: valid args [{n+1}]')
        try:
            term = Term(arg)
            T.passed()
        except Exception as e:
            T.failed(e)
    # New Test
    args = ((10), ('A', 5), (1, 2, 20), 'B', 5)
    for n,arg in enumerate(args):
        T.start(f'Constructor: invalid args [{n+1}]')
        try:
            term = Term(arg)
            T.failed()
        except:
            T.passed()

    # New Test
    arr = [[Pixel(char = '1'), Pixel(char = '5'), Pixel(char = '9')],
           [Pixel(char = '2'), Pixel(char = '6'), Pixel(char = 'a')],
           [Pixel(char = '3'), Pixel(char = '7'), Pixel(char = 'b')],
           [Pixel(char = '4'), Pixel(char = '8'), Pixel(char = 'c')]]
    arr = np.array(arr, dtype = Pixel)
    T.start('from_grid')
    try:
        term = Term.from_grid(Grid(arr))
        assert term.grid == Grid(arr)
        T.passed()
    except Exception as e:
        T.failed(e)

    # New Test
    T.start('shape')
    try:
        term = Term((20, 10))
        shape = term.shape
        assert np.array_equal(shape, (20, 10))
        T.passed()
    except ValueError:
        T.failed()

    # New Test
    T.start('height')
    try:
        term = Term((20, 10))
        height = term.height
        assert height == 20
        T.passed()
    except ValueError:
        T.failed()

    # New Test
    T.start('width')
    try:
        term = Term((20, 10))
        width = term.width
        assert width == 10
        T.passed()
    except ValueError:
        T.failed()

    # New Test
    T.start('size')
    try:
        term = Term((20, 10))
        size = term.size
        assert size == 200
        T.passed()
    except ValueError:
        T.failed()

    # New Test
    T.start('live')
    try:
        term = Term((20, 10))
        assert not term.live
        term.live_bool = True
        assert term.live
        T.passed()
    except ValueError:
        T.failed()

    # New Test
    indices = ((0,0),(3,2),(0),(3),(slice(0,None,2)))
    for n,idx in enumerate(indices):
        T.start(f'__getitem__: valid arg [{n+1}]')
        try:
            exp = arr.__getitem__(idx)
            term = Term.from_grid(Grid(arr))
            grid = term.__getitem__(idx)
            if isinstance(grid, Pixel):
                assert np.array_equal(exp, grid)
            elif exp.ndim == 1:
                assert np.array_equal(exp, grid.data.squeeze())
            else:
                assert np.array_equal(exp, grid.data)
            T.passed()
        except Exception as e:
            T.failed(e)

    # New Test
    indices = ((5,0),(-8,2),('A'),(3.2),(slice(0,1,2),40))
    for n,idx in enumerate(indices):
        T.start(f'__getitem__: invalid arg [{n+1}]')
        try:
            term = Term.from_grid(Grid(arr))
            exp = arr.__getitem__(idx)
            T.failed()
        except IndexError:
            T.passed()

    # New Test
    T.start('__str__')
    try:
        term = Term((20, 10))
        assert isinstance(term.__str__(), str)
        T.passed()
    except ValueError:
        T.failed()

    # New Test
    T.start('__repr__')
    try:
        term = Term((20, 10))
        assert isinstance(term.__repr__(), str)
        T.passed()
    except ValueError:
        T.failed()

    # New Test
    arr2 = [[Pixel(char = 'A'), Pixel(char = 'E'), Pixel(char = 'I')],
            [Pixel(char = 'B'), Pixel(char = 'F'), Pixel(char = 'J')],
            [Pixel(char = 'C'), Pixel(char = 'G'), Pixel(char = 'K')],
            [Pixel(char = 'D'), Pixel(char = 'H'), Pixel(char = 'L')]]
    arr2 = np.array(arr2, dtype = Pixel)
    indices = ((0,0),(3,2),(0),(3),(slice(0,None,2)))
    for n,idx in enumerate(indices):
        T.start(f'__setitem__: valid arg [{n+1}]')
        try:
            new_arr = arr2.__getitem__(idx)
            term = Term.from_grid(Grid(arr2))
            term.__setitem__(idx, new_arr)
            subgrid = term.__getitem__(idx)
            if isinstance(new_arr, Pixel):
                assert new_arr == subgrid
            elif new_arr.ndim == 1:
                assert np.array_equal(new_arr, subgrid.data.squeeze())
            else:
                assert np.array_equal(new_arr, subgrid.data)
            T.passed()
        except Exception as e:
            T.failed(e)

    # New Test
    indices = ((0),(3),(slice(0,None,2)),(slice(0,3,2)),(slice(0,3,1)))
    for n,idx in enumerate(indices):
        T.start(f'__setitem__: valid arg [{n+len(indices)+1}]')
        try:
            new_arr = arr2.__getitem__(idx)
            if new_arr.ndim == 1:
                new_arr = new_arr[None,:]
            new_arr = Grid(new_arr)
            term = Term.from_grid(Grid(arr))
            term.__setitem__(idx, new_arr)
            subgrid = term.__getitem__(idx)
            assert new_arr == subgrid
            T.passed()
        except Exception as e:
            T.failed(e)

    # New Test
    T.start('__setitem__: invalid arg')
    try:
        term = Term((20, 20))
        term.__setitem__(0, 'A')
        T.failed()
    except ValueError:
        T.passed()

    # New Test
    T.start('__setitem__: invalid arg')
    try:
        term = Term((20, 20))
        term.__setitem__('A', 0)
        T.failed()
    except ValueError:
        T.passed()

    # New Test
    T.start('locked')
    try:
        term = Term((20, 10))
        Term.lock_bool = True
        assert term.locked()
        Term.lock_bool = False
        assert not term.locked()
        T.passed()
    except ValueError:
        T.failed()

    # New Test
    T.start('resize_console')
    try:
        term = Term((30, 30))
        Term.resize_console((30, 30))
        Term.resize_console(term.term_shape)
        T.passed()
    except ValueError as e:
        T.failed(e)

    # New Test
    T.start('__enter__ & __exit__')
    try:
        term = Term((20, 10))
        assert not Term.locked()
        with term:
            assert Term.locked()
        assert not Term.locked()
        T.passed()
    except ValueError:
        T.failed()

    results = T.end()
    return results
