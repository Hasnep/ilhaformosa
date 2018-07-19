import os
from pyfiglet import Figlet
from math import floor


def title_print():
    """A function that prints the title in a fancy way."""
    title = Figlet(font="script").renderText("Ilha Formosa")
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
        print("=" * title_width + "\n" + title + "=" * title_width)


title_print()
