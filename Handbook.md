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

---

`__str__()`

> Allows `Char` objects to be printed to the terminal via `print()`

---

`__eq__(new)`

> Checks if all the attributes in one `Char` matches those of another `Char` via the `==` operator.

---

`set_text(c)`

> Replace the character string by passing a new single-character string to `c`

---

`set_t_color(t_color)`

> Replace the text color by passing a new text color to `t_color`.  Color guide is in the appendix.

---

`set_b_color(b_color)`

> Replace the background color by passing a new background color to `b_color`.  Color guide is in the appendix.

---

`set_style()`

> Replace the text style by passing a new text style to `style`.  Style guide is in the appendix.

---

`copy()`

> Copies the current state of the `Char` object to a new `Char` object, to prevent issues with memory addresses.

---

`compact()`

> Returns three integers with the `Char` object's color and style data

---

`overwrite(new)`

> Re-initialize this object in-place with another `Char` object - just pass the replacement to `new`.

---

`display()`

> Prints the character to the terminal

---

## Charray
### Summary
An array of Char objects, can modify individual array elements using indexing.  Row-major; indices take the form (row, column), or in other words (height, width).

### Methods

`__init__(height = None, width = None, t_color = "default", b_color = "default", style = "default", arr = None)`

> Checks that all parameters are valid:
>
> |Parameter| Description|
> |---|---|
> |`c`|           A single character string|
> |`t_color`|     Key or alias in `text_colors`|
> |`b_color`|     Key or alias in `back_colors`|
> |`style`|       Key or alias in `styles`|

---

`__getitem__(idx)`

> Access `Charray` elements or sub-arrays by indexing – supports *integers* and *slices*.

---

`__setitem__(idx, new)`

> Replace single or multiple elements of a `Charray` via indexing – supports *integers* and *slices*.

---

`__str__()`

> Allows `Charray` objects to be printed to the terminal via `print()`

---

`__repr__()`

> Returns an unambiguous representation of a `Char` object

---

`__iter__()`

> Makes `Charray` objects into interables:
>
> Iterates through each element in this Charray, yielding a tuple
> of coordinates followed by the value at that coordinate:

  C = Charray(...)
    for (height, width), value in C:
      ...

---

`copy()`

> Returns a copy of the current object.  Use this to avoid unintentionally overwriting other objects' data.

---

`save()`

> Saves the array data to a file, which can be loaded using the `load_Charray(filename, directory = "./")` function.

---
Prints the `Charray`
`display()`

> elements to the terminal.

---

### Functions

The functions below can be used to create and manage `Charray` objects.

`delete_Charray(filename, directory = "./")`

> Given a *filename* (and an optional *directory*) will attempt to delete the `.chc` and `.chs` files associated with the name.
>
> Returns a tuple `(bool, bool)`, which informs whether or not the files existed in the first place, for the `.chc` and `.chs` respectively.

---

`load_Charray(filename, directory = "./")`

> Given a pair of files with extensions `.chc` and `.chs`, will load these files and return the `Charray` saved in these files.

---

`display_logo(h = None, w = None)`

> Displays the animated termighty logo, and resizes the terminal to `(h,w)`; by default, these dimensions are $24 \times 80$ characters in size.

---

`design_Charray(chars = None, t_colors = None, b_colors = None, styles = None)`

> Creates images from four rectangular shaped strings of equal size, for example:
>
> |`chars`|`t_colors`|`b_colors`|`styles`|
> |---|---|---|---|
> |"ab=<br>&nbsp;&f#<br>&nbsp;g^i"  |"ddd<br>&nbsp;bbb<br>&nbsp;ggg" |"www<br>&nbsp;www<br>&nbsp;www" |"uuu<br>&nbsp;bbb<br>&nbsp;nnn"  |
>
> Each of these strings represents a layer in the output image, which is composed of the characters in `chars`, with the text color given in `t_colors`, on a background whose colors are designated by `b_colors`.  `styles` changes the formatting of each character.
>
> The color and style guide is located in the Appendix.

---

`big_letter(s, t_color = "default", b_color = "default", style = "default")`

> Given a single character `s` of `type<str>` and converts it to an ASCII-art character.  Accepts a letter or a digit, and has optional custom color/style parameters.

---

`big_word(s, t_color = "default", b_color = "default", style = "default")`

> Given an `s` of `type<str>` and converts it to a series of ASCII-art characters using `big_letter(s)` and `hcat(l)`.  Accepts any combination of letters and numbers, and has optional custom color/style parameters.
>
> Note that the optional parameters must be *single characters*; use `design_Charray()` to design more intricate patterns.

---

`hcat(l)`

> Takes a list of`Charray`objects `l` and concatenates them horizontally, returning a new `Charray`object.
>
> Attribute `Charray.h` must be equal in *every* element of `l`.

---

`vcat(l)`

> Takes a list of`Charray`objects `l` and concatenates them vertically, returning a new `Charray`object.
>
> Attribute `Charray.w` must be equal in *every* element of `l`.

---


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
