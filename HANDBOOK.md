# Reference

## Program Structure
The program as it is organized in the filesystem

     └── Termighty
       ├── config
       │   └── defaults.py
       ├── data
       │   ├── ANSI.py
       │   └── RGB.py
       ├── obj
       │   ├── Color.py
       │   ├── Grid.py
       │   ├── Pixel.py
       │   └── Style.py
       ├── tests
       │   └── Tester.py
       ├── tools
       │   └── painter.py
       └── utils
           ├── checkers.py
           ├── format.py
           └── interpreters.py

## Module Structure
The program as it should be accessed by the user when imported

    └── Termighty                   <module>
      ├── Color                       <class>
      ├── Grid                        <class>
      ├── Pixel                       <class>
      ├── Style                       <class>
      └── tools                       <module>
          └── Painter                   <class>

Much of the program is dedicated to internal management, and should never be
accessed by the user

## <class 'Color'>

## Minimal Example

    >>> import termighty as tm
    >>> color = tm.Color((31,41,59))      # Creating an arbitrary color
    >>> blue = tm.Color.palette('blue')   # Creating a color from a known color name

### Instance Methods

#### Color.\_\_init\_\_(RGB, name = 'Unnamed Color')

Constructor requires `RGB`: a tuple of three integers.  These integers must be values from 0 up to and including 255 – they represent red, green, and blue (RGB) color channels respectively.

Parameter `name` is optional, and should be the name of the instance's color.

    >>> color = tm.Color(RGB = (31,41,59), name = 'pi color')

---
#### Color.rename(name)

Change the name of the instance by passing a string to `name`.

    >>> color = tm.Color(RGB = (255,0,0), name = 'blue')  # Wrong name/color pair
    >>> color.rename('red')                               # Name fixed

---
#### Color.reset_RGB(RGB)

Change the RGB values of the instance by passing a three-tuple of integers from 0 up to and including 255 to `RGB`.

    >>> color = tm.Color(RGB = (255,0,0), name = 'blue')  # Wrong name/color pair
    >>> color.reset_RGB((0,0,255))                        # Color fixed

---
#### Color.\_\_str\_\_()

Print the color and its metadata to the terminal.

    >>> color = tm.Color.palette('black')
    >>> print(color)
    COLOR NAME      BLACK
    RGB             000 000 000
    SAMPLE          ███████████

---
#### Color.\_\_add\_\_(color)

Return a *Color* instance whose RGB values comprise of the sum of two other instances. RGB values over 255 are truncated to 255.

    >>> red = tm.Color.palette('red')
    >>> blue = tm.Color.palette('blue')
    >>> purple = red + blue

---
#### Color.\_\_sub\_\_(color)

Return a *Color* instance whose RGB values comprise of the sum of two other instances. RGB values below 0 are set to 0.

    >>> red = tm.Color.palette('red')
    >>> purple = tm.Color.palette('purple')
    >>> blue = purple  - red

---
#### Color.\_\_is\_\_(color)

Checks if two supposed instances of *Color* point to the same memory location.

    >>> red1 = tm.Color.palette('red')
    >>> red2 = red1
    >>> red3 = tm.Color.palette('red')
    >>> print(red1 is red2)
    True
    >>> print(red1 is red3)
    False

---
#### Color.\_\_eq\_\_(color)

Checks if two instances of *Color* have the same RGB values.

    >>> red1 = tm.Color.palette('red')
    >>> red2 = tm.Color.palette('red')
    >>> blue = tm.Color.palette('blue')
    >>> print(red1 == red2)
    True
    >>> print(red1 == blue)
    False

---
#### Color.\_\_neq\_\_(color)

Checks if two instances of *Color* have different RGB values.

    >>> red1 = tm.Color.palette('red')
    >>> red2 = tm.Color.palette('red')
    >>> blue = tm.Color.palette('blue')
    >>> print(red1 != red2)
    False
    >>> print(red1 != blue)
    True

---
### Static Methods

