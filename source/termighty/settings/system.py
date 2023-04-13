import platform
import shutil
import threading
import time
import warnings


class System:
    """
    Used to keep track of the terminal dimensions, and detect the current OS. Also contains the `kill_all` class
    attribute, which is by default set to `False`.  If it is set to `True`, all active termighty threads will be killed.
    """

    terminal_size: tuple[int, int] = tuple(shutil.get_terminal_size())[::-1]
    os = platform.system()

    # If the operating system is Darwin (macOS) then will warn the user that it is untested, and default to Linux mode.
    if os == "Darwin":
        warnings.warn("Termighty is untested for Darwin (macOS) platform, but will attempt to run in Linux mode.")
    elif os == "Java":
        warnings.warn("Termighty is untested for Java platform, but will attempt to run in Linux mode.")

    if os == "Windows":
        escape_code_encoding = "oem"
    else:
        escape_code_encoding = "utf"

    # If set to true, stops all processes.
    kill_all = False

    @classmethod
    def track_terminal_shape(cls):
        while not cls.kill_all:
            if (terminal_size := tuple(shutil.get_terminal_size())[::-1]) != cls.terminal_size:
                cls.terminal_size: tuple[int, int] = terminal_size
            time.sleep(0.05)


track_terminal_shape_thread = threading.Thread(target=System.track_terminal_shape, daemon=True)
track_terminal_shape_thread.start()
