from termutils.obj.text_box import TextBox
import textwrap
import time


class WordProcessor(TextBox):
    def __init__(self, dt: float = 0.01, tab_len: int = 4):
        """
        Creates an instance of TextEditor.  Supports usage of the default listener provided by class LiveMenu.
        """

    def __call__(self):
        """
        Main loop which runs on one thread, while a listener runs on another and provides commands to be read by
        this method.

        These inputs are accessed via the superclass attribute `LiveMenu._input_state` and are processed in an
        infinite loop until broken.
        """

    def _delete(self):
        """
        Performs a delete on the given list of characters, using the context attached to them (see docstring in
        self._process_key).
        """

    def _ctrl_delete(self):
        """
        Performs a ctrl-delete on the given list of characters, using the context attached to them (see docstring in
        self._process_key).
        """

    def _backspace(self):
        """
        Performs a backspace on the given list of characters, using the context attached to them (see docstring in
        self._process_key).
        """

    def _ctrl_backspace(self):
        """
        Performs a ctrl-backspace on the given list of characters, using the context attached to them (see docstring in
        self._process_key).
        """

    def _ctrl_left(self):
        """
        Moves the cursor to the left until the beginning of the previous word is reached.
        """

    def _ctrl_right(self):
        """
        Moves the cursor to the right until the end of the current word is reached.
        """

    def _ctrl_up(self):
        """
        Swaps the above line with the current one.
        """

    def _ctrl_down(self):
        """
        Swaps the below line with the current one.
        """

    def _process_key(self):
        """
        Takes the current text and modifies it using the given key input.
        """
