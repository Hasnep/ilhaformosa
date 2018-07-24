"""Creates the functions that can read or change options."""

options_choices = {"currency": ["pound", "dollar"], "distance": ["modern", "ancient"], "date": ["ymd", "dmy"]}
default_options = {"currency": "pound", "distance": "modern", "date": "ymd"}
options = default_options


def print_options_choices(option_name):
    """A function that prints the list of all avavilable choices for one option."""
    output = "choices: [ "
    for k in options_choices[option_name]:
        output = output + k + " "
    output = output + "]"
    print(output)


def print_option(key):
    """A function to get the current value of an option."""
    if key in options:  # if the key is a name of one of the currently set options
        print("%s: %s (default: %s)" % (key, options[key], default_options[key]))
        print_options_choices(key)
    else:
        print("%s is not a valid option name" % key)


def print_all_options():
    """A function that prints all the currently set options"""
    for k in options:
        print_option(k)


def set_option(key, value):
    """A function to set the value of an option."""
    if key in options_choices:  # if the key is the name of an option
        if value in options_choices[key]:  # if the value is one of the available values
            options[key] = value  # set the value
            print("%s has been set to %s" % (key, value))
        else:
            print("%s is not a valid value for the option %s" % (value, key))
    else:
        print("%s is not a valid option name" % key)


def reset_option(key):
    """A function that resets an option back to default."""
    set_option(key, default_options[key])


def reset_all_options():
    """A function that resets all options back to default."""
    for key in options:
        reset_option(key)
