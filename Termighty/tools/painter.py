import tkinter as tk
import numpy as np
from ..obj import Color

# Set number of rows and columns
ROWS = 24
COLS = 80

# Create a grid of None to store the references to the tiles
tiles = [[None for _ in range(ROWS)] for _ in range(COLS)]
arr = np.empty((ROWS, COLS), dtype = Color)

color = 'black'

for i in range(ROWS):
    for j in range(COLS):
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

def callback(event):
    # Get rectangle diameters
    col_width = c.winfo_width()/COLS
    row_height = c.winfo_height()/ROWS
    # Calculate column and row number
    col = int(event.x//col_width)
    row = int(event.y//row_height)
    # If the tile is not filled, create a rectangle
    tiles[col][row] = c.create_rectangle(col*col_width, row*row_height, (col+1)*col_width, (row+1)*row_height, fill=color, outline = color)
    arr[row][col] = Color.palette(color)

def select_color(event):
    if event.char in colormap.keys():
        globals()['color'] = colormap[event.char]

# Create the window, a canvas and the mouse click event binding
root = tk.Tk()
c = tk.Canvas(root, width=800, height=480, borderwidth=5, background=color)
c.pack()
c.focus_set()
c.bind("<B1-Motion>", callback)
c.bind("<Button-1>", callback)
c.bind("<KeyPress>", select_color)

root.mainloop()

for i in arr:
    for j in i:
        print(j.sample, end = '')
    print()
