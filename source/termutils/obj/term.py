import sys
import threading


class Term:
    """
    A collection of commands that can be used to make modifications to the terminal state.
    """

    _flush_lock = threading.Lock()

    def __init__(self) -> None:
        """
        While class Term could theoretically consist only of classmethods, it is instanced to allow for the existence of
        multiple buffers that each can be flushed and appended independently of others.
        """
        self._buffer = []

    def clear(self) -> None:
        """
        Cross-platform terminal clear command (appends to the buffer).
        """
        self._buffer.append("\033[2J\033[3J\033[f")

    def clear_now(self) -> None:
        """
        Cross-platform terminal clear command -- clears immediately (bypasses the buffer).
        """
        with self.__class__._flush_lock:
            sys.stdout.write("\033[2J\033[3J\033[f")
            sys.stdout.flush()

    def cursor_hide(self) -> None:
        """
        Make the cursor invisible (appends to the buffer).
        """
        self._buffer.append("\033[?25l")

    def cursor_hide_now(self) -> None:
        """
        Make the cursor invisible immediately (bypasses the buffer).
        """
        with self.__class__._flush_lock:
            sys.stdout.write("\033[?25l")
            sys.stdout.flush()

    def cursor_load(self) -> None:
        """
        Loads the cursor position (appends to the buffer) -- save it first by calling `cursor_save`.
        """
        self._buffer.append("\0338")

    def cursor_load_now(self) -> None:
        """
        Loads the cursor position immediately (bypasses the buffer) -- save it first by calling `cursor_save_now`.
        """
        with self.__class__._flush_lock:
            sys.stdout.write("\0338")
            sys.stdout.flush()

    def cursor_move(self, line: int, column: int) -> None:
        """
        Move the cursor to the given `line` and `column` (appends to the buffer).
        """
        self._buffer.append(f"\033[{line};{column}H")

    def cursor_move_now(self, line: int, column: int) -> None:
        """
        Move the cursor to the given `line` and `column` immediately (bypasses the buffer).
        """
        with self.__class__._flush_lock:
            sys.stdout.write(f"\033[{line};{column}H")
            sys.stdout.flush()

    def cursor_save(self) -> None:
        """
        Save the cursor position (appends to the buffer) -- reload it by calling `cursor_load`.
        """
        self._buffer.append("\0337")

    def cursor_save_now(self) -> None:
        """
        Save the cursor position immediately (bypasses the buffer) -- reload it by calling `cursor_load_now`.
        """
        with self.__class__._flush_lock:
            sys.stdout.write("\0337")
            sys.stdout.flush()

    def cursor_show(self) -> None:
        """
        Make the cursor visible (appends to the buffer).
        """
        self._buffer.append("\033[?25h")

    def cursor_show_now(self) -> None:
        """
        Make the cursor visible immediately (bypasses the buffer).
        """
        with self.__class__._flush_lock:
            sys.stdout.write("\033[?25h")
            sys.stdout.flush()

    def flush(self) -> None:
        """
        Flush the entire buffer to the terminal. Removes whatever is flushed from the buffer; if something is appended
        to the buffer while the flushing occurs, does not remove that element from the buffer.
        """
        with self.__class__._flush_lock:
            current_buffer_state = self._buffer.copy()
            sys.stdout.write("".join(current_buffer_state))
            sys.stdout.flush()
            for i in range(len(current_buffer_state)):
                self._buffer.pop(0)

    def write(self, string: str) -> None:
        """
        Write the given `string` wherever the cursor is currently positioned to the buffer (appends to the buffer).
        """
        self._buffer.append(f"{string}")

    def write_at(self, line: int, column: int, string: str) -> None:
        """
        Write the given `string` starting at the designated `line` and `column` coordinates to the buffer.  ANSI uses a
        one-based indexing system, but this class instead uses a zero-based indexing system.
        """
        self._buffer.append(f"\x1b[{line+1};{column+1}f{string}")
