"""Defining the ports classes"""
from buildings import *


class Port(object):
    def __init__(self, name):
        self.name = name
        self.landing_message = "You land in %s" % name
        self.description = "%s is a port" % self.name
        self.visited = False
        self.discovered = False
        self.buildings = []
        for k in all_building_types:
            self.buildings.append(k(self.name))


all_ports = ["taipei", "shanghai", "tokyo"]

# TODO: add distances
# ports_distances = {}
# for city1, cords1 in cords.items():
#     ports_distances[city1] = {}
#     for city2, cords2 in cords.items():
#         ports_distances[city1][city2] = dist(cords1, cords2)


world = {k: Port(k.title()) for k in all_ports}  # create port objects for all ports