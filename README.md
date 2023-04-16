# Termighty

High-level utilities for cross-platform terminal interaction.

# Class Documentation: System

The `System` class is used to keep track of the terminal dimensions and detect the current OS. It also contains the `kill_all` class attribute, which is by default set to `False`. If it is set to `True`, all active Termighty threads will be killed.

## Attributes

### terminal_size: tuple[int, int]
Stores the terminal dimensions (width and height) as a tuple.

### os
Stores the name of the current operating system.

### escape_code_encoding
Stores the encoding type of escape codes, based on the operating system.

### kill_all
A boolean attribute that, if set to `True`, stops all processes.

## Methods

### track_terminal_shape(cls)

A class method that tracks the terminal size in a loop, updating the `terminal_size` attribute whenever the terminal dimensions change. The loop will run until `kill_all` is set to `True`. The method has a sleep time of `0.05` seconds to prevent excessive CPU usage.

## Threading
### track_terminal_shape_thread

A daemon thread created to run the `track_terminal_shape` method in the background. The thread will start automatically when the module is imported.

# Class Documentation: Term

The `Term` class is a collection of commands that can be used to make modifications to the terminal state. It allows for the existence of multiple buffers that each can be flushed and appended independently of others. By default, methods that write to the terminal are not set to flush the buffer when called, which improves performance. However, if the flush parameter is set to True, then the buffer is bypassed and the command outputs immediately to the terminal.

## Methods

### __init__(self, flush: bool = False) -> None
The constructor method initializes the instance variables needed for the class.

### bell(self, flush: bool = False) -> None
Play the terminal bell sound.

### clear(self, flush: bool = False) -> None
Clears the terminal screen.

### cursor_hide(self, flush: bool = False) -> None
Make the cursor invisible.

### cursor_load(self, flush: bool = False) -> None
Load the cursor position.

### cursor_move(self, line: int, column: int, flush: bool = False) -> None
Move the cursor to the given line and column.

### cursor_save(self, flush: bool = False) -> None
Save the cursor position.

### cursor_show(self, flush: bool = False) -> None
Make the cursor visible.

### flush(self) -> None
Flush the entire buffer to the terminal.

### flush_string(self, string: str) -> None
Write and flush the given string to the terminal.

### write(self, line: int, column: int, string: str, flush: bool = False) -> None
Write the given string starting at the designated line and column coordinates to the buffer.

# Class Documentation: String

The String class is a more advanced version of the built-in `str` class, which can handle ANSI Escape Sequences indirectly through calling various methods. These methods allow for custom text and background colors, as well as text styles. Most methods for `str` class function, such as `string.partition()`, `string.strip()`, etc.

## Class Methods

### list_styles() -> str

Return a list of all available styles (as viewable ANSI escape sequences) and their names. Remember to print the outputted string if you want to view the list in the terminal.

## Constructor

### __init__(string: str, foreground: Optional[Union[str, Color, tuple[int, int, int]]] = None, background: Optional[Union[str, Color, tuple[int, int, int]]] = None, style: Optional[str] = None) -> None

Create an instance of class String. Arguments foreground and background should be the names of known colors, or instances of Color. Argument style should be the name of a known style in /data/styles.json.

## Magic Methods

Several magic methods are implemented for the String class, allowing it to be used in a similar way to a built-in string. Magic methods include: `__add__`, `__format__`, `__getitem__`, `__iter__`, `__mul__`, `__next__`, `__radd__`, `__repr__`, `__rmul__`, `__set__`, and `__str__`.

## Properties

### background -> Color
Return a copy of the Color instance assigned to the current background.

### foreground -> Color
Return a copy of the Color instance assigned to the current foreground.

### string -> str
Return the uncolored and unformatted text currently assigned to this `String` instance.

### style -> str
Return the name of the text style associated with the current instance.

## Setter Methods

### background.setter(color: Optional[Union[str, Color, tuple[int, int, int]]] = None) -> None
Set the background color to a new value. Accepts the name of a color as a string, or an instance of `Color`, or a tuple containing three integers in the range [0, 255] representing RGB color channels.

### foreground.setter(color: Optional[Union[str, Color, tuple[int, int, int]]] = None) -> None
Set the foreground color to a new value. Accepts the name of a color as a string, or an instance of `Color`, or a tuple containing three integers in the range [0, 255] representing RGB color channels.

