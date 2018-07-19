"""Defining the ships classes"""


def random_ship_name():
    """A function to generate a random starting name for every ship."""
    return "Seven"


def print_ship_information(ship):
    """A function that prints a ship's stats."""
    print("Name: %s\nType: %s\nHealth: %s/%s\nCannons: %s/%s\nCargo: ?/%s\n" % (ship.nickname, ship.type, ship.health, ship.maxHealth, ship.cannons, ship.maxCannons, ship.cargoCapacity))


class Ship(object):
    nickname = random_ship_name()

    def __init__(self):
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
        Ship.__init__(self)


class Baochuan(Ship):
    def __init__(self):
        self.type = "Baochuan"
        self.description = "A cargo ship."
        self.maxHealth = 60
        self.maxCannons = 5
        self.cargoCapacity = 100
        self.topSpeed = 7
        Ship.__init__(self)
