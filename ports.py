"""Defining the ports classes"""
from buildings import *
from distances import *


class Port(object):
    def __init__(self, port_name):
        self.id = port_name.lower().replace(" ", "")
        self.name = port_name
        self.visited = False
        self.discovered = False
        self.buildings = {}
        self.distances = ports_distances[self.name]
        for key, value in all_building_types.items():
            self.buildings[key] = value(self.name)


all_ports = [*ports_distances]

world = {port_name.lower().replace(" ", ""): Port(port_name) for port_name in all_ports}  # create port objects for all ports


def id_to_port(port_id, _world=world):
    return _world[port_id]


def port_name_to_id(port_name):
    return port_name.lower().replace(" ", "")


def name_to_port(port_name):
    return id_to_port(port_name_to_id(port_name))
