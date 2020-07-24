from pathlib import Path
import os

# Default terminal width
term_width = 80
# Default terminal height
term_height = 24

# Terminal Text Color
color_t = 'white'
# Terminal Background Color
color_b = 'black'

# Terminal ANSI escape sequence template
# <str> instance method 'format' should be used on this sequence
escape_sequence = '\033[{}m'

# Setting up filesystem access
home = Path.home()

# Default Termighty directory
save_path = home / 'Documents' / 'Termighty'

# Default saving directories
save_dirs = {
             # Key          Directory
             'grid'     :   'grids',
             'series'   :   'series'
            }

save_dirs = {i:save_path / j for i,j in save_dirs.items()}

# Logo save path
logo_file = 'logo.npy'
logo_path = save_dirs['series'] / logo_file

# Creating non-existent directories
if not os.path.isdir(save_path):
    os.mkdir(save_path)

for save_dir in save_dirs.values():
    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)
