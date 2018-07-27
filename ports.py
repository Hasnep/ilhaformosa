"""Defining the ports classes"""
from distances import *
from ships import *
from options import *
import random

all_building_types = ["palace", "bank", "shipyard", "market"]


def round_to(x, base=1):
    return int(base * round(float(x) / base))


def random_price(base_price, base=1, sd=None):
    if sd is None:
        sd = base_price/10
    price = None
    while price is None or abs(price - base_price) > 3 * sd or price < base:
        price = random.gauss(base_price, sd)
    return int(round_to(price, base=base))


class Port(object):
    def __init__(self, port_name):
        self.id = port_name.lower().replace(" ", "")
        self.name = port_name
        self.visited = False
        self.discovered = False
        self.distances = ports_distances[self.name]
        self.buildings = []
        for k in all_building_types:
            self.buildings.append(k)
        self.for_sale_ship = None
        self.for_sale_ship_price = 0

    def arrive(self):
        if "shipyard" in self.buildings:
            ship_type_class = random.choice(all_ship_objects)
            self.for_sale_ship = ship_type_class()
            self.for_sale_ship_price = random_price(self.for_sale_ship.value, base=100)

    def remove_for_sale_ship(self):
        self.for_sale_ship = None
        self.for_sale_ship_price = 0


all_ports = [*ports_distances]

world = {port_name.lower().replace(" ", ""): Port(port_name) for port_name in all_ports}  # create port objects for all ports


def id_to_port(port_id, _world=world):
    return _world[port_id]


def port_name_to_id(port_name):
    return port_name.lower().replace(" ", "")


def name_to_port(port_name):
    return id_to_port(port_name_to_id(port_name))