### string.setter(data: str) -> None
Overwrite the uncolored and unformatted text currently assigned to this `String` instance.

### style.setter(style: Optional[str] = None) -> None
Set the style to a new value.

# Class: Color

The Color class manages colors in RGB format for use in instances of the `String` class, or for modifying terminal background and foreground colors directly. It supports many operations between colors, as well as unary operations like adding and subtracting colors (by RGB value) or taking a color's negative.

Colors can be instantiated directly by inputting an RGB value (and optional color name), or they may be generated from a comprehensive catalog of colors using the classmethod `Color.palette` (the full catalog can be printed as a guide by executing the class method `Color.list_colors`).

## Class Methods:

### chart(r: Optional[int], g: Optional[int], b: Optional[int], term_width: int) -> str
Returns a terminal-printable color chart. Set exactly ONE of the parameters `r`, `g`, and `b` to a value in the range [0, 255], and the others must be set to None as they will be iterated over. Argument `term_width` should be a positive nonzero integer.

### is_color(name: str) -> bool
Returns True if `/data/rgb.json` contains the given string. Can be used to check whether or not a color you want to instantiate is included in Termighty.

### list_colors(sort_by="step") -> str
Returns a string containing a list of all available colors (as viewable ANSI escape sequences) and their names. Remember to print the outputted string if you want to view the list in the terminal.

### palette(name: str) -> "Color"
Initializes a `Color` instance using a color name; only succeeds if the name is found in `/data/rgb.json`.

## Properties:

### sample -> str
Returns a color sample in the form of a printable string, consisting of a single whitespace character with the background color set to that of the current instance of class Color.

## Constructor:

### init(self, rgb: Sequence[int], name: str = "Unnamed Color") -> None
Initializes a new instance of the `Color` class. Argument `rgb` should be a sequence containing three integers in the range [0, 255].

## Magic Methods:

### add(self, color: "Color") -> "Color"
Adds colors together by summing their RGB values.

### call(self, string: str) -> str
Returns the given string, but with the text colored using the current instance's RGB values.

### hash(self) -> int
Returns a unique hash for the combination of `rgb` values of the current Color instance.

### repr(self) -> str
Returns a color sample from the current instance that is machine-readable.

### str(self) -> str
Returns the current instance's color name, RGB value, and a sample of the color as a formatted human-readable multiline string.

### sub(self, color: "Color") -> "Color"
Subtracts colors from each other by subtracting their RGB values.

## Properties (Getters/Setters):

### b -> int
Returns the current instance's blue RGB value.

### g -> int
Returns the current instance's green RGB value.

### name -> str
Returns the current instance's color name.

### r -> int
Returns the current instance's red RGB value.

### rgb -> tuple[int, int, int]
Returns the current instance's RGB values as a tuple of integers.

## Public Methods:

### brightness(self) -> int
Returns the mean of the RGB values, which can be considered a measure of the color's brightness.

### copy(self) -> "Color"
Returns a deep copy of the current instance.

### hsv(self) -> tuple[float, float, float]
Return the color of the current instance in HSV form, which converts the red, green, and blue color channels to their equivalent hue, saturation, and brightness.  HSV is a representation of color that attempts to more closely represent the way that human vision interprets color.

### lightness(self, weighted: bool = True) -> float
Return the norm of the RGB vector as fraction of 255.  Should return a float in the range 0 to 1.
If weighted, multiply the squares of the `R`, `G`, and `B` color channels by 0.299, 0.587, and 0.114, respectively.
Source of weights: http://alienryderflex.com/hsp.html

### negative(self) -> "Color"
Return the color negative of the current instance, which is the element-wise difference (255-R, 255-G, 255-B), where `R`, `G`, and `B` are the current instance's color channels.

# Class: GetchIterator

The `GetchIterator` class is designed to be used in a for-loop to iterate over the `Listener`'s history, starting at the provided index, and continuously yielding all new additions to the history until the `Listener` is stopped.

## Methods

### __init__(self, idx: Optional[int] = None)
Initializes the GetchIterator object, preparing the indices for the iteration if they are given.

### __iter__(self)
Sets the start index for the iterator based on the current length of the Listener history if the index is not provided. Otherwise, it uses the given index.

### __next__(self)
Returns the next input detected by the Listener and appended to its history.

# Class: Listener

