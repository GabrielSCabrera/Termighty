# Reference

## Table of Contents

    ├──Program Structure
    ├──Module Structure
    ├──class Color
    │  ├── Minimal Example
    │  ├── Instance Methods
    │  │   ├── Color.__init__
    │  │   ├── Color.set_name
    │  │   ├── Color.set_RGB
    │  │   ├── Color.copy
    │  │   ├── Color.__str__
    │  │   ├── Color.__add__
    │  │   ├── Color.__sub__
    │  │   ├── Color.__is__
    │  │   ├── Color.__eq__
    │  │   └── Color.__neq__
    │  ├── Static Methods
    │  │   ├── Color.palette
    │  │   ├── Color.chart
    │  │   └── Color.list_colors
    │  └── Properties
    │      ├── Color.RGB
    │      ├── Color.R
    │      ├── Color.G
    │      ├── Color.B
    │      └── Color.sample
    ├──class Style
    │  ├── Minimal Example
    │  ├── Instance Methods
    │  │   ├── Style.__init__
    │  │   ├── Style.add
    │  │   ├── Style.remove
    │  │   ├── Style.copy
    │  │   ├── Style.__call__
    │  │   ├── Style.__str__
    │  │   ├── Style.__eq__
    │  │   └── Style.__neq__
    │  └── Static Methods
    │      ├── Style.clear
    │      └── Style.list_styles
    ├──class Pixel
    │  ├── Minimal Example
    │  ├── Instance Methods
    │  │   ├── Pixel.__init__
    │  │   ├── Pixel.set_color_t
    │  │   ├── Pixel.set_color_b
    │  │   ├── Pixel.set_style
    │  │   ├── Pixel.set_char
    │  │   └── Pixel.__str__
    │  └── Properties
    │      ├── Pixel.color_t
    │      ├── Pixel.color_b
    │      ├── Pixel.style
    │      └── Pixel.char
    ├──class Grid
    ├──class Painter

## Program Structure
The program as it is organized in the file-system.

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

## Package Structure
The package as it is accessed by the user when imported.

    └── [module] Termighty
      ├── [class] Color
      ├── [class] Grid
      ├── [class] Pixel
      ├── [class] Style
      └── [module] tools
          └── [class] Painter

Much of the program is dedicated to internal management, and should never be
accessed by the user

## class Color

### Minimal Example

Creating a color with an arbitrary set of RGB values, as well as the color *blue*.

    >>> import termighty as tm
    >>> color = tm.Color((31,41,59))      # Creating an arbitrary color
    >>> blue = tm.Color.palette('blue')   # Creating a color from a known color name

### Instance Methods

#### Color.\_\_init\_\_(RGB, name = 'Unnamed Color')

Constructor requires `RGB`: a tuple of three integers.  These integers must be values from 0 up to and including 255 – they represent red, green, and blue (RGB) color channels respectively.

Parameter `name` is optional, and should be the name of the instance's color.

    >>> color = tm.Color(RGB = (31,41,59), name = 'pi color')

___
#### Color.set_name(name)

Change the name of the instance by passing a string to `name`.

    >>> color = tm.Color(RGB = (255,0,0), name = 'blue')  # Wrong name/color pair
    >>> color.set_name('red')                             # Name fixed

___
#### Color.set_RGB(RGB)

Change the RGB values of the instance by passing a three-tuple of integers from 0 up to and including 255 to `RGB`.

    >>> color = tm.Color(RGB = (255,0,0), name = 'blue')  # Wrong name/color pair
    >>> color.set_RGB((0,0,255))                          # Color fixed

___
#### Color.copy()

Return a deep copy of the instance, in order to prevent memory issues.

    >>> green_1 = tm.Color.palette('green')
    >>> green_2 = green_1
    >>> green_3 = green_1.copy()
    >>> print(green_1 == green_2)
    True
    >>> print(green_1 == green_3)
    True
    >>> print(green_1 is green_2)
    True
    >>> print(green_1 is green_3)
    False
___
#### Color.set_R(R)

Change the red value of the instance in its RGB array to a new integer in range 0 up to and including 255.

    >>> color = tm.Color(RGB = (0,0,0), name = 'red')   # Wrong name/color pair
    >>> color.set_R(255)                                # Color fixed

___
#### Color.set_G(G)

Change the green value of the instance in its RGB array to a new integer in range 0 up to and including 255.

    >>> color = tm.Color(RGB = (0,0,0), name = 'green') # Wrong name/color pair
    >>> color.set_G(255)                                # Color fixed

___
#### Color.set_B(B)

