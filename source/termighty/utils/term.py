import sys
import threading


class Term:
    """
    A collection of commands that can be used to make modifications to the terminal state.
    """

    _flush_lock = threading.Lock()

    def __init__(self, flush: bool = False) -> None:
        """
        While class Term could theoretically consist only of classmethods, it is instanced to allow for the existence of
        multiple buffers that each can be flushed and appended independently of others.

        By default, methods that write to the terminal are not set to flush the buffer when called, which improves
        performance (just rememeber to call the `flush` method when you want the buffer to be printed to the terminal).
        If the `flush` parameter is set to True however, then the buffer is bypassed and the command outputs immediately
        to the terminal.
        """
        self._text_buffer_grid = {}
        self._text_buffer = []
        self._cursor_buffer = []

    def bell(self, flush: bool = False) -> None:
        """
        Play the terminal bell sound.
        """
        string = "\a"
        if not flush:
            self._text_buffer.append(string)
        else:
            self.flush_string(string)

    def clear(self, flush: bool = False) -> None:
        """
        Cross-platform terminal clear command (appends to the buffer).
        """
        string = "\033[2J\033[3J\033[f"
        if not flush:
            self._text_buffer.append(string)
            # There is no need to keep the prior buffer elements as they will be cleared anyways.
            for i in range(len(buffer))[::-1]:
                self._text_buffer.pop(i)
        else:
            self.flush_string(string)

    def _compile_buffer(self, text_buffer_grid):
        """
        Prepares the buffer for flushing -- improves efficiency by avoiding printing over a specific position more than
        once.
        """
        # TODO

    def cursor_hide(self, flush: bool = False) -> None:
        """
        Make the cursor invisible (appends to the buffer).
        """
        string = "\033[?25l"
        if not flush:
            self._text_buffer.append(string)
        else:
            self.flush_string(string)

    def cursor_load(self, flush: bool = False) -> None:
        """
        Load the cursor position (appends to the buffer) -- save it first by calling `cursor_save`.
        """
        string = "\0338"
        if not flush:
            self._text_buffer.append(string)
        else:
            self.flush_string(string)

    def cursor_move(self, line: int, column: int, flush: bool = False) -> None:
        """
        Move the cursor to the given `line` and `column` (appends to the buffer).
        """
        string = f"\033[{line+1};{column+1}H"
        if not flush:
            self._text_buffer.append(string)
        else:
            self.flush_string(string)

    def cursor_save(self, flush: bool = False) -> None:
        """
        Save the cursor position (appends to the buffer) -- reload it by calling `cursor_load`.
        """
        string = "\0337"
        if not flush:
            self._text_buffer.append(string)
        else:
            self.flush_string(string)

    def cursor_show(self, flush: bool = False) -> None:
        """
        Make the cursor visible (appends to the buffer).
        """
        string = "\033[?25h"
        if not flush:
            self._text_buffer.append(string)
        else:
            self.flush_string(string)

    def flush(self) -> None:
        """
        Flush the entire buffer to the terminal. Remove whatever is flushed from the buffer; if something is appended
        to the buffer while the flushing occurs, does not remove that element from the buffer.
        """
        with self.__class__._flush_lock:
            current_buffer_state = self._text_buffer.copy()
            buffer = self._compile_buffer(self._text_buffer.copy())
            sys.stdout.write("".join(current_buffer_state))
            sys.stdout.flush()
            for i in range(len(current_buffer_state)):
                self._text_buffer.pop(0)

    def flush_string(self, string: str) -> None:
        """
        Write and flushes the given string to the terminal.
        """
        with self.__class__._flush_lock:
            sys.stdout.write(string)
            sys.stdout.flush()

    # def write(self, string: str, flush: bool = False) -> None:
    #     """
    #     TODO: Rewrite for buffer compiler
    #     Write the given `string` wherever the cursor is currently positioned to the buffer (appends to the buffer).
    #     """
    #     if not flush:
    #         self._text_buffer.append(f"{string}")
    #     else:
    #         self.flush_string(string)

    def write(self, line: int, column: int, string: str, flush: bool = False) -> None:
        """
        Write the given `string` starting at the designated `line` and `column` coordinates to the buffer.  ANSI uses a
        one-based indexing system, but this class instead uses a zero-based indexing system.
        """
        if not flush:
            self._text_buffer.append(f"\x1b[{line+1};{column+1}f{string}")
            # self._text_buffer_grid[f"line+1 column+1"] = string
        else:
            self.flush_string(f"\x1b[{line+1};{column+1}f{string}")
