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

\__init__(RGB, name = 'Unnamed Color')
rename(name)
reset_RGB(RGB)
\__str__()
\__repr__()
\__add__(color)
\__sub__(color)
\__eq__(color)
\__ne__(color)
\__lt__(color)
\__gt__(color)
\__le__(color)
\__ge__(color)
\__is__(color)    

## Class Style

### Minimal Example

## Class Pixel

### Minimal Example

## Class Grid

### Minimal Example

## Class Painter

### Minimal Example