Change the blue value of the instance in its RGB array to a new integer in range 0 up to and including 255.

    >>> color = tm.Color(RGB = (0,0,0), name = 'blue')  # Wrong name/color pair
    >>> color.set_B(255)                                # Color fixed

___
#### Color.\_\_str\_\_()

Print the color and its metadata to the terminal.

    >>> color = tm.Color.palette('black')
    >>> print(color)
    COLOR NAME      BLACK
    RGB             000 000 000
    SAMPLE          ███████████

___
#### Color.\_\_add\_\_(color)

Return a *Color* instance whose RGB values comprise of the sum of two other instances. RGB values over 255 are truncated to 255.

    >>> red = tm.Color.palette('red')
    >>> blue = tm.Color.palette('blue')
    >>> purple = red + blue

___
#### Color.\_\_sub\_\_(color)

Return a *Color* instance whose RGB values comprise of the sum of two other instances. RGB values below 0 are set to 0.

    >>> red = tm.Color.palette('red')
    >>> purple = tm.Color.palette('purple')
    >>> blue = purple  - red

___
#### Color.\_\_is\_\_(color)

Checks if two supposed instances of *Color* point to the same memory location.

    >>> red1 = tm.Color.palette('red')
    >>> red2 = red1
    >>> red3 = tm.Color.palette('red')
    >>> print(red1 is red2)
    True
    >>> print(red1 is red3)
    False

___
#### Color.\_\_eq\_\_(color)

Checks if two instances of *Color* have the same RGB values.

    >>> red1 = tm.Color.palette('red')
    >>> red2 = tm.Color.palette('red')
    >>> blue = tm.Color.palette('blue')
    >>> print(red1 == red2)
    True
    >>> print(red1 == blue)
    False

___
#### Color.\_\_neq\_\_(color)

Checks if two instances of *Color* have different RGB values.

    >>> red1 = tm.Color.palette('red')
    >>> red2 = tm.Color.palette('red')
    >>> blue = tm.Color.palette('blue')
    >>> print(red1 != red2)
    False
    >>> print(red1 != blue)
    True

___
### Static Methods

#### Color.palette(name)

Returns an instance of *Color* whose `RGB` values are identified based on the given `name`.  If the color is invalid, an exception is raised.

    >>> red = tm.Color.palette('red')
    >>> blue = tm.Color.palette('blue')

___
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

___
#### Color.list\_colors()

Lists all named colors with a sample and RGB value.

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

___
### Properties

#### Color.name

Returns the name of the color as a <str>

    >>> color = tm.Color.palette('black')
    >>> print(color.name)
    black

#### Color.RGB

Returns the three-element `numpy.ndarray` of `dtype= numpy.uint8` which contains all RGB color data.

    >>> color = tm.Color((12,34,56))
    >>> print(color.RGB)
    [12 34 56]

___
#### Color.R

Returns the red RGB color data.

    >>> color = tm.Color((12,34,56))
    >>> print(color.R)
    12

___
#### Color.G

Returns the green RGB color data.

    >>> color = tm.Color((12,34,56))
    >>> print(color.G)
    34

___
#### Color.B

Returns the blue RGB color data.

    >>> color = tm.Color((12,34,56))
    >>> print(color.B)
    56

___
#### Color.sample

Returns a color sample as a string.

    >>> color = tm.Color.palette('blue')
    >>> print(color.sample)
    █

___
## class Style

### Minimal Example

Creating a *bold* style and making a string ready-to-print in bold to the terminal.

    >>> import termighty as tm
    >>> bold = tm.Style('bold')           # Creating a 'bold' style
    >>> bold_string = bold('Hello World') # Will be bold when printed to terminal

### Instance Methods

#### Style.\_\_init\_\_(\*styles)

Initializes the *Style* instance, with any number of valid *str* arguments.

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

___
#### Style.add(\*styles)

Add new styles to the current instance.

    >>> bold = tm.Style('bold')
    >>> bold.add('italic')
    >>> bold.add('underline', 'blink')

___
#### Style.remove(\*styles)

Removes existing styles from the current instance.

    >>> style = tm.Style('bold','underline', 'blink')
    >>> style.remove('underline', 'blink')
    >>> style.remove('bold')

___
#### Style.copy()

Return a deep copy of the instance, in order to prevent memory issues.

    >>> bold_1 = tm.Style('bold')
    >>> bold_2 = bold_1
    >>> bold_3 = bold_1.copy()
    >>> print(bold_1 == bold_2)
    True
    >>> print(bold_1 == bold_3)
    True
    >>> print(bold_1 is bold_2)
    True
    >>> print(bold_1 is bold_3)
    False
