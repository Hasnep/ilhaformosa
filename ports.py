"""Defining the ports classes"""
from buildings import *
from distances import *


class Port(object):
    def __init__(self, port_name):
        self.name = port_name
        self.visited = False
        self.discovered = False
        self.buildings = {}
        self.distances = ports_distances[self.name]
        for key, value in all_building_types.items():
            self.buildings[key] = value(self.name)


all_ports = [*ports_distances]

# TODO: Change world dict into a class.
world = {k.lower().replace(" ", ""): Port(k) for k in all_ports}  # create port objects for all ports
