from termutils import Listener, Term

Listener.start(raw= True)
looper = Listener.looper()
term = Term()

for i in looper:
    term.clear()
    term.write_at(10,0,i)
    term.flush()