___
#### Style.\_\_call\_\_(string)

Returns argument *string* (which must be of type *str*) with style formatting implemented.

    >>> bold = tm.Style('bold')
    >>> greeting = 'Hello World!'
    >>> bold_greeting = bold(greeting)
___
#### Style.\_\_str\_\_()

Prints out information about the current *Style* instance.

    >>> style = tm.Style('italic', 'bold')
    >>> print(style)
    STYLES  italic bold
    SAMPLE  Aa Zz 0123
___
#### Style.\_\_eq\_\_(style)

Checks if two instances of *Style* have the same applied styles.

    >>> bold1 = tm.Style.palette('red')
    >>> bold2 = tm.Style.palette('red')
    >>> italic = tm.Style.palette('italic')
    >>> print(bold1 != bold2)
    True
    >>> print(bold1 != italic)
    False
___
#### Style.\_\_neq\_\_(style)

Checks if two instances of *Style* have different applied styles.

    >>> bold1 = tm.Style.palette('bold')
    >>> bold2 = tm.Style.palette('bold')
    >>> italic = tm.Style.palette('italic')
    >>> print(bold1 != bold2)
    False
    >>> print(bold1 != italic)
    True
___
### Static Methods

#### Style.clear()

Returns a string that will reset the terminal's character style, without affecting any other properties (such as color).

    >>> print('\\033[1m')
    >>> print('BOLD TEXT')
    >>> print(tm.Style.clear())
    STYLES  italic bold
    SAMPLE  Aa Zz 0123
___
#### Style.list\_styles()

Lists all styles with a sample.

    >>> tm.Style.list_styles()
    STYLES
            bold
           faint
          italic
       underline
           blink
         reverse
     crossed out
       overlined
___
## class Pixel

### Minimal Example

Creating a *Pixel* instance with red text, a blue background, and the character *T*.

    >>> import Termighty as tm
    >>> pixel = tm.Pixel(color_t = 'red', color_b = 'blue', char = 'T')

### Instance Methods

#### Pixel.\_\_init\_\_(color\_t = None, color\_b = None, style = None, char = None)

Initialize an instance of *Pixel*.

    >>> pixel = tm.Pixel()

##### Constructor Arguments

 | Optional Parameter | Expects |
 | --- | --- |
 | `color_t` | *Color* instance, 3-tuple of unsigned 8-bit integers, or color name |
 | `color_b` | *Color* instance, 3-tuple of unsigned 8-bit integers, or color name |
 | `style` | *Style* instance or style name |
 | `char` | *str* of length one |

___
#### Pixel.set\_color_t(color)

Set the current instance's text color.

    >>> pixel = tm.Pixel()
    >>> pixel.set_color_t('blue')

___
#### Pixel.set\_color_b(color)

Set the current instance's background color.

    >>> pixel = tm.Pixel()
    >>> pixel.set_color_t('red')

___
#### Pixel.set\_style(style)

Set the current instance's style.

    >>> pixel = tm.Pixel()
    >>> pixel.set_style('bold')

___
#### Pixel.set\_char(char)

Set the current instance's character.

    >>> pixel = tm.Pixel()
    >>> pixel.set_char('T')

___
#### Pixel.\_\_str\_\_()

Print the current pixel as it is meant to be displayed.

    >>> pixel = tm.Pixel(char = '█')
    >>> print(pixel)
    █
___
### Properties

#### Pixel.color\_t

Returns the pixel's text color.

    >>> pixel = tm.Pixel()
    >>> color_t = pixel.color_t
    >>> print(color_t)
    COLOR NAME      WHITE
    RGB             255 255 255
    SAMPLE          ███████████
___
#### Pixel.color\_b

Returns the pixel's background color.

    >>> pixel = tm.Pixel()
    >>> color_b = pixel.color_b
    >>> print(color_b)
    COLOR NAME      BLACK
    RGB             000 000 000
    SAMPLE          ███████████

___
#### Pixel.style

Returns the pixel's style.

    >>> pixel = tm.Pixel(style = 'bold')
    >>> style = pixel.style
    >>> print(style)
    STYLES  bold
    SAMPLE  Aa Zz 0123

___
#### Pixel.char

Returns the pixel's character.

    >>> pixel = tm.Pixel(char = 'A')
    >>> char = pixel.char
    >>> print(char)
    A

___
## class Grid

### Minimal Example

### Instance Methods

### Static Methods

### Properties

## class Painter

### Minimal Example

### Instance Methods

### Static Methods

### Properties
