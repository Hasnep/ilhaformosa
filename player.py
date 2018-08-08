"""Initialises information about the player and creates helper functions about time."""
import datetime
import math
from ports import *
from options import *





def percent(decimal: float) -> str:
    """A function to convert a decimal to a percentage string."""
    return str(int(math.floor(100 * decimal))) + "%"


def compound_interest(principal_amount: int, interest_rate: float, days_passed: int) -> int:
    return int(math.floor(principal_amount * (1 + interest_rate)**(days_passed/365)))

# TODO: Allow the player to select different starting ports.


class Player(object):
    """Define the player class."""
    def __init__(self):
        # money related variables
        self._cash = 9000
        self._balance = 1000
        self.bank_rate = 0.10  # bank interest rate per year
        self._debt = 50
        self.lend_rate = 0.20  # moneylender interest rate per year
        self.borrow_limit_multiplier = 1.5

        # time related variables
        self._day = 0

        # fleet related variables
        self.fleet = [Junk()]
        self.cargo = {cargo_type: 0 for cargo_type in cargo.types}

        # location related variables
        self._location = world["taipei"]
        self.location.arrive()

    # location property
    @property
    def location(self) -> Port:
        return self._location

    @location.setter
    def location(self, port_name: str):
        """Sets the location of the player to the port with the name provided."""
        self._location = world[port_name]

    # day property
    @property
    def day(self) -> int:
        return self._day

    @day.setter
    def day(self, change_day_to: int):
        try:
            change_day_to = int(math.ceil(float(change_day_to)))
        except TypeError:
            print("Cannot set day to %s." % change_day_to)
        else:
            change_day_by = change_day_to - self._day
            if change_day_by > 0:
                if self.balance > 0:
                    self.balance = compound_interest(self.balance, self.bank_rate, change_day_by)
                if self.debt > 0:
                    self.debt = compound_interest(self.debt, self.lend_rate, change_day_by)
                self._day = change_day_to
                return
            elif change_day_by < 0:
                print("Cannot go back in time.")
                return
            else:
                print("Date not changed.")
                return

    # money properties
    @property
    def cash(self) -> int:
        return self._cash

    @cash.setter
    def cash(self, set_cash_to: int):
        if set_cash_to < 0:
            print("Cannot set cash to less than 0.")
            return
        else:
            self._cash = set_cash_to
            return

    @property
    def balance(self) -> int:
        return self._balance

    @balance.setter
    def balance(self, set_balance_to: int):
        if set_balance_to < 0:
            print("Cannot set bank balance to less than 0.")
            return
        else:
            self._balance = set_balance_to
            return

    @property
    def debt(self) -> int:
        return self._debt

    @debt.setter
    def debt(self, set_debt_to: int):
        if set_debt_to < 0:
            print("Cannot set debt to less than 0.")
            return
        else:
            self._debt = set_debt_to
            return

    @property
    def total_money(self) -> int:
        """Returns the player's cash and bank balance minus their debts."""
        return self.cash + self.balance - self.debt

    @property
    def max_debt(self) -> int:
        """Returns the maximum amount of money the player can borrow."""
        return int(math.floor(self.total_money * self.borrow_limit_multiplier))

    # money related functions
    def move_cash(self, action_amount: int, action: str):
        """General function to move money into or out of the bank."""
        if action_amount < 0:
            print("You cannot %s a negative amount." % action)
            return
        elif action_amount == 0:
            print("You cannot %s nothing." % action)
            return
        else:
            if action == "deposit":
                if action_amount > self.cash:
                    print("You do not have enough money to deposit %s. You only have %s." % (money(action_amount), money(self.cash)))
                    return
                else:
                    self.balance += action_amount
                    self.cash -= action_amount
                    print("You deposit %s into the bank." % money(action_amount))
            elif action == "withdraw":
                if action_amount > self.balance:
                    print("You do not have enough money in the bank to withdraw %s. You only have %s." % (money(action_amount), money(self.balance)))
                    return
                else:
                    self.cash += action_amount
                    self.balance -= action_amount
                    print("You withdraw %s from the bank." % money(action_amount))
            elif action == "borrow":
                if player.debt + action_amount > self.max_debt:
                    print("You cannot borrow more than %s at a time." % (money(self.max_debt)))
                    return
                else:
                    self.cash += action_amount
                    self.debt += action_amount
                    print("You borrow %s from the moneylender." % money(action_amount))
            elif action == "repay":
                if self.debt == 0:
                    print("You have no debt to repay.")
                    return
                if action_amount > self.cash:
                    print("You do not have enough money to repay %s of debt. You only have %s." % (money(action_amount), money(self.cash)))
                    return
                elif action_amount > self.debt:
                    print("You cannot repay more money than you have debt. You have %s of debt." % money(self.debt))
                    return
                else:
                    self.cash -= action_amount
                    self.debt -= action_amount
                    print("You repay %s to the moneylender." % money(action_amount))
            else:
                print("None of deposit, withdraw, borrow or repay specified.")
                return

    # cargo related functions
    def get_cargo_weight(self, cargo_type=None) -> int:
        cargo_weight = 0
        for key, value in self.cargo.items():
            if cargo_type is None or key == cargo_type:
                cargo_weight += value
        return cargo_weight

    def set_cargo_quantity(self, cargo_type: str, quantity: int):
        if self.get_cargo_weight() + quantity > self.get_cargo_capacity():
            print("Your fleet can only hold %s." % weight(self.get_cargo_capacity()))
        else:
            self.cargo[cargo_type] = quantity
        return

    def get_cargo_capacity(self) -> int:
        combined_cargo_capacity = 0
        for ship in self.fleet:
            combined_cargo_capacity += ship.cargo_capacity
        return combined_cargo_capacity


player = Player()  # Initialise the player object

start_date = datetime.date(1700, 1, 1)


def day_to_date(x: int) -> str:
    """Convert the number of days to a readable string."""
    x = start_date + datetime.timedelta(days=x)
    if options.get_option("date") == "ymd":
        x = x.strftime("%Y-%m-%d")
    elif options.get_option("date") == "dmy":
        x = x.strftime("%d/%m/%Y")
    return x
