import importlib.resources
import configparser


class Config:
    """
    Dataclass that contains the program settings as given in `config.ini`.
    """

    with importlib.resources.open_text("termighty", "config.ini") as infile:
        parser = configparser.ConfigParser()
        parser.readfp(infile)

    # The default background color.
    background_color = parser["Colors and Style"]["background color"]
    # The default foreground color.
    foreground_color = parser["Colors and Style"]["foreground color"]
    # The default text style.
    style = parser["Colors and Style"]["style"]

    # The default background color for selected text.
    selected_background_color = parser["Colors and Style"]["selected text background color"]
    # The default foreground color for selected text.
    selected_foreground_color = parser["Colors and Style"]["selected text foreground color"]
    # The default style for selected text.
    selected_style = parser["Colors and Style"]["selected text style"]

    # The default background color for line numbers.
    line_numbers_background_color = parser["Colors and Style"]["line numbers background color"]
    # The default foreground color for line numbers.
    line_numbers_foreground_color = parser["Colors and Style"]["line numbers foreground color"]
    # The default style for line numbers.
    line_numbers_style = parser["Colors and Style"]["line numbers style"]

    # The default number of spaces per tab.
    tab_length = int(parser["Formatting"]["tab length"])

    # The minimum width of the column containing line numbers (if line numbers are active).
    line_numbers_width = int(parser["Formatting"]["line numbers minimum width"])
