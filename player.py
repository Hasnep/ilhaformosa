"""Initialises information about the player and creates helper functions about time."""
import datetime
from ports import *


class Player(object):
    """Define the player class."""
    def __init__(self):
        # money related variables
        self.cash = 1000
        self.balance = 0
        self.debt = 0
        self.bank_rate = 0.1  # bank interest rate per year
        self.lend_rate = 0.2  # moneylender interest rate per year

        # time related variables
        self.day = 0

        # location related variables
        self.location = world["taipei"]
        self.building = None

        # fleet related variables
        self.fleet = [Junk()]

    def set_location(self, location_string):
        """Sets the location of the player to the string."""
        self.location = world[location_string]

    def day_increase(self, increase_by):
        """Increase the time by a certain number of days"""
        self.day = self.day + increase_by

    def leave_building(self):
        """Make the player leave whatever building they are in."""
        self.building = None

    def cash_increase(self, increase_by):
        """Increase the player's cash."""
        self.cash = self.cash + increase_by

    def cash_decrease(self, decrease_by):
        """Decrease the player's cash. Calls cash_increase()."""
        self.cash_increase(-decrease_by)

    # TODO: add function to rename ship?


player = Player()  # Initialise the player object

start_date = datetime.date(1700, 1, 1)


def day_to_date(x):
    """Convert the number of days to a readable string."""
    x = start_date + datetime.timedelta(days=x)
    if options["date"] == "ymd":
        x = x.strftime("%Y-%m-%d")
    elif options["date"] == "dmy":
        x = x.strftime("%d/%m/%Y")
    return x