The `Listener` class is a superclass that allows users to display live, dynamic text on the terminal while simultaneously accepting user inputs. It must be inherited before instantiation, and the `_writer` attribute must be overwritten. The overwritten `_writer` should contain the main loop displayed to the terminal.

Only one instance of `Listener` may be active at once.

## Class Attributes

### _active
A boolean indicating whether the `Listener` is active.

### _escape_hits
The number of consecutive Esc key presses needed to stop the `Listener`.

### _history
A list of the user's input history.

### _raw
A boolean indicating whether the `Listener` should return raw escape codes or interpret them.

### _sleep_time
The time in seconds the `Listener` should sleep between input checks.

## Class Methods

### _getch_linux()
Listens for keyboard input on Linux systems and returns a string with a key name.

### _getch_windows()
Listens for keyboard input on Windows systems and returns a string with a key name.

### _interpret_escape_code(escape_code: bytes) -> str
Returns a character or command from the given escape code.

### _listener()
A method for updating the global `input_state` variable by appending the latest keypress to it (interpreted by `data/keymaps`).

Expects `_raw_mode` to be True, implying the terminal will read user inputs immediately without echoing to the
terminal.

To kill all running threads, hold key `ESC` for a few seconds, or hit it as many times in a row as the value
given in `cls._escape_hits` -- be sure not to press any other keys in between or the kill process is interrupted.

### _listener_raw()
A method for updating the global `input_state` variable by appending the latest keypress to it (as an ANSI escape sequence or character).

### _raw_mode_linux(state: bool)
Sets the terminal to raw mode on Linux systems if state is True, or to echo mode if state is False.

### _raw_mode_windows(state: bool)
Windows placeholder for raw mode, which is only necessary on Linux systems.

## Public Methods

### getch_iterator(cls, idx: Optional[int] = None, keytest: bool = False) -> GetchIterator
Returns a `GetchIterator` object for the given index.

### start(cls, raw: bool = False)
Activates the `Listener` session. If raw is True, the listener will return raw escape codes instead of interpreting them.

### stop(cls)
Deactivates the `Listener` session.

## OS-Specific Methods

### _getch
Alias for `_getch_linux` on Linux systems, and `_getch_windows` on Windows systems.

### _raw_mode
Alias for `_raw_mode_linux` on Linux systems, and `_raw_mode_windows` on Windows systems.

### _fd
File descriptor for the terminal input on Linux systems.

### _old_settings
The terminal's old settings on Linux systems.

# Class: TextBox

The `TextBox` class provides a base for rectangular shapes (that may or may not contain text) that display on the terminal. It is used to simplify and standardize more complex objects.
Magic Methods

## Constructor

### __init__(self, row_start: int, col_start: int, row_end: int, col_end: int, wrap_text: bool = False, wrap_subsequent_indent: str = "", wrap_text_break_on_hyphens: bool = True, wrap_text_break_long_words: bool = True, background: Optional[Union[str, Color]] = None, foreground: Optional[Union[str, Color]] = None, style: Optional[str] = None, alignment: Literal["left", "right", "center"] = "left", view: tuple[int, int] = (0, 0),) -> None
Return a new instance of class `TextBox` at the specified coordinates.  If negative coordinates are given, they will be set dynamically relative to the size of the terminal; a thread will loop in the background keeping track of the terminal dimensions and resizing the `TextBox` if its coordinates are dynamic.

### __call__(self, text: Union[str, list[str, ...]]) -> None
This method modifies the current state of the `TextBox` by replacing its contents with the given text. It accepts a single string or a list of strings. If a list is given, each element will be placed in its own row within the `TextBox`. However, it does not support the use of strings containing ANSI escape sequences.

### _process_text(self) -> None
This method justifies the raw text given to the __call__ method such that all lines of text are equally-sized and wide enough to allow for the view of the text to be moved left, right, up, and down until the text is just out of view. It takes the `_alignment` attribute into account, aligning the text either to the left, right, or center of the `TextBox`.

### _init_color_attributes(self, background: Color, foreground: Color, style: str) -> None
This method prepares all the required instance attributes, such as colors, style, and the resulting ANSI sequences that will be used to correctly display the text with these colors and styles.

### _init_spacial_attributes(self, row_start: int, col_start: int, row_end: int, col_end: int, view: tuple[int, int]) -> None
This method initializes attributes that are related to the `TextBox` shape, position within the terminal, and the position of its contents. This includes the coordinates of the `TextBox` corners (user-defined), the initial size of the terminal, as obtained by the `System` class, and the window view, set to (0,0) by default.

