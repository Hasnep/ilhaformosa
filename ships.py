"""Defining the ships classes"""


def random_ship_name():
    return "seven"


class Ship(object):
    nickname = random_ship_name()

    def __init__(self):
        self.description = "'%s' is a %s with max health %s and capacity %s" % (self.nickname, self.type, self.maxHealth, self.capacity)


class Junk(Ship):
    def __init__(self):
        self.type = "Junk"
        self.maxHealth = 50
        self.capacity = 30
        Ship.__init__(self)


class Baochuan(Ship):
    def __init__(self):
        self.type = "Baochuan"
        self.maxHealth = 60
        self.capacity = 100
        Ship.__init__(self)
