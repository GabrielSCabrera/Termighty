# Termighty (Pre-Alpha)

## What is Termighty?

Termighty is a python 3.6+ package for high-level terminal interactivity. If your linux-based terminal supports 24-bit true colors, then Termighty can help you to
* Print easily to any point in the terminal.
* Display text and backgrounds – with over 16 million colors to choose from. Select over one-thousand different colors by name, or select an RGB value and design your own colors.
* Easily format text with styles including bold, italic, and underline.

## Getting Started

### Requirements
Depends on package `numpy`, which can be installed with the command `pip3 install numpy`.  

Includes some developer tools that depend on package `tkinter`, which can be installed with the command `sudo apt-get install python3-tk`.

### Setup and Testing
In the terminal
1. Clone this repository with the command `git clone https://github.com/GabrielSCabrera/Termighty.git`.
2. Open the Termighty directory with the command `cd Termighty`.
3. Enter the command `make` to install Termighty in pip3 development mode.
4. (OPTIONAL) Run `make test` to run all unit tests & confirm that there are zero errors.
5. (OPTIONAL) Run `make logo` to view the Termighty logo, which confirms terminal compatibility.
