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
    if options.get_option("commas") == "on":
        input_as_string = str(input_number)
        digits_list = []
        while len(input_as_string) > 0:
            digits_list.insert(0, input_as_string[-3:])
            input_as_string = input_as_string[:-3]
        output_string = ",".join(digits_list)
        return output_string
    else:
        return str(input_number)


def commas(input_object: [int, list, dict]) -> [str, list, dict]:
    """Add commas to a single number or list of numbers"""
    return apply_units(input_object, _commas_one)


def _money_one(input_number: int) -> str:
    """Add the currency symbol to a single number."""
    currency_option = options.get_option("currency")
    if currency_option == "pound":
        return "£" + _commas_one(input_number)
    elif currency_option == "dollar":
        return "$" + _commas_one(input_number)
    elif currency_option == "gold":
        return _commas_one(input_number) + " gold"
    elif currency_option == "doubloon":
        return _commas_one(input_number) + " doubloon" + "s" * (input_number != 1)
    else:
        raise ValueError("Invalid currency option.")


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


def table_aligned_print(column_names: list, column_aligns: list, row_keys: list, column_dicts: list, show_header: bool = True, show_row_keys: bool=True) -> None:
    max_column_widths = []
    for column_index, column_dict in enumerate(column_dicts):

        if not (len(column_dict) == len(row_keys)):
            raise ValueError("Column {}'s dict is the wrong length.".format(column_index))

        for key in column_dict:
            if key not in row_keys:
                raise ValueError("Key '{}' not in list of keys.".format(key))

        max_variable_width = max([len(value) for key, value in column_dict.items()])
        if show_header:
            max_column_widths.append(max(max_variable_width, len(column_names[column_index])))
        else:
            max_column_widths.append(max_variable_width)
    if show_row_keys:
        keys_column_width = max([len(key) for key in row_keys])
        text = blanks(keys_column_width + 1)
    else:
        keys_column_width = 0
        text = ""

    # print the header row
    if show_header:
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


def bar(value: int, out_of: int, units = str, label: str="", total_length: int=25) -> None:
    if value < 0:
        value = 0
    elif value > out_of:
        value = out_of
    bar_length = round_to(total_length * (value/out_of))
    blank_length = total_length - bar_length
    print(label + " |" + "=" * bar_length + blanks(blank_length) + "| " + str(value) + "/" + units(out_of))


# Input validation
def syntax_checker(command_syntax) -> None:
    """Check that the supplied syntax list is valid and can be used for checking."""
    which_elements_required = []
    for syntax_element in command_syntax:
        # check each element has a name, type and required attribute
        for required_attribute in ["name", "type", "required"]:
            if required_attribute not in syntax_element:
                raise ValueError("Missing the '{}' atribute.".format(required_attribute))
        # check the 'valid_values' attribute is of the correct type
        if "valid_values" in syntax_element and syntax_element["valid_values"] is not None:
            if syntax_element["type"] == "string":
                if isinstance(syntax_element["valid_values"], list) and syntax_element["valid_values"] != []:
                    if all(type(valid_value) is str for valid_value in syntax_element["valid_values"]):
                        pass
                    else:
                        raise TypeError("Elements of the attribute 'valid_values' of the argument '{}' must be strings.".format(syntax_element["name"]))
                else:
                    raise TypeError("Attribute 'valid_values' of the argument '{}' must be a nonempty list.".format(syntax_element["name"]))
            elif syntax_element["type"] in ["integer", "float"]:
                if type(syntax_element["valid_values"]) is tuple:
                    if 2 <= len(syntax_element["valid_values"]) <= 3:
                        if (type(syntax_element["valid_values"][0]) is int or type(syntax_element["valid_values"][0]) is float) and (type(syntax_element["valid_values"][1]) is int or type(syntax_element["valid_values"][1]) is float):
                            if syntax_element["valid_values"][0] <= syntax_element["valid_values"][1]:
                                if len(syntax_element["valid_values"]) == 3:
                                    if type(syntax_element["valid_values"][2]) is list:
                                        pass
                                    else:
                                        TypeError("Attribute 'valid_values' of the argument '{}' must be of the form (min, max, [extra_values]) where extra_values is a list.".format(syntax_element["name"]))
                            else:
                                raise ValueError("Attribute 'valid_values' of the argument '{}' must have min value smaller than max value.".format(syntax_element["name"]))
                        else:
                            raise TypeError("Attribute 'valid_values' of the argument '{}' must be of the form (min, max, [extra_values]) where min and max are of the type int or float.".format(syntax_element["name"]))
                    else:
                        raise ValueError("Attribute 'valid_values' of the argument '{}' must be either two or three long and of the form (min, max, [extra_values]).".format(syntax_element["name"]))
                else:
                    raise TypeError("Attribute 'valid_values' of the argument '{}' must be a tuple of the form (min, max, [extra_values]).".format(syntax_element["name"]))
            else:
                raise ValueError("'{}' is not a valid value for the attribute 'type' for the argument ''.".format(syntax_element["type"], syntax_element["name"]))
        which_elements_required.append(syntax_element["required"])
    # check that the required arguments are all first
    if any(which_elements_required[sum(which_elements_required):]):
        raise ValueError("Required arguments occur after optional arguments. {}".format(which_elements_required))


def argument_parser(command_string, command_syntax):
    """Parse and check arguments according to a syntax list."""
    syntax_checker(command_syntax)
    command_arguments = split_args(command_string)
    output_arguments = []
    for element_index, syntax_element in enumerate(command_syntax):
        try:
            argument_text = command_arguments[element_index]
        except IndexError:
            if syntax_element["required"]:
                print("The argument '{}' is not specified.".format(syntax_element["name"]))
                return
            else:
                try:
                    argument_text = syntax_element["default"]
                except KeyError:
                    break
        if syntax_element["type"] == "string":
            if "valid_values" in syntax_element and syntax_element["valid_values"] is not None:
                if argument_text in syntax_element["valid_values"]:
                    pass
                else:
                    valid_values_string = ", ".join(syntax_element["valid_values"])
                    print("'{}' is not a valid value for '{}' must be one of: {}.".format(argument_text, syntax_element["name"], valid_values_string))
                    return
        elif syntax_element["type"] in ["integer", "float"]:
            if len(syntax_element["valid_values"]) == 3 and argument_text in syntax_element["valid_values"][2]:
                pass
            else:
                try:
                    argument_text = float(argument_text)
                except ValueError:
                    print("The argument '{}' must be a number.".format(syntax_element["name"]))
                    return
                if syntax_element["type"] == "integer":
                    argument_text = int(math.floor(argument_text))
                # check if between valid values
                if syntax_element["valid_values"] is not None:
                    if syntax_element["valid_values"][0] <= argument_text:
                        if argument_text <= syntax_element["valid_values"][1]:
                            pass
                        else:
                            print("'{}' is bigger than {}.".format(syntax_element["name"], syntax_element["valid_values"][1]))
                            return
                    else:
                        print("'{}' is smaller than {}.".format(syntax_element["name"], syntax_element["valid_values"][0]))
                        return
        else:
            raise ValueError("Invalid syntax element type: {}".format(syntax_element["type"]))
        output_arguments.append(argument_text)
    return output_arguments

# TODO: Add custom error messages, e.g.: "error_missing_argument", "error_not_valid_string", "error_too_low", "error_too_high"
# TODO: Required should accept a string/list of strings that will only require if those arguments are included
# TODO: Output as dict of argument names and values
# TODO: Option for final string argument to accept the tail of the input string (e.g. for the sail command)