#### Color.palette(name)

Returns an instance of *Color* whose `RGB` values are identified based on the given `name`.  If the color is invalid, an exception is raised.

    >>> red = tm.Color.palette('red')
    >>> blue = tm.Color.palette('blue')

---
#### Color.chart(R = None, G = None, B = None, term\_width = 80)
Returns a printable chart showing a 2-D color gradient field for red & green, green & blue, or blue & red.  By passing `R = 0`, we would hold the red portion of the RGB color channels constant at zero.

Must set exactly one of the parameters *R*, *G*, and *B* to a value
in range [0, 255].  The others must be set to None.

`term_width` should be an integer, and will determine the chart width.

    >>> tm.Color.chart(R = 0, term_width = 10)
    ██████████
    ██████████
    ██████████
    ██████████
    ██████████

---
#### Color.list\_colors()

Lists all names colors with a sample and RGB value.

    >>> tm.Color.list_colors()
    █ 000 000 000 BLACK
    █ 000 000 127 NAVY BLUE
    █ 000 000 155 DUKE BLUE
    █ 000 000 204 MEDIUM BLUE
    ⋮
    █ 255 255 225 LIGHT YELLOW
    █ 255 255 240 IVORY
    █ 255 255 250 BABY POWDER
    █ 255 255 255 WHITE

---
### Property Methods

#### Color.RGB

Returns the three-element `numpy.ndarray` of `dtype= numpy.uint8` which contains all RGB color data.

    >>> color = tm.Color((12,34,56))
    >>> print(color.RGB)
    [12 34 56]

---
#### Color.R

Returns the red RGB color data.

    >>> color = tm.Color((12,34,56))
    >>> print(color.R)
    12

---
#### Color.G

Returns the green RGB color data.

    >>> color = tm.Color((12,34,56))
    >>> print(color.G)
    34

---
#### Color.B

Returns the blue RGB color data.

    >>> color = tm.Color((12,34,56))
    >>> print(color.B)
    56

---
#### Color.sample

Returns a color sample as a string.

    >>> color = tm.Color.palette('blue')
    >>> print(color.sample)
    █

---
## Class Style

### Minimal Example

    >>> import termighty as tm
    >>> bold = tm.Style('bold')           # Creating a 'bold' style
    >>> bold_string = bold('Hello World') # Will be bold when printed to terminal

### Instance Methods

#### \_\_init\_\_(styles = None)

Initializes the *Style* instance, with any number of valid <str> arguments.

    >>> style_1 = tm.Style()                      # Creating an empty style
    >>> style_2 = tm.Style('italic')              # Creating an italic style
    >>> style_3 = tm.Style('underline', 'blink')  # Creating an underlined & blinking style

##### Valid Arguments

| Argument | Effect |
| --- | --- |
| bold | Bold (thicker) text |
| faint | Fainter text |
| italic | Italic (askew) text |
| underline | Underlined text |
| blink | Blinking text |
| reverse | Text & background colors switch |
| crossed out | Text is crossed out |
| overlined | Overlined text |

#### add(styles)

#### \_\_iadd\_\_(styles)

#### \_\_call\_\_(string)

#### \_\_str\_\_()

### Static Methods

#### check\_styles(styles)
#### clear()
#### list\_styles()

## Class Pixel

### Minimal Example

### Instance Methods

#### \_\_init\_\_(color\_t = None, color\_b = None, style = None, char = None)
#### update\_color_t(color)
#### update\_color_b(color)
#### update\_style(style)
#### update\_char(char)
#### \_\_str\_\_()

### Static Methods

#### is\_char(char)

### Property Methods

#### color\_t\_seq
#### color\_b\_seq
#### style\_seq
#### end\_seq
#### color\_t
#### color\_b
#### style
#### char

## Class Grid

### Minimal Example

### Instance Methods

### Static Methods

### Property Methods

## Class Painter

### Minimal Example

### Instance Methods

### Static Methods

### Property Methods
