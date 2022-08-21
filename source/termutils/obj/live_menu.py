from termutils.data import Data
from typing import Optional, Callable
import threading
import warnings
import shutil
import time
import sys
import os

from termutils.config.defaults import term_rows, term_cols, term_fd, term_settings

# If the OS is Windows, uses msvcrt to read inputs from the terminal.
try:
    import msvcrt
    _OS_mode = "WINDOWS"

# If the OS is Linux-based, uses termios and tty to read inputs from the terminal.
except ImportError:
    import termios
    import tty
    _OS_mode = "LINUX"


class LiveMenu:

    """
    Superclass that allows the user to display live, changing text on the terminal while simultaneously accepting user
    inputs.

    Must be inherited before instantiation, and __call__ must be overwritten.  The overwritten __call__ should contain
    the main loop displayed to the terminal
    """

    _active = False
    _fd = term_fd  # sys.stdin.fileno()
    _old_settings = term_settings  # termios.tcgetattr(_fd)
    _raw_mode = False

    """CONSTRUCTOR"""

    def __init__(self, rows: Optional[int] = None, cols: Optional[int] = None, escape_hits: Optional[int] = 15) -> None:
        """
        Creates a new, inactive instance of LiveMenu.  Arguments `rows` and `cols` should be integers greater than zero.
        """
        default_dims = shutil.get_terminal_size((term_rows, term_cols))

        if rows is None:
            rows = default_dims[1]

        if cols is None:
            cols = default_dims[0]

        self._escape_hits = escape_hits

        self._dims = (rows, cols)
        self._current_active = False
        self._listener = self._default_listener
        self._kill = False
        self._key_history = []

    """GETTERS"""

    @property
    def dims(self) -> tuple[int]:
        """
        Returns the terminal dimensions.
        """
        return self._dims

    @property
    def rows(self) -> int:
        """
        Returns the display height (number of rows).
        """
        return self._dims[0]

    @property
    def cols(self) -> int:
        """
        Returns the display width (number of columns).
        """
        return self._dims[1]

    @property
    def active(self) -> bool:
        """
        Returns True if the current instance is active. False otherwise.
        """
        return self._current_active

    def __call__(self):
        """
        Must be inherited before instantiation, and __call__ must be overwritten.  The overwritten __call__ must
        contain the main loop that prints to the terminal.
        """
        error_message = "\n" * 2 + "".join([line.strip() for line in self.__call__.__doc__.split("\n")])
        raise NotImplementedError(error_message)

    """SETTERS"""

    def set_dims(self, rows: Optional[int] = None, cols: Optional[int] = None) -> None:
        """
        Sets the terminal dimensions.
        """
        if rows is None:
            rows = self._dims[0]
        if cols is None:
            cols = self._dims[1]
        self._dims = (rows, cols)

    def set_listener(self, listener: Callable) -> None:
        """
        The callable will create an input source for the `writer` attribute, seen in method `set_writer.` By default,
        calls private method `_default_listener`.

        Note: avoid changing the listener, the default will usually do the trick!
        """
        self._listener = listener

    """RUNTIME"""

    def start(self) -> None:
        """
        Activates the LiveMenu session.
        """
        if LiveMenu._active:
            self.__class__._raw(False)
            msg = (
                "\n\nLiveMenu is already active, cannot run method `start` on multiple separate instances.  Call "
                "method `stop` on current active instance before attempting to activate this one.\n"
            )
            raise RuntimeError(msg)
        self._current_active = True
        LiveMenu._active = True

        thread_listener = threading.Thread(target=self._listener)
        thread_terminal_monitor = threading.Thread(target=self._terminal_monitor)
        thread_writer = threading.Thread(target=self.__call__)

        self._raw(True)

        try:
            print(f"\033[2J\033[3J\033[f", end="", flush=True)
            thread_listener.start()
            thread_writer.start()

            while thread_listener.is_alive():
                time.sleep(0.01)

            thread_listener.join()
            thread_writer.join()
        except Exception as e:
            print(f"\033[2J\033[3J\033[f", end="", flush=True)
            self._raw(False)
            raise Exception(e)

        self._raw(False)

    def stop(self) -> None:
        """
        Deactivates the LiveMenu session.
        """
        if not LiveMenu._active:
            switch = self.__class__._raw_mode
            if switch:
                self.__class__._raw(False)
            msg = "\n\nAttempted to stop an inactive LiveMenu.\n"
            warnings.warn(msg)
            if switch:
                self.__class__._raw(True)
        else:
            self.__class__._raw(False)
            LiveMenu._active = False
            self._current_active = False

        print(f"\033[2J\033[3J\033[f", end="", flush=True)

    def __enter__(self) -> None:
        """
        Context manager wrapper for `start`.
        """
        self.start()

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Context manager wrapper for `stop`.
        """
        self.stop()

    """PRIVATE METHODS"""

    @classmethod
    def _raw(cls, state: bool) -> None:
        """
        Sets the terminal to raw mode if True, or to echo mode if False
        """
        if _OS_mode == "WINDOWS":
            if state:
                cls._raw_mode = True
            elif not state:
                cls._raw_mode = False

        elif _OS_mode == "LINUX":
            if state:
                tty.setraw(sys.stdin.fileno())
                cls._raw_mode = True
            elif not state:
                termios.tcsetattr(cls._fd, termios.TCSADRAIN, cls._old_settings)
                cls._raw_mode = False

    def _default_listener(self) -> str:
        """
        An input source for the `writer` callable, as seen in method `set_writer.`  Updates the global variable
        `input_state` by appending the latest keypress to it.

        Expects `_raw_mode` to be True, implying the terminal will read user inputs immediately without echoing to the
        terminal.
        """
        escape_hitcount = 0
        try:
            print("\033[?1002h", end="", flush=True)
            while not self._kill:
                output = self._get_input()
                if output == "Esc":
                    if escape_hitcount < self._escape_hits - 1:
                        escape_hitcount += 1
                        continue
                    else:
                        self._key_history.append("Kill")
                        break
                elif escape_hitcount > 0 and output != "Esc":
                    escape_hitcount = 0
                if isinstance(output, str):
                    self._key_history.append(output)
        except Exception as e:
            print("\033[?1002l", end="", flush=True)
            raise Exception(e)
        print("\033[?1002l", end="", flush=True)

    def _terminal_monitor(self):
        """
        A loop that keeps track of terminal statistics, such as its dimensions (given by os.get_terminal_size).
        """

    @classmethod
    def _get_input(cls) -> str:
        """
        Listens for keyboard input, and returns a string with a key name (such as `a`, `Z`, or `Backspace`).

        Expects `_raw_mode` to be True, implying the terminal will read user inputs immediately without echoing to the
        terminal.
        """
        if _OS_mode == "WINDOWS":
            repeat = True
            key = b""
            while repeat:
                key += msvcrt.getch()
                repeat = msvcrt.kbhit()

            if key in Data.keymaps.keys():
                output = Data.keymaps[key]
            else:
                output = key.decode("oem")

        elif _OS_mode == "LINUX":
            key = os.read(1, 10).decode()

            if key in Data.keymaps.keys():
                output = Data.keymaps[str(key)]
            else:
                output = key.decode("utf-8")

        return output
