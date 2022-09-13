import codecs
import importlib.resources
import json
from termighty.settings.system import System


class Data:
    """
    Dataclass that contains all the package data.  Can be used to decode ANSI escape sequences, get RGB values from
    color names, and access ANSI codes for string styles.
    """
    with importlib.resources.open_text("termighty.data", "keymaps.json") as infile:
        keymaps = json.load(infile)

    # Loads a set of keymaps depending on the current OS in use.
    if System.os == "Windows":
        keymaps = keymaps["windows"]
    else:
        keymaps = keymaps["linux"]
    # Encoding the dictionary keys using the OEM-standard.
    keymaps = {codecs.escape_decode(key)[0]: value for key, value in keymaps.items()}

    with importlib.resources.open_text("termighty.data", "rgb.json") as infile:
        colors = json.load(infile)

    with importlib.resources.open_text("termighty.data", "styles.json") as infile:
        styles = json.load(infile)
