import os
import sys

from termighty.settings.data import Data
from termighty.settings.system import System
from termighty.utils.term import Term

import threading
import time

from typing import Callable, Optional, Union

# If the OS is Windows, uses msvcrt to read inputs from the terminal.
if System.os == "Windows":
    import msvcrt

# If the OS is Linux-based, uses termios and tty to read inputs from the terminal.
else:
    import termios
    import tty


class GetchIterator:
    """
    Iterate over the Listener's history starting at the provided index, and continuously yields all new additions to
    the history until the Listener is stopped.  Designed to be used in a for-loop.
    """

    def __init__(self, idx: Optional[int] = None):
        """
        Prepare the indices for the iteration, if they are given.
        """
        self._idx = idx
        self._start_idx = idx

    def __iter__(self):
        """
        If the start index is not given, set it to the current length of the Listener history, in order to start the
        iterator on its last getch inputs. Otherwise, use the given `idx`.
        """
        if self._idx == None:
            self._idx = len(Listener._history)
        else:
            self._idx = self._start_idx
        return self

    def __next__(self):
        """
        Every time a new input is detected by the Listener and appended to its history, return it.
        """
        while Listener._active and not System.kill_all:
            if self._idx < len(Listener._history):
                self._idx += 1
                return Listener._history[self._idx - 1]
            else:
                time.sleep(0.01)
        raise StopIteration


