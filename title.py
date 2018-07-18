import os
from pyfiglet import Figlet
import math


def print_title():
    terminal_width = os.get_terminal_size()[0]
    title = Figlet(font='script').renderText('Ilha Formosa')
    title_width = len(title.split("\n", 1)[0])
    n_blanks = math.floor((terminal_width - title_width)/2)
    blanks = " " * n_blanks
    title = blanks + title
    title = title.replace("\n", "\n" + blanks)
    title = title.replace(" " * title_width + "\n", "")
    print("=" * terminal_width + title + "\n" + "=" * terminal_width)

try:
    print_title()
except:
    print("Ilha Formosa!")
