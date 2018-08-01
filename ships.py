"""Define the ships classes."""
from randomwords import *


def print_ship_information(ship):
    """A function that prints a ship's stats."""
    print("Name: " + ship.nickname)
    print("Type: " + ship.type)
    print("Description: " + ship.description)
    print("Health: " + str(ship.health) + "/" + str(ship.max_health))
    print("Cannons: " + str(ship.cannons) + "/" + str(ship.max_cannons))
    print("Max cargo: " + str(ship.cargo_capacity))


class Ship(object):
    max_health = 0

    def __init__(self):
        self.nickname = random_ship_name()
        self.health = self.max_health
        self.cannons = 0  # TODO: Add cannons


class Junk(Ship):
    def __init__(self):
        self.type = "junk"
        self.description = "A standard ship."
        self.max_health = 50
        self.max_cannons = 10
        self.cargo_capacity = 30
        self.top_speed = 8
        self.value = 3000
        Ship.__init__(self)


class Baochuan(Ship):
    def __init__(self):
        self.type = "baochuan"
        self.description = "A cargo ship."
        self.max_health = 60
        self.max_cannons = 5
        self.cargo_capacity = 100
        self.top_speed = 7
        self.value = 4500
        Ship.__init__(self)


all_ship_objects = [Junk, Baochuan]
all_ship_types = ["junk", "baochuan"]  # TODO: Figure out how to get default values for a class in a loop
