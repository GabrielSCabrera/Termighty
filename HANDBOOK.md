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

Parameter `name` is optional, and should be a string that will be given name of the instance's color.

**rename**(name)

**reset_RGB**(RGB)

**\_\_str\_\_**()

**\_\_repr\_\_**()

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
