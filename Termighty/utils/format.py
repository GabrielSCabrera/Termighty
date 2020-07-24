from ..config import escape_sequence as esc

def bold(string):
    return esc.format(1) + string + esc.format('')

def italic(string):
    return esc.format(3) + string + esc.format('')

def underline(string):
    return esc.format(4) + string + esc.format('')
