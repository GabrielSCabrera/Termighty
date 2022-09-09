import codecs
import importlib.resources
import json
from termutils.settings.system import System


class Data:
    """
    Dataclass that contains all the package data.  Can be used to decode ANSI escape sequences, get RGB values from
    color names, and access ANSI codes for string styles.
    """

    with importlib.resources.open_text("termutils.data", "keymaps.json") as infile:
        keymaps = json.load(infile)

    # Loads a set of keymaps depending on the current OS in use.
    if System.os == "Windows":
        keymaps = keymaps["windows"]
        # Encoding the dictionary keys using the OEM-standard.
        keymaps = {codecs.escape_decode(key)[0]: value for key, value in keymaps.items()}
    elif System.os == "Linux":
        keymaps = keymaps["linux"]

    with importlib.resources.open_text("termutils.data", "rgb.json") as infile:
        colors = json.load(infile)

    with importlib.resources.open_text("termutils.data", "styles.json") as infile:
        styles = json.load(infile)
