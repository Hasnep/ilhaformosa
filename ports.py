from cargo import *
from distances import *

all_building_types = ["palace", "bank", "shipyard", "market", "moneylender"]


class Port(object):
    def __init__(self, port_name):
        self.id = port_name.lower().replace(" ", "")
        self.name = port_name
        self.last_visited = None
        self.discovered = False
        self.buildings = []
        for k in all_building_types:  # TODO: Make the building selection process semi-random using a matrix
            self.buildings.append(k)

        # shipyard
        self.for_sale_ship = None
        self.for_sale_ship_price = 0

        # market
        self.local_values = {cargo_type: 0 for cargo_type in cargo.types}
        self.local_prices = cargo.calculate_prices(self.local_values)

    def remove_for_sale_ship(self):
        self.for_sale_ship = None
        self.for_sale_ship_price = 0


all_ports = [*ports_distances]

world = {port_name.lower().replace(" ", ""): Port(port_name) for port_name in all_ports}  # create port objects for all ports


# helper functions
def id_to_port(port_id: str, _world=world) -> Port:
    return _world[port_id]


def port_name_to_id(port_name: str) -> str:
    return port_name.lower().replace(" ", "")


def name_to_port(port_name: str) -> Port:
    return id_to_port(port_name_to_id(port_name))