### _process_text_wrapper(self) -> None
This method sets up the text wrapper.

### _init_arguments(self, background: Union[str, Color, tuple[int, int, int]], foreground: Union[str, Color, tuple[int, int, int]], style: str, defaults: tuple[Color, Color, str], argnames: tuple[str, str, str]) -> tuple[Color, Color, str]
This method performs checks making sure that the initialization arguments are correctly set up. It confirms that the `TextBox` dimensions are correctly set up (`start` < `end`), that the given background & foreground colors are valid, and that the given style is valid.

### _run_thread(self, dt: float) -> None
This method keeps updating the window every `dt` seconds and accounts for changes in the terminal size (useful when dealing with relative coordinates on initialization).

### _set_shape(self) -> None
This method sets the size of the `TextBox` to those given by the user at instantiation. If the terminal size is smaller than the `TextBox` size, it will decrease the `TextBox` size to make it fit in the terminal. It also accounts for negative size instantiation values; if a value is negative, it is subtracted from the terminal size (from the axis in question).

### _set_view(self) -> None
This method limits the view to prevent out of bounds errors by using commands min and max with the `TextBox` dimensions.

## Public Methods

### start(self, dt: float = 0.005) -> None
This method activates a thread that runs the method `_run_thread`.

### stop(self) -> None
This method kills the active thread.

### alignment(self, mode: str) -> None
This method sets the `TextBox` text alignment mode.

# TextEditor Class

`TextEditor` is a subclass of `TextBox` that emulates a fully-functional word processor. It uses class Listener to detect keyboard inputs and supports the following advanced functions:

* Cursor positioning with the arrow keys
* Ctrl-arrow key to move the cursor to the beginning/end of words
* Alt-arrow to select text
* Deletion of selected text
* Copying & pasting of selected text.

## Constructor
### __init__(self, row_start: int, col_start: int, row_end: int, col_end: int, wrap_text: bool = False, wrap_subsequent_indent: str = "", line_numbers: bool = False, background: Union[str, Color, tuple[int, int, int]] = None, foreground: Union[str, Color, tuple[int, int, int]] = None, style: Optional[str] = None, select_background: Union[str, Color, tuple[int, int, int]] = None, select_foreground: Union[str, Color, tuple[int, int, int]] = None, select_style: Optional[str] = None, line_number_background: Union[str, Color, tuple[int, int, int]] = None, line_number_foreground: Union[str, Color, tuple[int, int, int]] = None, line_number_style: Optional[str] = None, vertical_scroll_buffer: Optional[int] = None, horizontal_scroll_buffer: Optional[int] = None, cursor_position: tuple[int, int] = (0, 0), frozen: bool = False,)
The constructor in class TextEditor creates an instance of TextEditor and initializes its attributes and those of its inherited TextBox.

## Methods
### _init_editor_attributes(self, cursor_position, frozen, line_numbers, select_background, select_foreground, select_style, line_number_background, line_number_foreground, line_number_style, selected=None)
Prepare all the instance attributes for selected text, such as colors, style, and the resulting ANSI sequences that will be used to correctly display the text with these colors and styles. Also initializes the coordinate list of selected text, set to an empty list by default.

### _process_text_wrapper(self)
Prepare the TextWrapper object that wraps text when it is too long to fit on one line. If line numbers are enabled, this method also determines the maximum width required for the line numbers.

### _run_getch_thread(self) -> None
Keeps updating the window every set number of seconds (given by dt) and accounts for changes in the terminal size (useful when dealing with relative coordinates on initialization).

### _set_scroll_buffer(self) -> None
If the vertical and/or horizontal scroll buffers are dynamic, changes them based on the current terminal dimensions.

### _set_view(self) -> None
Updates the current view of the text based on the current cursor position and selected text.

### start(self)
Main loop which runs on one thread, while a listener runs on another and provides commands to be read by this method. These inputs are accessed via the superclass attribute LiveMenu._input_state and are processed in an infinite loop until broken.

### freeze(self)
Freeze the TextEditor -- the getch_iterator in method _run_getch_thread will continue to run, but it will not act on the inputs and leave the window unchanged.

### unfreeze(self)
Unfreeze the TextEditor and reopen it to getch inputs.

### write(self) -> None
Writes the text to its designated coordinates with the view taken into account.
