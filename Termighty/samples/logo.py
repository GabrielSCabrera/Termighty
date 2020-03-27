from ..obj import Term, Grid, Pixel, Color, Style
import numpy as np
import time

def color_b_gradients():
    '''
        PURPOSE
        Creates a color gradient
    '''

    colors_w = np.linspace(0, 255, 80).astype(np.uint8)
    colors_h = np.linspace(0, 255, 24).astype(np.uint8)
    colors_up = np.arange(0, 256, 20, dtype = np.uint8)
    colors_down = np.arange(255, 0, -20, dtype = np.uint8)
    colors_3 = np.concatenate([colors_up, colors_down])
    color_grid = np.meshgrid(colors_w, colors_h)
    out = ''
    colors_b = []
    idx = 1
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
    return colors_b

def logo():
    '''
        PURPOSE
        Creates a 'Term' instance that displays the animated Termighty logo
    '''
    term = Term((24,80))

    chars = []
    chars.append("                                                             ")
    chars.append("                                                             ")
    chars.append("    ┏━┓                       ┏━┓      ┏━┓    ┏━┓            ")
    chars.append("    ┃ ┃                       ┗━┛      ┃ ┃    ┃ ┃            ")
    chars.append("    ┃ ┗━┓┏━━━┓┏━━━┓┏━━━━━━━━━┓┏━┓┏━━━━┓┃ ┗━━━┓┃ ┗━┓┏━┓┏━┓    ")
    chars.append("    ┃ ┏━┛┃ ┏ ┃┃ ┏━┛┃ ┏━┓ ┏━┓ ┃┃ ┃┃ ┏┓ ┃┃ ┏━┓ ┃┃ ┏━┛┃ ┃┃ ┃    ")
    chars.append("    ┃ ┃  ┃ ┏━┛┃ ┃  ┃ ┃ ┃ ┃ ┃ ┃┃ ┃┃ ┃┃ ┃┃ ┃ ┃ ┃┃ ┃  ┃ ┃┃ ┃    ")
    chars.append("    ┃ ┗━┓┃ ┗━┓┃ ┃  ┃ ┃ ┃ ┃ ┃ ┃┃ ┃┃ ┗┛ ┃┃ ┃ ┃ ┃┃ ┗━┓┃ ┗┛ ┃    ")
    chars.append("    ┗━━━┛┗━━━┛┗━┛  ┗━┛ ┗━┛ ┗━┛┗━┛┗━━┓ ┃┗━┛ ┗━┛┗━━━┛┗━━┓ ┃    ")
    chars.append("    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┓┏━━┛ ┃┏━━━━━━━━━━━━━━┛ ┃    ")
    chars.append("    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━┛┗━━━━┛┗━━━━━━━━━━━━━━━━┛    ")
    chars.append("                                                             ")
    chars.append("                 GUI AND TERMINAL INTERFACE                  ")
    chars.append("                   Gabriel S Cabrera 2020                    ")
    chars.append("                                                             ")

    chars_1 = []
    chars_1.append("                                                             ")
    chars_1.append("                                                             ")
    chars_1.append("    ┍━┑                       ┍━┑      ┍━┑    ┍━┑            ")
    chars_1.append("    │ │                       ┕━┙      │ │    │ │            ")
    chars_1.append("    │ ┕━┑┍━━━┑┍━━━┑┍━━━━━━━━━┑┍━┑┍━━━━┑│ ┕━━━┑│ ┕━┑┍━┑┍━┑    ")
    chars_1.append("    │ ┍━┙│ ┍ ││ ┍━┙│ ┍━┑ ┍━┑ ││ ││ ┍┑ ││ ┍━┑ ││ ┍━┙│ ││ │    ")
    chars_1.append("    │ │  │ ┍━┙│ │  │ │ │ │ │ ││ ││ ││ ││ │ │ ││ │  │ ││ │    ")
    chars_1.append("    │ ┕━┑│ ┕━┑│ │  │ │ │ │ │ ││ ││ ┕┙ ││ │ │ ││ ┕━┑│ ┕┙ │    ")
    chars_1.append("    ┕━━━┙┕━━━┙┕━┙  ┕━┙ ┕━┙ ┕━┙┕━┙┕━━┑ │┕━┙ ┕━┙┕━━━┙┕━━┑ │    ")
    chars_1.append("    ┍━━━━━━━━━━━━━━━━━━━━━━━━━━━┑┍━━┙ │┍━━━━━━━━━━━━━━┙ │    ")
    chars_1.append("    ┕━━━━━━━━━━━━━━━━━━━━━━━━━━━┙┕━━━━┙┕━━━━━━━━━━━━━━━━┙    ")
    chars_1.append("                                                             ")
    chars_1.append("                 GUI AND TERMINAL INTERFACE                  ")
    chars_1.append("                   Gabriel S Cabrera 2020                    ")
    chars_1.append("                                                             ")

    chars_2 = []
    chars_2.append("                                                             ")
    chars_2.append("                                                             ")
    chars_2.append("    ┎─┒                       ┎─┒      ┎─┒    ┎─┒            ")
    chars_2.append("    ┃ ┃                       ┖─┚      ┃ ┃    ┃ ┃            ")
    chars_2.append("    ┃ ┖─┒┎───┒┎───┒┎─────────┒┎─┒┎────┒┃ ┖───┒┃ ┖─┒┎─┒┎─┒    ")
    chars_2.append("    ┃ ┎─┚┃ ┎ ┃┃ ┎─┚┃ ┎─┒ ┎─┒ ┃┃ ┃┃ ┎┒ ┃┃ ┎─┒ ┃┃ ┎─┚┃ ┃┃ ┃    ")
    chars_2.append("    ┃ ┃  ┃ ┎─┚┃ ┃  ┃ ┃ ┃ ┃ ┃ ┃┃ ┃┃ ┃┃ ┃┃ ┃ ┃ ┃┃ ┃  ┃ ┃┃ ┃    ")
    chars_2.append("    ┃ ┖─┒┃ ┖─┒┃ ┃  ┃ ┃ ┃ ┃ ┃ ┃┃ ┃┃ ┖┚ ┃┃ ┃ ┃ ┃┃ ┖─┒┃ ┖┚ ┃    ")
    chars_2.append("    ┖───┚┖───┚┖─┚  ┖─┚ ┖─┚ ┖─┚┖─┚┖──┒ ┃┖─┚ ┖─┚┖───┚┖──┒ ┃    ")
    chars_2.append("    ┎───────────────────────────┒┎──┚ ┃┎──────────────┚ ┃    ")
    chars_2.append("    ┖───────────────────────────┚┖────┚┖────────────────┚    ")
    chars_2.append("                                                             ")
    chars_2.append("                 GUI AND TERMINAL INTERFACE                  ")
    chars_2.append("                   Gabriel S Cabrera 2020                    ")
    chars_2.append("                                                             ")

    colors_b = color_b_gradients()
    char_arrs = [chars, chars_1, chars_2]
    for colors in colors_b:
        for i in range(len(chars)):
            for j in range(len(chars[0])):
                char_arr = char_arrs[np.random.choice(3)]
                term[i,j] = Pixel(color_b = Color(colors[i][j]), char = char_arr[i][j])
        time.sleep(0.01)
        print("\033[1;1H")
        print(term)


    for k in range(50):
        for i in range(len(chars)):
            for j in range(len(chars[0])):
                char_arr = char_arrs[np.random.choice(3)]
                term[i,j] = Pixel(char = char_arr[i][j])

        print("\033[1;1H")
        print(term)


        print("\033[1;1H")
        print(term)
