from ..obj import Term, Grid, Pixel, Color, Style
import numpy as np
import time
import sys

ROWS, COLS = 24, 80

def color_b_gradients():
    '''
        PURPOSE
        Creates a color gradient
    '''

    colors_w = np.linspace(0, 255, COLS).astype(np.uint8)
    colors_h = np.linspace(0, 255, ROWS).astype(np.uint8)
    colors_up = np.arange(0, 256, 20, dtype = np.uint8)
    colors_down = np.arange(255, 0, -20, dtype = np.uint8)
    colors_3 = np.concatenate([colors_up, colors_down])
    color_grid = np.meshgrid(colors_w, colors_h)
    out = ''
    colors_b = []
    idx = np.random.choice(3)
    start = []

    colors_b.append([])
    for m,n in zip(*color_grid):
        colors_b[-1].append([])
        for i,j in zip(m,n):
            RGB = [0,0,0]
            RGB[idx] = 0
            RGB[(idx+1)%3] = j
            RGB[(idx+2)%3] = i
            colors_b[-1][-1].append(tuple(RGB))

    while colors_b[-1][-1][-1][0] > 0 or colors_b[-1][-1][-1][1] > 0 or colors_b[-1][-1][-1][2] > 0:
        new = []
        for i in colors_b[-1]:
            new.append([])
            for j in i:
                RGB = [0,0,0]
                RGB[0] = 0
                RGB[1] = max(0, j[1]-1)
                RGB[2] = max(0, j[2]-1)
                new[-1].append(tuple(RGB))
        colors_b.append(new)

    colors_b = colors_b[1::-1]

    for val in colors_3:
        colors_b.append([])
        for m,n in zip(*color_grid):
            colors_b[-1].append([])
            for i,j in zip(m,n):
                RGB = [0,0,0]
                RGB[idx] = val
                RGB[(idx+1)%3] = j
                RGB[(idx+2)%3] = i
                colors_b[-1][-1].append(tuple(RGB))

    while colors_b[-1][-1][-1][0] > 0 or colors_b[-1][-1][-1][1] > 0 or colors_b[-1][-1][-1][2] > 0:
        new = []
        for i in colors_b[-1]:
            new.append([])
            for j in i:
                RGB = [0,0,0]
                RGB[0] = max(0, j[0]-10)
                RGB[1] = max(0, j[1]-10)
                RGB[2] = max(0, j[2]-10)
                new[-1].append(tuple(RGB))
        colors_b.append(new)
    return np.array(colors_b).astype(np.uint8)

