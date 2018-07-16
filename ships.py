"""Defining the ships classes"""


def random_ship_name():
    """A function to generate a random starting name for every ship."""
    return "Seven"


class Ship(object):
    nickname = random_ship_name()

    def __init__(self):
        self.information = "Name: %s\nType: %s\nHealth: ?/%s\nCargo: ?/%s\n" % (self.nickname, self.type, self.maxHealth, self.capacity)


class Junk(Ship):
    def __init__(self):
        self.type = "Junk"
        self.description = "A standard ship."
        self.maxHealth = 50
        self.capacity = 30
        Ship.__init__(self)


class Baochuan(Ship):
    def __init__(self):
        self.type = "Baochuan"
        self.description = "A cargo ship."
        self.maxHealth = 60
        self.capacity = 100
        Ship.__init__(self)
