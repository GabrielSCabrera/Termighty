import numpy as np
import argparse

# import termios
import time
import sys

# import tty
import os

from termutils import *

globals()["status_entries"] = []


def parse_args():

    argparse_desc = "Cross-platform utilities for displaying complex text in a Terminal"
    help_color = "A sample of class Color showcasing its usage."
    help_string = "A sample of class String displaying its abilities."
    help_live_menu = "A sample of class LiveMenu presenting a few of its uses."
    help_word_processor = "A word processing class that can be used to interpret keyboard input within a text box."

    parser = argparse.ArgumentParser(description=argparse_desc)

    parser.add_argument("--unit-tests", action="store_true", help="Runs all unit tests")
    parser.add_argument("--test", action="store_true", help="Runs the latest test script")
    parser.add_argument("--color", action="store_true", help=help_color)
    parser.add_argument("--string", action="store_true", help=help_string)
    parser.add_argument("--live-menu", action="store_true", help=help_live_menu)
    parser.add_argument("--word-processor", action="store_true", help=help_word_processor)

    return parser.parse_args()


def update_status(new_entry):
    tab_len = len("Prev. Selections:") + 7
    tot_len = tab_len
    max_len = 80
    for entry in globals()["status_entries"]:
        if entry == "<newline>":
            continue
        elif tot_len + len(entry) + 3 >= max_len:
            tot_len = tab_len + len(entry) + 3
        else:
            tot_len += len(entry) + 3
    if tot_len + len(new_entry) >= max_len:
        globals()["status_entries"].append("<newline>")
    globals()["status_entries"].append(new_entry)


def display_status():
    tab_len = len("Prev. Selections:") + 7
    status = text.bold("Prev. Selections:") + " " * 7
    for n, entry in enumerate(globals()["status_entries"]):
        if entry == "<newline>":
            status += "\n" + " " * tab_len
        elif n == len(globals()["status_entries"]) - 1:
            status += f"{text.italic(entry)}"
        else:
            status += f"{text.italic(entry)} > "
    return status + "\n"


"""SCRIPT PROCEDURES"""


def procedure_color():
    color = Color((255, 255, 255))
    print(Color.list_colors())


def procedure_string():
    string = String("test", "yellow", "turquoise")
    print(string)


def procedure_live_menu():
    live_menu = LiveMenu()
    live_menu.start()
    live_menu.stop()


def procedure_word_processor():
    text_editor = WordProcessor()
    text_editor.start()
    text_editor.stop()


"""MAIN SCRIPT"""

args = parse_args()

if args.unit_tests is True:
    tests.run_all()

if args.test is True:

    print("No tests at the moment")

if args.color is True:
    procedure_color()

if args.string is True:
    procedure_string()

if args.live_menu is True:
    procedure_live_menu()

if args.word_processor is True:
    procedure_word_processor()
