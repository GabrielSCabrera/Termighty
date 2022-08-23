from termutils.data import Data
from typing import Callable, Optional, Union
import threading
import warnings
import shutil
import time
import sys
import os


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
    Superclass that allows the user to display live, dynamic text on the terminal while simultaneously accepting user
    inputs.

    Must be inherited before instantiation, and _writer must be overwritten.  The overwritten _writer should contain
    the main loop displayed to the terminal.
    """

    _raw_mode: bool = False
    _active: bool = False

    def __init__(self, escape_hits: int = 15) -> None:
        """
        Creates a new, inactive instance of LiveMenu.  Arguments `rows` and `cols` should be integers greater than zero.
        """
        self._escape_hits: int = escape_hits
        self._sleep_time: Union[int, float] = 0.01
        self._key_history: list[str, ...] = []

    """CLASSMETHODS"""

    @classmethod
    def _getch_linux(cls) -> str:
        """
        Listens for keyboard input, and returns a string with a key name (such as `a`, `Z`, or `Backspace`).

        Expects `_raw_mode` to be True, implying the terminal will read user inputs immediately without echoing to the
        terminal.

        Functions exclusively in Linux.
        """
        key: str = os.read(1, 10).decode("utf8")

        if key in Data.keymaps.keys():
            char: str = Data.keymaps[str(key)]
        else:
            char: str = key.decode("utf-8")

        return char

    @classmethod
    def _getch_windows(cls) -> str:
        """
        Listens for keyboard input, and returns a string with a key name (such as `a`, `Z`, or `Backspace`).

        Functions exclusively in Windows.
        """
        repeat: bool = True
        key: bytes = b""
        while repeat:
            key += msvcrt.getch()
            repeat: bool = msvcrt.kbhit()

        if key in Data.keymaps.keys():
            char: str = Data.keymaps[key]
        else:
            char: str = key.decode("oem")

        return char

    @classmethod
    def _raw_linux(cls, state: bool) -> None:
        """
        Sets the terminal to raw mode if True, or to echo mode if False
        """
        if state:
            tty.setraw(sys.stdin.fileno())
        elif not state:
            termios.tcsetattr(cls._fd, termios.TCSADRAIN, cls._old_settings)
        cls._raw_mode: bool = state

    @classmethod
    def _raw_windows(cls, state: bool) -> None:
        """
        Windows placeholder for raw mode, which is only necessary in Linux.
        """
        cls._raw_mode: bool = state

    """DYNAMICALLY SELECT CLASSMETHODS BY OS"""

    # If the OS is Windows, use _getch_windows as backend for _getch, and _raw_windows as backend for _raw.
    if _OS_mode == "WINDOWS":
        _getch: classmethod = _getch_windows
        _raw: classmethod = _raw_windows
    # If the OS is Linux, use _getch_linux as backend for _getch, and _raw_linux as backend for _raw.
    # Additionally, save the terminal's old tty attributes for when raw mode is deactivated.
    elif _OS_mode == "LINUX":
        _getch: classmethod = _getch_linux
        _raw: classmethod = _raw_linux
        _fd: str = sys.stdin.fileno()
        _old_settings: list[str, list[bytes]] = termios.tcgetattr(_fd)

    """PROPERTIES"""

    @property
    def active(self) -> bool:
        """
        Returns True if the current instance is active. False otherwise.
        """
        return LiveMenu._active

    @property
    def columns(self) -> int:
        """
        Returns the display width (number of columns).
        """
        return self.terminal_size[0]

    @property
    def lines(self) -> int:
        """
        Returns the display height (number of lines).
        """
        return self.terminal_size[1]

    @property
    def terminal_size(self) -> tuple[int, int]:
        """
        Returns the terminal dimensions.
        """
        return tuple(shutil.get_terminal_size())

    """MAGIC METHODS"""

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

    def _listener(self) -> None:
        """
        An input source for the `writer` callable, as seen in method `set_writer.`  Updates the global variable
        `input_state` by appending the latest keypress to it.

        Expects `_raw_mode` to be True, implying the terminal will read user inputs immediately without echoing to the
        terminal.
        """
        # If this reaches the value given to `self._escape_hits`, will trigger the `Kill` command.
        escape_hitcount: int = 0
        # While the LiveMenu is active, run the listener loop.
        while LiveMenu._active:
            # Get a character or command from the selected getch method.
            char: str = self._getch()

            # Check if the character is `Esc`.
            if char == "Esc":
                # If increment `escape_hitcount`. hasn't reached its limit, increment it by one.
                if escape_hitcount < self._escape_hits - 1:
                    escape_hitcount += 1
                    continue
                # If increment `escape_hitcount`. has reached its limit, send the `Kill` command and break.
                else:
                    self._key_history.append("Kill")
                    break
            # If the character is not `Esc`, and `escape_hitcount` is greater than 0, set `escape_hitcount` to zero.
            elif escape_hitcount > 0:
                escape_hitcount = 0

            # If getch returned a string, append it to the key history.
            if isinstance(char, str):
                self._key_history.append(char)

    def _terminal_monitor(self) -> None:
        """
        A loop that keeps track of terminal statistics, such as its dimensions (given by shutil.get_terminal_size).
        """
        while LiveMenu._active:
            self._terminal_size: os.terminal_size = shutil.get_terminal_size()
            time.sleep(self._sleep_time)

    def _writer(self) -> None:
        """
        Must be inherited before instantiation, and _writer must be overwritten.  The overwritten _writer must contain
        the main loop that prints to the terminal.
        """
        error_message: str = "\n" * 2 + "".join([line.strip() for line in self._step.__doc__.split("\n")])
        raise NotImplementedError(error_message)

    """PUBLIC METHODS"""

    def start(self) -> None:
        """
        Activates the LiveMenu session.
        """
        if LiveMenu._active:
            LiveMenu._active: bool = False
            self._raw(False)
            msg: str = (
                "\n\nLiveMenu is already active, cannot run method `start` on multiple separate instances.  Call "
                "method `stop` on current active instance before attempting to activate this one.\n"
            )
            raise RuntimeError(msg)

        elif not LiveMenu._active:
            LiveMenu._active: bool = True

            thread_listener: threading.Thread = threading.Thread(target=self._listener, daemon=True)
            thread_terminal_monitor: threading.Thread = threading.Thread(target=self._terminal_monitor, daemon=True)
            thread_writer: threading.Thread = threading.Thread(target=self._writer, daemon=True)

            self._raw(True)

            try:
                print(f"\033[2J\033[3J\033[f", end="", flush=True)
                thread_listener.start()
                thread_terminal_monitor.start()
                thread_writer.start()

                while LiveMenu._active:
                    time.sleep(self._sleep_time)

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
        self._raw(False)
        LiveMenu._active: bool = False
        print(f"\033[2J\033[3J\033[f", end="", flush=True)
