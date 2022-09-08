from termutils import TextBox, Term, Listener, WordProcessor
import time

term = Term()
term.clear(flush=True)
Listener.start()
word_processor = WordProcessor(5, 5, -5, -10)
word_processor(["Line 1", "Line 2 is longer", "Line 3"])
word_processor.start()
