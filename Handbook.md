# Introduction and Basic Example

Using **Termighty** is simple and straightforward.  You can create a simple image in just a few lines of code:

  ```python
  from Termighty import Termighty as term

  text = "┏━┓\n┃ ┃\n┗━┛"
  text_color = "ggg\nrdr\nbbb"
  background_color = "ddd\ndrd\nddd"

  image = term.design_Charray(chars = text, t_colors = text_color,
  b_colors = background_color)

  image.display()
  ```

Running the above outputs the following:
  ```python
  ┏━┓
  ┃ ┃
  ┗━┛
  ```
If this is run in the terminal, the top row will be green, the middle red, and the bottom blue.

# Documentation

## Char
### Summary
A single-character "pixel" that can have a custom text and/or background color.

## Charray
### Summary
An array of Char objects, can modify individual array elements using indexing.  Row-major; indices take the form (row, column), or in other words (height, width).
### Methods

`__init__(self, c = None, t_color = "default", b_color = "default", style = "default"`
> Checks that all parameters are valid:
>
> |Parameter| Description|
> |---|---|
> |`c`|           A single character string|
> |`t_color`|     Key or alias in `text_colors`|
> |`b_color`|     Key or alias in `back_colors`|
> |`style`|       Key or alias in `styles`|

`__str__(self)`

> For printing

`__eq__(self, new)`

> Checks if all the attributes in one `Char` matches those of another `Char` via the `==` operator.

`set_text(self, c)`

> Replace the character string by passing a new single-character string to `c`

`set_t_color(self, t_color)`

> Replace the text color by passing a new text color to `t_color`.  Color guide is in the appendix.

`set_b_color(self, b_color)`

> Replace the background color by passing a new background color to `b_color`.  Color guide is in the appendix.

`set_style(self, style)`

> Replace the text style by passing a new text style to `style`.  Style guide is in the appendix.

`copy(self)`

> Copies the current state of the `Char` object to a new `Char` object, to prevent issues with memory addresses.

`compact(self)`

> Returns three integers with the `Char` object's color and style data

`overwrite(self, new)`

> Re-initialize this object in-place with another `Char` object - just pass the replacement to `new`.

`display(self)`

> Prints the character to the terminal

## String
### Summary
Meant to emulate `type <str>` in the Terminal environment by supporting a good number of `type<str>` functions.

## Terminal
### Summary
An intermediary for the terminal that allows for easier graphics visualization and interactivity.

All actions are "live" in this object; for example, `Terminal.__setitem__` will both reassign one (or more) elements *and* display the changes on the terminal immediately.

# Appendix

## Colors and Styles

Text colors, background colors, and styles are all saved in */Termighty/utils/config.py* as dictionaries which are not meant to be directly accessible.  Instead, use the following tables as reference:
### Text Color

|Color Key|Key Alias|Unicode Value|
|---|---|---|
|black|k|30|
|red|r|31|
|green|g|32|
|yellow|y|33|
|blue|b|34|
|purple|p|35|
|cyan|c|36|
|white|w|37|
|default|d|37|

### Background Color

|Color Key|Key Alias|Unicode Value|
|---|---|---|
|black|k|40|
|red|r|41|
|green|g|42|
|yellow|y|43|
|blue|b|44|
|purple|p|45|
|cyan|c|46|
|white|w|47|
|default|d|1|

### Text Style

|Style Key|Key Alias|Unicode Value|
|---|---|---|
|default|d|0|
|bold|b|1|
|faded|f|2|
|italic|i|3|
|underlined|u|4|
|negative|n|7|
|strikethrough|s|9|
