"""Initialises information about the player and creates helper functions about time."""
import datetime
from ports import *


def compound_interest(principal_amount, interest_rate, days_passed):
    return principal_amount * (1 + interest_rate)**(days_passed/365)


class Player(object):
    """Define the player class."""
    def __init__(self):
        # money related variables
        self.cash = 1000
        self.balance = 0
        self.debt = 0
        self.bank_rate = 0.10  # bank interest rate per year
        self.lend_rate = 0.20  # moneylender interest rate per year

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
        self.balance = compound_interest(self.balance, self.bank_rate, increase_by)
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

    def balance_increase(self, increase_by):
        """Increase the player's bank balance."""
        self.balance = self.balance + increase_by

    def balance_decrease(self, decrease_by):
        """Decrease the player's bank balance. Calls balance_increase()."""
        self.balance_increase(-decrease_by)

    def deposit_cash(self, deposit_amount):
        """Deposit money into the bank."""
        self.cash_decrease(deposit_amount)
        self.balance_increase(deposit_amount)

    def withdraw_cash(self, withdraw_amount):
        """Withdraw money from the bank."""
        self.cash_increase(withdraw_amount)
        self.balance_decrease(withdraw_amount)

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
