from termutils import TextBox, Term, Listener, WordProcessor
import time

term = Term()
title_bar_height = 1

title_bar = TextBox(0, 0, title_bar_height, -1, background="Purple Navy")
title_bar.align("center")
main_window = WordProcessor(title_bar_height, 0, -2, -1)

title_bar(["WORD PROCESSOR (hold ESC to exit)"])
main_window(["Line 1" + "."*100, "Line 2 is longer", "Line 3"])

term.clear(flush=True)
Listener.start()
title_bar.start()
main_window.start()
