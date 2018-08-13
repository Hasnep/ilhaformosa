import math
import random
import datetime

from options import *


# Functions to add units
def commas(amount_int: int) -> str:
    amount_str = str(amount_int)
    amount_list = []
    while len(amount_str) > 0:
        amount_list.insert(0, amount_str[-3:])
        amount_str = amount_str[:-3]
    amount_str = ",".join(amount_list)
    return amount_str


def money(amount_int: int) -> str:
    """Add the currency symbol to a number."""
    amount_str = commas(amount_int)
    currency_option = options.get_option("currency")
    if currency_option == "pound":
        symbol = "£"
    elif currency_option == "dollar":
        symbol = "$"
    else:
        symbol = "?"
    return symbol + amount_str


def weight(weight_amount: int) -> str:
    return commas(weight_amount) + options.get_option("weight")


def price_per_weight(price_amount: int) -> str:
    return money(price_amount) + "/" + options.get_option("weight")


def percent(decimal: float) -> str:
    """A function to convert a decimal to a percentage string."""
    return str(int(math.floor(100 * decimal))) + "%"


# Money
def compound_interest(principal_amount: int, interest_rate: float, days_passed: int) -> int:
    return int(math.floor(principal_amount * (1 + interest_rate)**(days_passed/365)))


def round_to(x: float, base: int=1) -> int:
    return int(base * round(float(x) / base))


def random_price(base_price: float, base: int=1, sd=None) -> int:
    if sd is None:
        sd = base_price/10
    price = None
    while price is None or abs(price - base_price) > 3 * sd or price < base:
        price = random.gauss(base_price, sd)
    return int(round_to(price, base=base))


# Dates
def day_to_date(n_days_passed: int, _start_date: datetime.date=datetime.date(1700, 1, 1)) -> str:
    """Convert the number of days to a readable string."""
    date_as_date = _start_date + datetime.timedelta(days=n_days_passed)
    if options.get_option("date") == "ymd":
        date_as_string = date_as_date.strftime("%Y-%m-%d")
    elif options.get_option("date") == "dmy":
        date_as_string = date_as_date.strftime("%d/%m/%Y")
    else:
        raise ValueError("Invalid option selected for 'date'.")
    return date_as_string


# Parsing arguments
def split_args(input_string: str) -> list:
    if input_string == "":
        return []
    else:
        output_list = input_string.lower().split()
        if input_string[-1] == " ":
            output_list.append("")
    return output_list


def format_arg(input_string):
    input_string = input_string.lower()
    input_string = input_string.replace(" ", "")
    return input_string
