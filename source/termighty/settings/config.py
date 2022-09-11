import importlib.resources
import configparser


class Config:
    """
    Dataclass that contains the program settings as given in `config.ini`.
    """

    with importlib.resources.open_text("termighty", "config.ini") as infile:
        parser = configparser.ConfigParser()
        parser.readfp(infile)

    # The name of the default background color.
    background_color = parser["Colors and Style"]["background color"]
    # The name of the default foreground color.
    foreground_color = parser["Colors and Style"]["foreground color"]
    # The name of the default text style.
    style = parser["Colors and Style"]["style"]
    # The default number of spaces per tab.
    tab_length = int(parser["Formatting"]["tab length"])
