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

## Class Color

### Minimal Example

    import termighty as tm

    color = tm.Color((31,41,59))      # Creating an arbitrary color
    blue = tm.Color.palette('blue')   # Creating a color from a known color name

### Instance Methods

**\_\_init\_\_**(RGB, name = 'Unnamed Color')

Constructor requires `RGB`: a tuple of three integers.  These integers must be values from 0 up to and including 255 – they represent red, green, and blue (RGB) color channels respectively.

Parameter `name` is optional, and should be the name of the instance's color.

    color = tm.Color(RGB = (31,41,59), name = 'pi color')

**rename**(name)

Change the name of the instance by passing a string to `name`.

    color = tm.Color(RGB = (255,0,0), name = 'blue')  # Wrong name/color pair
    color.rename('red')                               # Name fixed


**reset_RGB**(RGB)

Change the RGB values of the instance by passing a three-tuple of integers from 0 up to and including 255 to `RGB`.

    color = tm.Color(RGB = (255,0,0), name = 'blue')  # Wrong name/color pair
    color.reset_RGB((0,0,255))                        # Color fixed

**\_\_str\_\_**()

Print the color and its metadata to the terminal.

    color = tm.Color.palette('black')
    print(color)

    \>\>\> 



**\_\_add\_\_**(color)

**\_\_sub\_\_**(color)

**\_\_is\_\_**(color)

## Class Style

### Minimal Example

## Class Pixel

### Minimal Example

## Class Grid

### Minimal Example

## Class Painter

### Minimal Example
