"""Initialises information about the player and creates helper functions about money and time."""
import datetime
from options import *
from ports import *

player = {"cash": 1000,
          "balance": 0,
          "debt": 0,
          "day": 0,
          "location": world["taipei"],
          "fleet": [Junk()]
          }

start_date = datetime.date(1700, 1, 1)


def money(amount):
    """A function to add the currency symbol to money."""
    return options["currency"] + " " + amount


def day_to_date(x):
    """Convert the number of days to a readable string."""
    x = start_date + datetime.timedelta(days=x)
    if options['date'] == "ymd":
        x = x.strftime("%Y-%m-%d")
    elif options['date'] == "dmy":
        x = x.strftime("%d/%m/%Y")
    return x


def day_increase(x):
    """Increase the time by a certain number of days"""
    player["day"] = player["day"] + x


def rename_ship(old_nickname, new_nickname):
    """A function that changes the nickname of a ship."""
    for k in player["fleet"]:
        if k.nickname == old_nickname:
            k.nickname = new_nickname