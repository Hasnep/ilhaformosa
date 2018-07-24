"""Defining the ships classes"""
from randomwords import *


def print_ship_information(ship):
    """A function that prints a ship's stats."""
    print("Name: " + ship.nickname)
    print("Type: " + ship.type)
    print("Description: " + ship.description)
    print("Health: " + str(ship.health) + "/" + str(ship.maxHealth))
    print("Cannons: " + str(ship.cannons) + "/" + str(ship.maxCannons))
    print("Cargo: " + "?/" + str(ship.cargoCapacity))


class Ship(object):
    maxHealth = 0

    def __init__(self):
        self.nickname = random_ship_name()
        self.health = self.maxHealth
        self.cargo = []
        self.cannons = 0


class Junk(Ship):
    def __init__(self):
        self.type = "Junk"
        self.description = "A standard ship."
        self.maxHealth = 50
        self.maxCannons = 10
        self.cargoCapacity = 30
        self.topSpeed = 8
        self.value = 300
        Ship.__init__(self)


class Baochuan(Ship):
    def __init__(self):
        self.type = "Baochuan"
        self.description = "A cargo ship."
        self.maxHealth = 60
        self.maxCannons = 5
        self.cargoCapacity = 100
        self.topSpeed = 7
        self.value = 400
        Ship.__init__(self)


all_ship_types = [Junk, Baochuan]
