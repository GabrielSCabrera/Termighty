import os
import platform
import shutil
import threading
import time
import warnings


class System:

    terminal_size: tuple[int, int] = tuple(shutil.get_terminal_size())[::-1]
    os = platform.system()

    # If the operating system is Darwin (macOS) then will warn the user that it is untested, and default to Linux mode.
    if os == "Darwin":
        warnings.warn("TermUtils is untested for Darwin (macOS) platform, but will attempt to run in Linux mode.")
        os = "Linux"
    elif os == "Java":
        warnings.warn("TermUtils is untested for Java platform, but will attempt to run in Linux mode.")
        os = "Linux"

    if os == "Windows":
        escape_code_encoding = "oem"
    elif os == "Linux":
        escape_code_encoding = "utf"

    @classmethod
    def track_terminal_shape(cls):
        while True:
            if (terminal_size := tuple(shutil.get_terminal_size())[::-1]) != cls.terminal_size:
                cls.terminal_size: tuple[int, int] = terminal_size
            time.sleep(0.05)


track_terminal_shape_thread = threading.Thread(target=System.track_terminal_shape, daemon=True)
track_terminal_shape_thread.start()
