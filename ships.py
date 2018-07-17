"""Defining the ships classes"""


def random_ship_name():
    """A function to generate a random starting name for every ship."""
    return "Seven"


class Ship(object):
    nickname = random_ship_name()

    def __init__(self):
        self.health = self.maxHealth
        self.cargo = []
        self.cannons = 0
        self.information = "Name: %s\nType: %s\nHealth: %s/%s\nCannons: %s/%s\nCargo: ?/%s\n" % (self.nickname, self.type, self.health, self.maxHealth, self.cannons, self.maxCannons, self.cargoCapacity)


class Junk(Ship):
    def __init__(self):
        self.type = "Junk"
        self.description = "A standard ship."
        self.maxHealth = 50
        self.maxCannons = 10
        self.cargoCapacity = 30
        Ship.__init__(self)


class Baochuan(Ship):
    def __init__(self):
        self.type = "Baochuan"
        self.description = "A cargo ship."
        self.maxHealth = 60
        self.maxCannons = 5
        self.cargoCapacity = 100
        Ship.__init__(self)
