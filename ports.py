"""Defining the ports classes"""
from buildings import *
import random

class Port(object):
    def __init__(self, name):
        self.name = name
        self.landing_message = "You land in %s" % name
        self.description = "%s is a port" % self.name
        self.buildings = []
        for k in all_building_types:
            if random.uniform(0, 1) > 0.5:
                self.buildings.append(k(self.name))


all_ports = ["taipei", "shanghai", "tokyo"]

world = {k: Port(k.title()) for k in all_ports}