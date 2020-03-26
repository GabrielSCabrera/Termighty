import tkinter as tk
import numpy as np

from ..obj import Color, Pixel
from ..config import defaults

class Painter:

    def __init__(self, shape = (defaults.term_height, defaults.term_width)):
        '''
            PURPOSE
            Object that can run a tkinter-based painting application, and whose
            data can be accessed at any time.

            The painting application is meant to emulate the terminal's
            characters, and the 'shape' parameter represents the painter's
            shape in terms of terminal characters.

            The first element of 'shape' should be the number of rows of
            characters in the terminal (terminal height), and the second should
            be the number of characters per row in the terminal (terminal width)

            PARAMETERS
            shape       <tuple> containing two elements of <class 'int'>
        '''


        # The height and width of the application window in pixels
        self.shape_px = (self.height*10, self.width*10)
        self.height_px = self.shape_px[0]
        self.width_px = self.shape_px[1]

        arr = np.empty((self.height, self.width), dtype = Color)

        color = 'black'

        for i in range(self.height):
            for j in range(self.width):
                arr[i,j] = Color.palette(color)

        colormap = {'1':'red',
                    '2':'orange',
                    '3':'yellow',
                    '4':'green',
                    '5':'blue',
                    '6':'indigo',
                    '7':'violet',
                    '8':'black',
                    '9':'white'}

        colormap_inv = {}
        for key, value in colormap.items():
            colormap_inv[value] = key
    #
# def callback(event):
#     # Get rectangle diameters
#     col_width = c.winfo_width()/self.width
#     row_height = c.winfo_height()/self.height
#     # Calculate column and row number
#     col = int(event.x//col_width)
#     row = int(event.y//row_height)
#     # If the tile is not filled, create a rectangle
#     tiles[col][row] = c.create_rectangle(col*col_width, row*row_height, (col+1)*col_width, (row+1)*row_height, fill=color, outline = color)
#     arr[row][col] = Color.palette(color)
#
# def select_color(event):
#     if event.char in colormap.keys():
#         globals()['color'] = colormap[event.char]
#
#     # Create the window, a canvas and the mouse click event binding
#     root = tk.Tk()
#     c = tk.Canvas(root, width=800, height=480, borderwidth=5, background=color)
#     c.pack()
#     c.focus_set()
#     c.bind("<B1-Motion>", callback)
#     c.bind("<Button-1>", callback)
#     c.bind("<KeyPress>", select_color)
#
#     root.mainloop()
#
#     for i in arr:
#         for j in i:
#             print(j.sample, end = '')
#         print()
