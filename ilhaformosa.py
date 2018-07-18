# from title import *
import cmd, textwrap, pyreadline
from options import *
from ships import *
from ports import *
import datetime
from pdb import * # use set_trace() to debug

# Money


def money(amount):
    """Add the currency symbol to money."""
    return options["currency"] + " " + amount


my_cash = 1000
my_balance = 0
my_debt = 0

# Time
start_date = datetime.date(1700, 1, 1)
day = 0


def day_to_date(x):
    """Convert the number of days to a readable string."""
    x = start_date + datetime.timedelta(days=x)
    if options['date'] == "ymd":
        x = x.strftime("%Y-%m-%d")
    elif options['date'] == "dmy":
        x = x.strftime("%d/%m/%Y")
    return x


my_fleet = [Junk()]
my_location = world["taipei"]


def set_sail(destination):
    """A function that travels to a location."""
    print("You set sail for %s" % world[destination].name)
    print(world[destination].landing_message)
    print(world[destination].description)
    return world[destination]


def rename_ship(old_nickname, new_nickname):
    """A function that changes the nickname of a ship."""
    for k in my_fleet:
        if k.nickname == old_nickname:
            k.nickname = new_nickname


class IlhaFormosa(cmd.Cmd):
    prompt = '\n > '

    def do_options(self, args):
        """Vew or modify an option or reset all options to default.
        options [option] [new value/default] or options default to reset to defaults"""
        args = args.split()
        if len(args) > 2:  # if too many options have been entered
            print("Use options [option] [new value] to set an option.")
        elif len(args) == 2:  # if an option and a value were specified
            if args[1] == "default":
                reset_option(args[0])
            else:
                set_option(args[0], args[1])
        elif len(args) == 1:  # if only an option was specified
            if args[0] == "default":  # if resetting all options to default
                reset_all_options()
            else:  # if only an option name was specified
                print_option(args[0])
        elif len(args) == 0:  # if no option name was specified
            print_all_options()

    def do_calendar(self, line):
        """Find out what the date is."""
        print("It is %s." % day_to_date(day))

    do_cal = do_calendar

    def do_map(self, line):
        """List the locations on the map."""
        print("You are in %s" % my_location.name)
        print("The map has these ports on it:")
        for key, value in world.items():
            print(value.name)

    def do_look(self, line):
        """Look around the port you are currently in."""
        print("You are in %s" % my_location.name)
        print("There is a ")
        for k in my_location.buildings:
            print(k.type)

    def do_sail(self, destination):
        """Set sail for a port.
        sail [destination]"""
        my_location = set_sail(destination)

    def complete_sail(self, text, line, begidx, endidx):
        return [key for key, value in world.items() if key.startswith(text)]

    def do_rename(self, nicknames):
        """Rename a ship.
        rename [old name]>[new name]"""
        nicknames = nicknames.split(">")
        if len(nicknames) != 2:
            print("Use [old name]>[new name] to rename a ship.")
        else:
            rename_ship(nicknames[0], nicknames[1])
            print("%s is now named %s" % (nicknames[0], nicknames[1]))

    def do_fleet(self, line):
        """Get information about your fleet."""
        print("Your fleet has %s ship(s)" % len(my_fleet))
        for k in my_fleet:
            print_ship_information(k)

    def do_quit(self, line):
        """Quit the game."""
        return True


IlhaFormosa().cmdloop()
print('Thank you for playing Ilha Formosa!')
