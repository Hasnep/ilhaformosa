"""Defining the ports classes"""
from buildings import *


class Port(object):
    def __init__(self, name):
        self.name = name
        self.landing_message = "You land in %s" % name
        self.description = "%s is a port" % self.name
        self.buildings = []
        for k in all_building_types:
            self.buildings.append(k(self.name))


all_ports = ["taipei", "shanghai", "tokyo"]

world = {k: Port(k.title()) for k in all_ports}