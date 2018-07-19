import os
import random

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
nouns_path = os.path.join(THIS_FOLDER, 'resources/nouns.txt')
with open(nouns_path, "r") as myfile:
    nouns = myfile.read().splitlines()

adjectives_path = os.path.join(THIS_FOLDER, 'resources/adjectives.txt')
with open(adjectives_path, "r") as myfile:
    adjectives = myfile.read().splitlines()


def random_ship_name():
    """A function to generate a random starting name for every ship."""
    name = "The " + random.choice(adjectives) + " " + random.choice(nouns)
    return name
