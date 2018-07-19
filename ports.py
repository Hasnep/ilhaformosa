"""Defining the ports classes"""
from buildings import *
from distances import *


class Port(object):
    def __init__(self, port_name):
        self.name = port_name
        self.landing_message = "You land in %s" % self.name
        self.description = "%s is a port" % self.name
        self.visited = False
        self.discovered = False
        self.buildings = []
        self.distances = ports_distances[self.name]
        for k in all_building_types:
            self.buildings.append(k(self.name))


all_ports = ["Hong Kong", "Incheon", "Naha", "Shanghai", "Taipei", "Tianjin", "Tokyo"]

world = {k.lower().replace(" ", ""): Port(k) for k in all_ports}  # create port objects for all ports
