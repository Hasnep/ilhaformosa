"""Defining the buildings classes"""
from ships import *
from options import *


def money(amount):
    """A function to add the currency symbol to money."""
    # TODO: Add commas to currency.
    currency_option = options["currency"]
    if currency_option == "pound":
        symbol = "£"
    elif currency_option == "dollar":
        symbol = "$"
    return symbol + str(amount)


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
        self.wares = None


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

        self.sale_price = None

    def reset_wares(self):
        ship_type_class = random.choice(all_ship_types)
        self.wares = ship_type_class()
        self.sale_price = self.wares.value * (1 + random.gauss(0, 0.1))

    def print_wares(self):
        print("Price: %s" % money(self.sale_price))
        print_ship_information(self.wares)

    def enter_building(self):
        self.reset_wares()
        self.print_wares()


all_building_types = {"palace": Palace, "bank": Bank, "shipyard": Shipyard}
