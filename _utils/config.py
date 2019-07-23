import os, sys, string, time, math

"""Terminal Settings"""

os_nt = os.name == 'nt'         # Whether the operating system is windows-based
default_term_h = 24             # Ubuntu Default Terminal Height
default_term_w = 80             # Ubuntu Default Terminal Width
term_h = default_term_h         # Current Terminal Height
term_w = default_term_w         # Current Terminal Width
cursor_allowed = True           # Whether the cursor is shown or not
input_allowed = True            # Whether the terminal accepts input

"""Color Guides"""

# Allowed colors and styles, their unicode values, and their single-char
# aliases used for data storage and image creation.

text_colors = {"black":30, "k":30, "red":31, "r":31, "green":32,
"g":32, "yellow":33, "y":33, "blue":34, "b":34, "purple":35, "p":35,
"cyan":36, "c":36, "white":37, "w":37, "default":37, "d":37}

back_colors = {"black":40, "k":40, "red":41, "r":41, "green":42,
"g":42, "yellow":43, "y":43, "blue":44, "b":44, "purple":45, "p":45,
"cyan":46, "c":46, "white":47, "w":47, "default":1, "d":1}

styles = {"default":0, "d":0, "bold":1, "b":1, "faded":2, "f":2,
"italic":3, "i":3, "underlined":4, "u":4, "negative":7, "n":7,
"strikethrough":9, "s":9}

aliases_color = {"black":"k", "red":"r", "green":"g", "yellow":"y",
"blue":"b", "purple":"p", "cyan":"c", "white":"w", "default":"d"}

aliases_style = {"default":"d", "bold":"b", "faded":"f",
"italic":"i", "underlined":"u", "negative":"n", "strikethrough":"s"}
