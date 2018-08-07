"""Defining the ports classes"""
from distances import *
from ships import *
from cargo import *
import random


all_building_types = ["palace", "bank", "shipyard", "market", "moneylender"]


def random_price(base_price: float, base: int=1, sd=None) -> int:
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
        for k in all_building_types:  # TODO: Make the building selection process semi-random using a matrix
            self.buildings.append(k)

        # shipyard
        self.for_sale_ship = None
        self.for_sale_ship_price = 0

        # market
        self.cargo_local_value = {cargo: 0 for cargo in cargo_names}
        self.cargo_price = {cargo: 0 for cargo in cargo_names}

    def arrive(self, n_days: int=100):
        # shipyard
        if "shipyard" in self.buildings:
            ship_type_class = random.choice(all_ship_objects)
            self.for_sale_ship = ship_type_class()
            self.for_sale_ship_price = random_price(self.for_sale_ship.value, base=100)

        # market
        self.cargo_local_value = cargo_randomise_values(self.cargo_local_value, n_days)
        self.cargo_price = cargo_calculate_prices(cargo_global_value, self.cargo_local_value)

    def remove_for_sale_ship(self):
        self.for_sale_ship = None
        self.for_sale_ship_price = 0


all_ports = [*ports_distances]

world = {port_name.lower().replace(" ", ""): Port(port_name) for port_name in all_ports}  # create port objects for all ports


def id_to_port(port_id: str, _world=world) -> Port:
    return _world[port_id]


def port_name_to_id(port_name: str) -> str:
    return port_name.lower().replace(" ", "")


def name_to_port(port_name: str) -> Port:
    return id_to_port(port_name_to_id(port_name))