def get_grids():
    '''
        PURPOSE
        Returns the set of 'Grid' instances to be displayed

        RETURNS
        <list> with instances of 'Grid'
    '''

    chars = []
    chars.append("                                                                                ")
    chars.append("                                                                                ")
    chars.append("                                                                                ")
    chars.append("                                                                                ")
    chars.append("                                                                                ")
    chars.append("                                                                                ")
    chars.append("                                                                                ")
    chars.append("             ┏━┓                       ┏━┓      ┏━┓    ┏━┓                      ")
    chars.append("             ┃ ┃                       ┗━┛      ┃ ┃    ┃ ┃                      ")
    chars.append("             ┃ ┗━┓┏━━━┓┏━━━┓┏━━━━━━━━━┓┏━┓┏━━━━┓┃ ┗━━━┓┃ ┗━┓┏━┓┏━┓              ")
    chars.append("             ┃ ┏━┛┃ ┏ ┃┃ ┏━┛┃ ┏━┓ ┏━┓ ┃┃ ┃┃ ┏┓ ┃┃ ┏━┓ ┃┃ ┏━┛┃ ┃┃ ┃              ")
    chars.append("             ┃ ┃  ┃ ┏━┛┃ ┃  ┃ ┃ ┃ ┃ ┃ ┃┃ ┃┃ ┃┃ ┃┃ ┃ ┃ ┃┃ ┃  ┃ ┃┃ ┃              ")
    chars.append("             ┃ ┗━┓┃ ┗━┓┃ ┃  ┃ ┃ ┃ ┃ ┃ ┃┃ ┃┃ ┗┛ ┃┃ ┃ ┃ ┃┃ ┗━┓┃ ┗┛ ┃              ")
    chars.append("             ┗━━━┛┗━━━┛┗━┛  ┗━┛ ┗━┛ ┗━┛┗━┛┗━━┓ ┃┗━┛ ┗━┛┗━━━┛┗━━┓ ┃              ")
    chars.append("             ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┓┏━━┛ ┃┏━━━━━━━━━━━━━━┛ ┃              ")
    chars.append("             ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━┛┗━━━━┛┗━━━━━━━━━━━━━━━━┛              ")
    chars.append("                                                                                ")
    chars.append("                          GUI AND TERMINAL INTERFACE                            ")
    chars.append("                            Gabriel S Cabrera 2020                              ")
    chars.append("                                                                                ")
    chars.append("                                                                                ")
    chars.append("                                                                                ")
    chars.append("                                                                                ")
    chars.append("                                                                                ")

    chars_1 = []
    chars_1.append("                                                                                ")
    chars_1.append("                                                                                ")
    chars_1.append("                                                                                ")
    chars_1.append("                                                                                ")
    chars_1.append("                                                                                ")
    chars_1.append("                                                                                ")
    chars_1.append("                                                                                ")
    chars_1.append("             ┍━┑                       ┍━┑      ┍━┑    ┍━┑                      ")
    chars_1.append("             │ │                       ┕━┙      │ │    │ │                      ")
    chars_1.append("             │ ┕━┑┍━━━┑┍━━━┑┍━━━━━━━━━┑┍━┑┍━━━━┑│ ┕━━━┑│ ┕━┑┍━┑┍━┑              ")
    chars_1.append("             │ ┍━┙│ ┍ ││ ┍━┙│ ┍━┑ ┍━┑ ││ ││ ┍┑ ││ ┍━┑ ││ ┍━┙│ ││ │              ")
    chars_1.append("             │ │  │ ┍━┙│ │  │ │ │ │ │ ││ ││ ││ ││ │ │ ││ │  │ ││ │              ")
    chars_1.append("             │ ┕━┑│ ┕━┑│ │  │ │ │ │ │ ││ ││ ┕┙ ││ │ │ ││ ┕━┑│ ┕┙ │              ")
    chars_1.append("             ┕━━━┙┕━━━┙┕━┙  ┕━┙ ┕━┙ ┕━┙┕━┙┕━━┑ │┕━┙ ┕━┙┕━━━┙┕━━┑ │              ")
    chars_1.append("             ┍━━━━━━━━━━━━━━━━━━━━━━━━━━━┑┍━━┙ │┍━━━━━━━━━━━━━━┙ │              ")
    chars_1.append("             ┕━━━━━━━━━━━━━━━━━━━━━━━━━━━┙┕━━━━┙┕━━━━━━━━━━━━━━━━┙              ")
    chars_1.append("                                                                                ")
    chars_1.append("                          GUI AND TERMINAL INTERFACE                            ")
    chars_1.append("                            Gabriel S Cabrera 2020                              ")
    chars_1.append("                                                                                ")
    chars_1.append("                                                                                ")
    chars_1.append("                                                                                ")
    chars_1.append("                                                                                ")
    chars_1.append("                                                                                ")

    chars_2 = []
    chars_2.append("                                                                                ")
    chars_2.append("                                                                                ")
    chars_2.append("                                                                                ")
    chars_2.append("                                                                                ")
    chars_2.append("                                                                                ")
    chars_2.append("                                                                                ")
    chars_2.append("                                                                                ")
    chars_2.append("             ┎─┒                       ┎─┒      ┎─┒    ┎─┒                      ")
    chars_2.append("             ┃ ┃                       ┖─┚      ┃ ┃    ┃ ┃                      ")
    chars_2.append("             ┃ ┖─┒┎───┒┎───┒┎─────────┒┎─┒┎────┒┃ ┖───┒┃ ┖─┒┎─┒┎─┒              ")
    chars_2.append("             ┃ ┎─┚┃ ┎ ┃┃ ┎─┚┃ ┎─┒ ┎─┒ ┃┃ ┃┃ ┎┒ ┃┃ ┎─┒ ┃┃ ┎─┚┃ ┃┃ ┃              ")
    chars_2.append("             ┃ ┃  ┃ ┎─┚┃ ┃  ┃ ┃ ┃ ┃ ┃ ┃┃ ┃┃ ┃┃ ┃┃ ┃ ┃ ┃┃ ┃  ┃ ┃┃ ┃              ")
    chars_2.append("             ┃ ┖─┒┃ ┖─┒┃ ┃  ┃ ┃ ┃ ┃ ┃ ┃┃ ┃┃ ┖┚ ┃┃ ┃ ┃ ┃┃ ┖─┒┃ ┖┚ ┃              ")
    chars_2.append("             ┖───┚┖───┚┖─┚  ┖─┚ ┖─┚ ┖─┚┖─┚┖──┒ ┃┖─┚ ┖─┚┖───┚┖──┒ ┃              ")
    chars_2.append("             ┎───────────────────────────┒┎──┚ ┃┎──────────────┚ ┃              ")
    chars_2.append("             ┖───────────────────────────┚┖────┚┖────────────────┚              ")
    chars_2.append("                                                                                ")
    chars_2.append("                          GUI AND TERMINAL INTERFACE                            ")
    chars_2.append("                            Gabriel S Cabrera 2020                              ")
    chars_2.append("                                                                                ")
    chars_2.append("                                                                                ")
    chars_2.append("                                                                                ")
    chars_2.append("                                                                                ")
    chars_2.append("                                                                                ")

    extra_frames = 0
    colors_b = color_b_gradients()
    grids = []
    char_arrs = [chars, chars, chars, chars_1, chars_2]
    idx = np.random.choice(len(char_arrs), ROWS*COLS*(len(colors_b)+extra_frames))
    n = 0
    for colors in colors_b:
        grid = Grid.empty((ROWS, COLS))
        for i in range(ROWS):
            for j in range(COLS):
                grid[i,j].color_b.set_RGB(colors[i][j])
                grid[i,j].set_char(char_arrs[idx[n]][i][j])
                n += 1
        grids.append(grid)
    for k in range(extra_frames):
        grid = Grid.empty((ROWS, COLS))
        for i in range(ROWS):
            for j in range(COLS):
                grid[i,j].set_char(char = char_arrs[idx[n]][i][j])
                n += 1
        grids.append(grid)

    grid = Grid.empty((ROWS, COLS))
    for i in range(ROWS):
        for j in range(COLS):
            grid[i,j].set_char(char = chars[i][j])
    grids.append(grid)

    return grids

def logo():
    '''
        PURPOSE
        Creates a 'Term' instance that displays the animated Termighty logo
    '''
    term = Term((ROWS, COLS))

    t_sleep = 0.1

    print('DEBUG Making Logo')
    t0 = time.time()
    grids = get_grids()
    t1 = time.time()
    print(f'\n\nDEBUG Logo Done – {float(t1-t0):.1f}s')
    sys.stdout.flush()
    time.sleep(2)

    for grid in grids:
        time.sleep(t_sleep)
        print("\033[1;1H")
        print(grid)
