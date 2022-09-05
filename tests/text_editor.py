from termutils import TextBox, Term, Listener, WordProcessor
import time

term = Term()
term.clear(flush=True)
Listener.start()
word_processor = WordProcessor(0, 0, -5, -10)
word_processor.start()

# text = ["abcd", "efgh", "ijkl", "mnop"]
# cursor_position = (1,0)
# text, cursor_position = delete(text, cursor_position)
# print(text, cursor_position)
