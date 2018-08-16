# TODO: Add an option for sig figs when using units
# TODO: Add an option for using words billion/million when using units
# TODO: Add import/export of options


class Options(object):
    def __init__(self):
        self.choices = {
            "currency": ["pound", "dollar", "gold", "doubloon"],
            "distance": ["modern", "ancient"],  # TODO: implement distance units
            "weight": ["kg"],  # TODO: implement weight units
            "date": ["ymd", "dmy"]
        }
        self.default_options = {key: value[0] for key, value in self.choices.items()}
        self.options = self.default_options

    def get_option(self, option_name: str):
        """A function to get the current value of an option."""
        return self.options[option_name]

    def set_option(self, option_name: str, value: str):
        """A function to set the value of an option."""
        if option_name in self.choices:  # if the key is the name of an option
            if value in self.choices[option_name]:  # if the value is one of the available values
                self.options[option_name] = value  # set the value
                print("'{}' has been set to '{}'.".format(option_name, value))
                return
            else:
                print("'{}' is not a valid value for the option '{}'.".format(value, option_name))
                return
        else:
            print("'{}' is not a valid option name.".format(option_name))
            return

    def reset_option(self, option_name: str):
        """A function that resets an option back to default."""
        self.set_option(option_name, self.choices[option_name][0])

    def reset_all_options(self):
        """A function that resets all options back to default."""
        for option_name in self.default_options:
            self.reset_option(option_name)
        return

    def print_option(self, option_name: str):  # TODO: turn this into a flexitable
        """A function that prints all the choices available for a certain option, highlighting the current value and the default value."""
        if option_name in self.options:
            choices_string = ""
            for choice_name in self.choices[option_name]:
                if self.get_option(option_name) == choice_name:
                    choices_string = choices_string + "[" + choice_name + "] "
                else:
                    choices_string = choices_string + choice_name + " "
            choices_string = choices_string[0:-1]
            print(option_name + ": " + choices_string)
        else:
            print("{} is not a valid option name".format(option_name))
            return

    def print_all_options(self):
        """A function that prints all the choices available for every option."""
        for option_name in self.options:
            self.print_option(option_name)


options = Options()
