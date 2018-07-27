import os
from pyfiglet import Figlet
from math import floor

version_number = "v0.1.090"

# TODO: Make some sort of system for integrating ascii art with text.

def title_print():
    """A function that prints the title in a fancy way."""
    global version_number
    try:
        title = Figlet(font="script").renderText("Ilha Formosa")  # TODO: Make the title using an online generator and put into the script as a string.
        title_width = len(title.split("\n", 1)[0])
        try:
            terminal_width = os.get_terminal_size()[0]
            n_blanks = floor((terminal_width - title_width) / 2)
            blanks = " " * n_blanks
            title = blanks + title
            title = title.replace("\n", "\n" + blanks)
            title = title.replace(" " * title_width + "\n", "")
            print("=" * terminal_width + title + "\n" + "=" * terminal_width)
        except:
            title = title.replace(" " * title_width + "\n", "")
            title = title + " " * title_width + "\n"
            print("=" * title_width + "\n" + title + "=" * title_width)
        print(version_number)
    except:
        print("Ilha Formosa! - " + version_number)


title_print()
