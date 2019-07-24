# **Termighty**
## A Python-based GUI development package for Ubuntu's Gnome terminal

If you want to create colorful ASCII-art images, animations, and interactive games directly in your Gnome terminal, then **Termighty** is what you are looking for.

This package maps an array of characters and colors to the terminal, giving users a great deal of flexibility in how they choose to develop their own programs.

Termighty features:
* `Char` objects - terminal "pixels" that contain a single character, text color, background color, and style.
* `Charray` objects - arrays of `Char` objects that can be accessed and modified via integer or slice indices.
* `String` objects - subclass of `Charray`; supports a large number of `type<str>` functions.
* `Terminal`objects -  interface that takes over the terminal, and displays `Charray` objects.
* Keypress events - react immediately to users pressing any alphanumeric keys.
* Unit Tests - a robust set of tests allows users to modify Termighty more securely

## Installation
Note: Termighty is designed for the Ubuntu 18.04 LTS Gnome-terminal

In the terminal, run `pip Termighty` to install it

For more information, consult `Handbook.md`
