import random
import math
from options import *


def money(amount: int) -> str:
    """A function to add the currency symbol to money."""
    # TODO: Add commas to currency.
    currency_option = options.get_option("currency")
    if currency_option == "pound":
        symbol = "£"
    elif currency_option == "dollar":
        symbol = "$"
    else:
        symbol = "?"
    return symbol + str(int(math.floor(amount)))


def weight(weight_amount: int) -> str:
    return str(weight_amount) + options.get_option("weight")


def price_per_weight(price_amount: int) -> str:
    return money(price_amount) + "/" + options.get_option("weight")


cargo_names = ["tea", "silk", "porcelain", "jade"]
cargo_base_price = {"tea": 10, "silk": 20, "porcelain": 30, "jade": 40}
cargo_global_value = {cargo: 0 for cargo in cargo_names}
cargo_volatility = 10
cargo_control = 10
cargo_variability = 0.5


def round_to(x: float, base: int=1) -> int:
    return int(base * round(float(x) / base))


def cargo_calculate_prices(global_value: dict, local_value: dict, _cargo_names=cargo_names, base_price=cargo_base_price, volatility=cargo_volatility) -> dict:
    cargo_prices = {cargo_name: None for cargo_name in _cargo_names}
    for cargo_name in _cargo_names:
        cargo_prices[cargo_name] = round_to(base_price[cargo_name] * (1 + volatility/1000) ** (global_value[cargo_name] + local_value[cargo_name]))
    return cargo_prices


def invlogit(x: float, _control=cargo_control):
    return math.exp(x/_control)/(1 + math.exp(x/_control))


def cargo_randomise_values(base_values: dict, n_days: int, _control=cargo_control, _variability=cargo_variability, _cargo_names=cargo_names) -> dict:
    cargo_values = {cargo_name: None for cargo_name in _cargo_names}
    for cargo_type, value_start in base_values.items():
        this_cargos_value = value_start
        for day in range(n_days):
            if random.random() > invlogit(this_cargos_value):
                this_cargos_value += 1
            else:
                this_cargos_value -= 1
            this_cargos_value += random.gauss(0, _variability)
        cargo_values[cargo_type] = this_cargos_value
    return cargo_values


def table_cargo_prices(cargo_prices: dict, cargo_owned: dict, cargo_bought_for: dict, _cargo_names=cargo_names):
    for cargo_type in _cargo_names:
        print(
            cargo_type
            + " " * (1 + len(max(cargo_names, key=len)) - len(cargo_type))
            + " " * (len(max([str(value) for key, value in cargo_prices.items()], key=len)) - len(str(cargo_prices[cargo_type])))
            + price_per_weight(cargo_prices[cargo_type])
            + " " * (1 + len(max([str(value) for key, value in cargo_owned.items()], key=len)) - len(str(cargo_owned[cargo_type])))
            + weight(cargo_owned[cargo_type])
        )
