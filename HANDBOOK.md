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

&ensp; **\_\_init\_\_**(RGB, name = 'Unnamed Color')
&ensp; **rename**(name)
&ensp; **reset_RGB**(RGB)
&ensp; **\_\_str\_\_**()
&ensp; **\_\_repr\_\_**()
&ensp; **\_\_add\_\_**(color)
&ensp; **\_\_sub\_\_**(color)
&ensp; **\_\_is\_\_**(color)

## Class Style

### Minimal Example

## Class Pixel

### Minimal Example

## Class Grid

### Minimal Example

## Class Painter

### Minimal Example
