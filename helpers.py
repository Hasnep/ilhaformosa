import math
import random
import datetime

from options import *


# Functions to add units
def apply_units(input_object: [int, float, str, list, dict], function_one) -> [str, list, dict]:
    """Apply a unit adding function to a single object or a list of objects."""
    if type(input_object) is int or type(input_object) is float:
        return function_one(input_object)
    elif type(input_object) is str:
        return function_one(int(input_object))
    elif type(input_object) is list:
        return [function_one(x) for x in input_object]
    elif type(input_object) is dict:
        return {key: function_one(value) for key, value in input_object.items()}
    else:
        raise ValueError("Invalid input type.")


def _commas_one(input_number: int) -> str:
    """Add commas to a single integer."""
    input_as_string = str(input_number)
    digits_list = []
    while len(input_as_string) > 0:
        digits_list.insert(0, input_as_string[-3:])
        input_as_string = input_as_string[:-3]
    output_string = ",".join(digits_list)
    return output_string


def commas(input_object: [int, list, dict]) -> [str, list, dict]:
    """Add commas to a single number or list of numbers"""
    return apply_units(input_object, _commas_one)


def _money_one(input_number: int) -> str:
    """Add the currency symbol to a single number."""
    currency_option = options.get_option("currency")
    if currency_option == "pound":
        currency_symbol = "£"
    elif currency_option == "dollar":
        currency_symbol = "$"
    else:
        currency_symbol = "?"
    return currency_symbol + _commas_one(input_number)


def money(input_object: [int, list, dict]) -> [str, list, dict]:
    """Add the currency symbol to a single number or list of numbers."""
    return apply_units(input_object, _money_one)


def _weight_one(input_number: int) -> str:
    """Add the weight symbol to a single number."""
    return _commas_one(input_number) + options.get_option("weight")


def weight(input_object: [int, list, dict]) -> [str, list, dict]:
    """Add the weight symbol to a single number or list of numbers."""
    return apply_units(input_object, _weight_one)


def _price_per_weight_one(input_number: int) -> str:
    """Add the currency and weight symbols to a single number."""
    return _money_one(input_number) + "/" + options.get_option("weight")


def price_per_weight(input_object: [int, list, dict]) -> [str, list, dict]:
    """Add the currency and weight symbols to a single number or list of numbers."""
    return apply_units(input_object, _price_per_weight_one)


def _percent_one(input_number: [float, int]) -> str:
    """A function to convert a decimal to a percentage string."""
    return str(int(math.floor(100 * input_number))) + "%"


def percent(input_object: [float, int, list, dict]) -> [str, list, dict]:
    """A function to convert a decimal or list of decimals to a percentage string."""
    return apply_units(input_object, _percent_one)


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


# Aligning text
def blanks(n_spaces: int) -> str:
    return " " * n_spaces


def align_text(text: str, max_width: int, align: str="l") -> str:
    padding_n = max_width - len(text)
    if align == "l":
        return text + blanks(padding_n)
    elif align == "r":
        return blanks(padding_n) + text
    elif align == "c":
        if padding_n % 2 == 1:
            extra_space = 1
        else:
            extra_space = 0
        padding_n = math.floor(padding_n/2)
        return blanks(padding_n) + text + blanks(padding_n + extra_space)


def table_aligned_print(column_names: list, column_aligns: list, row_keys: list, column_dicts: list, show_row_keys: bool=True) -> None:  # TODO: add option to not print header
    max_column_widths = []
    for column_index, column_dict in enumerate(column_dicts):

        if not (len(column_dict) == len(row_keys)):
            raise ValueError("Column {}'s dict is the wrong length.".format(column_index))

        for key in column_dict:
            if key not in row_keys:
                raise ValueError("Key '{}' not in list of keys.".format(key))

        max_variable_width = max([len(value) for key, value in column_dict.items()])
        max_column_widths.append(max(max_variable_width, len(column_names[column_index])))

    if show_row_keys:
        keys_column_width = max([len(key) for key in row_keys])
        text = blanks(keys_column_width + 1)
    else:
        keys_column_width = 0
        text = ""

    # print the header row
    for column_index, column_name in enumerate(column_names):
        text += align_text(column_name, max_column_widths[column_index], "l") + blanks(1)
    print("".join(text))

    for key_index, key in enumerate(row_keys):
        if show_row_keys:
            text = align_text(key, keys_column_width, align="l") + blanks(1)
        else:
            text = ""
        for column_index, column_dict in enumerate(column_dicts):
            text += align_text(column_dict[key], max_column_widths[column_index], column_aligns[column_index]) + blanks(1)
        print("".join(text))

    return
