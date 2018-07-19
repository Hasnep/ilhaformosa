"""Defining the buildings classes"""
from ships import *

def building_namer(type, location):
    """Helper function for generating building names."""
    name = "%s %s" % (location, type)
    name.title()
    return name


class Building(object):
    type = "Building"

    def __init__(self, location):
        self.location = location
        self.name = building_namer(self.type, self.location)
        self.description = "%s is a %s in %s" % (self.name, self.type, self.location)


class Palace(Building):
    def __init__(self, location):
        self.type = "Palace"
        self.description = "A super fancy building."
        Building.__init__(self, location)


class Bank(Building):
    def __init__(self, location):
        self.type = "Bank"
        self.description = "Money is here."
        Building.__init__(self, location)


class Shipyard(Building):
    def __init__(self, location):
        self.type = "Shipyard"
        self.description = "Where you can buy ships."
        Building.__init__(self, location)


all_building_types = [Palace, Bank, Shipyard]
