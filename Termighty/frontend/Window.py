from ..data import int_types, arr_types
from ..backend.Grid import Grid
from ..config import defaults
from ..utils import checkers
from .Term import Term

class Window(Term):

    def __init__(self, shape, pos):
        '''
            PURPOSE
            Displays and manages instances of class 'Grid' – can be displayed
            as subdivisions of 'Term' live sessions.

            NOTE
            Parameter 'shape' represents the (H,W) of the 'Window' instance,
            while 'pos' represents its position

            PARAMETERS
            shape       <tuple> with two postive <int> elements
            pos         <tuple> with two postive <int> elements
        '''
        checkers.check_type(shape, arr_types, 'shape', '__init__')
        checkers.check_type_arr(shape, int_types, 'shape', '__init__')
        checkers.check_range_arr(shape, 1, None, 'shape', '__init__')
        checkers.check_shape_arr(shape, (2,), 'shape', '__init__')

        checkers.check_type(pos, arr_types, 'pos', '__init__')
        checkers.check_type_arr(pos, int_types, 'pos', '__init__')
        checkers.check_range_arr(pos, 0, None, 'pos', '__init__')
        checkers.check_shape_arr(pos, (2,), 'pos', '__init__')

        self.data = Grid.empty(shape)
        self.shape_arr = self.data.shape
        self.pos_arr = tuple(pos)
        self.height_val = self.shape_arr[0]
        self.width_val = self.shape_arr[1]
        self.live_bool = False

    '''INSTANTIATORS'''

    @classmethod
    def from_grid(cls, grid, pos):
        '''
            PURPOSE
            Initializes an instance of 'Window' from a 'Grid' instance

            PARAMETERS
            grid        Instance of class 'Grid'
            pos         <tuple> with two positive <int> elements

            RETURNS
            Instance of class 'Window'
        '''
        checkers.check_type(grid, Grid, 'grid', 'from_grid')
        window = cls(grid.shape, pos)
        window.data[:,:] = grid
        return window

    '''SETTERS'''

    def __setitem__(self, idx, value):
        '''
            PURPOSE
            Replaces an element or sub-grid of the current instance

            PARAMETERS
            idx             Length 1 or 2 <tuple> containing <int> or <slice>
            value           Instance of 'Pixel' or 'Grid'
        '''
        try:
            if isinstance(value, Grid):
                self.grid.__setitem__(idx, value.data)
            else:
                self.grid.__setitem__(idx, value)
        except IndexError:
            msg = f'Attempt to access Pixel or sub-Grid at invalid index {idx}'
            raise IndexError(msg)

        self.update()

    def cursor_to(self, idx):
        '''
            PURPOSE
            Returns a string that moves the cursor the the given relative
            coordinates 'idx' when printed

            PARAMETERS
            idx         <tuple> of two non-negative <int> values

            RETURNS
            <str>
        '''
        sys.stdout.write(f"\033[{idx[0] + self.pos[0]};{idx[1] + self.pos[1]}H")

    '''GETTERS'''

    def __getitem__(self, idx):
        '''
            PURPOSE
            Retrieve an element or sub-grid of the current 'Window' instance

            PARAMETERS
            idx             Length 1 or 2 <tuple> containing <int> or <slice>

            RETURNS
            Instance of 'Pixel' or 'Grid'
        '''

        subdata = self.grid.__getitem__(idx)
        return subdata

    def __str__(self):
        '''
            PURPOSE
            Returns a printable string that contains the 'Window' data

            RETURNS
            out         <str>
        '''
        out = ''
        for row in self.grid.data:
            for pixel in row:
                out += pixel.__str__()
            out += '\n'
        return out[:-1]

    def __repr__(self):
        '''
            PURPOSE
            Returns a machine-readable <str> with instance information

            RETURNS
            <str>
        '''
        out = (f'Window(h={self.height}, w={self.width}, x={self.pos_arr[1]}, '
               f'y={self.pos_arr[0]})')
        return out

    '''ACCESSORS'''

    @property
    def grid(self):
        '''
            PURPOSE
            Returns the 'Grid' data of the current 'Window' instance

            RETURNS
            Instance of 'Grid'
        '''
        return self.data

    @property
    def shape(self):
        '''
            PURPOSE
            Returns the shape of the current 'Window' instance

            RETURNS
            shape       <tuple> of length 2 with <int> values
        '''
        return self.shape_arr

    @property
    def pos(self):
        '''
            PURPOSE
            Returns the absolute position of the current 'Window' instance's
            uppermost left corner in terms of the grid in 'Term'.

            RETURNS
            <tuple> of length 2 with <int> values
        '''
        return self.pos_arr

    @property
    def size(self):
        '''
            PURPOSE
            Returns the size of the current 'Window' instance

            RETURNS
            <int>
        '''
        return self.data.size

    @property
    def height(self):
        '''
            PURPOSE
            Returns the shape of the current 'Window' instance

            RETURNS
            <int>
        '''
        return self.height_val

    @property
    def width(self):
        '''
            PURPOSE
            Returns the shape of the current 'Window' instance

            RETURNS
            <int>
        '''
        return self.width_val

    '''MANAGERS'''

    def update(self):
        '''
            PURPOSE
            Updates the console if current 'Window' instance is live
        '''
        if self.live_bool:
            for i in range(0, self.height):
                self.cursor_to((pos[0] + i, pos[1]))
                for j in range(0, self.width):
                    sys.stdout.write(self.data[i,j].__str__())
            sys.stdout.flush()

    @classmethod
    def clear(cls):
        '''
            PURPOSE
            Clears the window
        '''
        for m, row in enumerate(self.data):
            for n, col in enumerate(row):
                self.data[m,n].color_t.set_RGB(defaults.color_t)
                self.data[m,n].color_b.set_RGB(defaults.color_b)
                self.data[m,n].char = ' '
                self.data[m,n].update()

        self.update()

    def open():
        '''
            PURPOSE
            Makes the 'Window' instance live, meaning it will be displayed
        '''
        self.live_bool = True
        self.update()

    def close():
        '''
            PURPOSE
            Kills the 'Window' instance's live session
        '''
        self.clear()
        self.live_bool = False

    '''REMOVED'''

    def __enter__(self):
        msg = 'Context manager unavailable for class \'Window\''
        raise NotImplementedError(msg)

    def __exit__(self):
        msg = 'Context manager unavailable for class \'Window\''
        raise NotImplementedError(msg)
