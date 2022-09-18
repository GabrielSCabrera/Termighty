from termighty import TextBox, Term, Listener, TextEditor
import time

term = Term()
title_bar_height = 1

title_bar = TextBox(0, 0, title_bar_height, -1, background="Purple Navy")
title_bar.alignment = "center"
main_window = TextEditor(title_bar_height, 0, -2, -1, line_numbers=True)

title_bar(["TEXT EDITOR (hold ESC to exit)"])
main_window(["Line 1", "Line 2 is longer", "Line 3", "Line 4", "Line 5"])

term.clear(flush=True)
Listener.start()
title_bar.start()
main_window.start()
