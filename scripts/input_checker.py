from termutils import Listener, Term

Listener.start()
getch_iterator = Listener.getch_iterator()
term = Term()
term.clear()
term.cursor_hide(flush=True)
term.write_at(0, 0, "Your Input:")
term.write_at(1, 0, f"> ")
term.write_at(3, 0, f"Hold ESC for a few seconds to quit.")
term.flush()

i_prev = None
for i in getch_iterator:
    if i != i_prev:
        i_prev = i
        term.clear()
        term.write_at(0, 0, "Your Input:")
        term.write_at(1, 0, f"> {i}")
        term.write_at(3, 0, f"Hold ESC for a few seconds to quit.")
        term.flush()

term.cursor_show(flush=True)
term.clear(flush=True)