class Listener:

    """
    Superclass that allows the user to display live, dynamic text on the terminal while simultaneously accepting user
    inputs.

    Must be inherited before instantiation, and _writer must be overwritten.  The overwritten _writer should contain
    the main loop displayed to the terminal.

    Only one instance of `Listener` may be active at once.
    """

    _active: bool = False
    _escape_hits: int = 15
    _history: list[str, ...] = []
    _raw: bool = False
    _sleep_time: Union[int, float] = 0.01

    """PRIVATE METHODS"""

    @classmethod
    def _getch_linux(cls) -> bytes:
        """
        Listen for keyboard input, and return a string with a key name (such as `a`, `Z`, or `Backspace`).

        Expects `_raw_mode` to be True, implying the terminal will read user inputs immediately without echoing to the
        terminal.

        Functions exclusively in Linux.
        """
        escape_code: str = os.read(1, 10)
        return escape_code

    @classmethod
    def _getch_windows(cls) -> bytes:
        """
        Listen for keyboard input, and return a string with a key name (such as `a`, `Z`, or `Backspace`).

        Functions exclusively in Windows.
        """
        repeat: bool = True
        escape_code: bytes = b""
        while repeat and not System.kill_all:
            escape_code += msvcrt.getch()
            repeat: bool = msvcrt.kbhit()
        return escape_code

    @classmethod
    def _interpret_escape_code(cls, escape_code: bytes) -> str:
        """ """
        if escape_code in Data.keymaps.keys():
            char: str = Data.keymaps[escape_code]
        else:
            char: str = escape_code.decode(System.escape_code_encoding)

        return char

    @classmethod
    def _listener(cls) -> None:
        """
        An input source for the `writer` callable, as seen in method `set_writer.`  Updates the global variable
        `input_state` by appending the latest keypress to it (interpreted by data/keymaps).

        Expects `_raw_mode` to be True, implying the terminal will read user inputs immediately without echoing to the
        terminal.

        To kill all running threads, hold key `ESC` for a few seconds, or hit it as many times in a row as the value
        given in cls._escape_hits -- be sure not to press any other keys in between or the kill process is interrupted.
        """
        # If this reaches the value given to `cls._escape_hits`, will trigger the `Kill` command.
        escape_hitcount: int = 0
        # While the Listener is active, run the listener loop.
        while Listener._active and not System.kill_all:

            # Get an escape code from the getch method.
            escape_code: str = cls._getch()
            # Get a character or command from the acquired escape code.
            char = cls._interpret_escape_code(escape_code)

            # Check if the character is `Esc`.
            if char == "Esc":
                cls._history.append(char)
                # If increment `escape_hitcount`. hasn't reached its limit, increment it by one.
                if escape_hitcount < cls._escape_hits - 1:
                    escape_hitcount += 1
                    continue
                # If increment `escape_hitcount`. has reached its limit, send the `Kill` command and break.
                else:
                    cls._history.append("Kill")
                    System.kill_all = True
                    cls.stop()

            # If the character is not `Esc`, and `escape_hitcount` is greater than 0, set `escape_hitcount` to zero.
            elif escape_hitcount > 0:
                escape_hitcount = 0

            # If getch returned a string, append it to the key history.
            if isinstance(char, str):
                cls._history.append(char)

    @classmethod
    def _listener_raw(cls) -> None:
        """
        An input source for the `writer` callable, as seen in method `set_writer.`  Updates the global variable
        `input_state` by appending the latest keypress to it (as an ANSI escape sequence or character).

        Expects `_raw_mode` to be True, implying the terminal will read user inputs immediately without echoing to the
        terminal.

        To kill all running threads, hold key `ESC` for a few seconds, or hit it as many times in a row as the value
        given in cls._escape_hits -- be sure not to press any other keys in between or the kill process is interrupted.
        """
        # If this reaches the value given to `cls._escape_hits`, will trigger the `Kill` command.
        escape_hitcount: int = 0
        # While the Listener is active, run the listener loop.
        while Listener._active and not System.kill_all:
            # Get a character or command from the selected getch method.
            escape_code: bytes = cls._getch()
            # Check if the escape code for `Esc` is returned.
            if escape_code == b"\x1b":
                # If increment `escape_hitcount`. hasn't reached its limit, increment it by one.
                if escape_hitcount < cls._escape_hits - 1:
                    escape_hitcount += 1
                # If increment `escape_hitcount`. has reached its limit, send the `Kill` command and break.
                else:
                    cls._history.append("Kill")
                    System.kill_all = True
                    cls.stop()

            cls._history.append(escape_code)

    @classmethod
    def _raw_mode_linux(cls, state: bool) -> None:
        """
        Set the terminal to raw mode if True, or to echo mode if False
        """
        if state:
            tty.setraw(sys.stdin.fileno())
            # tty.setcbreak(sys.stdin.fileno())

        elif not state:
            termios.tcsetattr(cls._fd, termios.TCSADRAIN, cls._old_settings)
        cls._raw: bool = state

    @classmethod
    def _raw_mode_windows(cls, state: bool) -> None:
        """
        Windows placeholder for raw mode, which is only necessary in Linux.
        """
        cls._raw: bool = state

    """PUBLIC METHODS"""

    @classmethod
    def getch_iterator(cls, idx: Optional[int] = None, keytest: bool = False) -> GetchIterator:
        """ """
        return GetchIterator(idx=idx)

    @classmethod
    def start(cls, raw: bool = False) -> None:
        """
        Activate the Listener session.  If `raw` is set to True, will not interpret the escape codes input by the user,
        and simply append the raw escape code bytes to the history.
        """
        if not Listener._active:
            Listener._active: bool = True

            if raw:
                thread_listener: threading.Thread = threading.Thread(target=cls._listener_raw, daemon=False)
            else:
                thread_listener: threading.Thread = threading.Thread(target=cls._listener, daemon=False)

            cls._raw_mode(True)

            try:
                thread_listener.start()
            except Exception as e:
                cls._raw_mode(False)
                System.kill_all = True
                raise Exception(e)

    @classmethod
    def stop(cls) -> None:
        """
        Deactivate the Listener session.
        """
        cls._raw_mode(False)
        Listener._active: bool = False
        Listener._history = []
        Term().clear(flush=True)

    """DYNAMICALLY SELECT CLASSMETHODS BY OS"""

    # If the OS is Windows, use _getch_windows as backend for _getch, and _raw_mode_windows as backend for _raw.
    if System.os == "Windows":
        _getch: classmethod = _getch_windows
        _raw_mode: classmethod = _raw_mode_windows
    # If the OS is Linux, use _getch_linux as backend for _getch, and _raw_mode_linux as backend for _raw.
    # Additionally, save the terminal's old tty attributes for when raw mode is deactivated.
    else:
        _getch: classmethod = _getch_linux
        _raw_mode: classmethod = _raw_mode_linux
        _fd: str = sys.stdin.fileno()
        _old_settings: list[str, list[bytes]] = termios.tcgetattr(_fd)
