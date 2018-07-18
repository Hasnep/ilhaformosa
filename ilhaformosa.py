from title import *
import cmd, textwrap, pyreadline
import math
from player import *
# from pdb import * # use set_trace() to debug


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

    def do_calendar(self, args):
        """Find out what the date is or what the date will be in the future.
        calendar [days]"""
        if args == "":
            print("It is %s." % day_to_date(player["day"]))
            return
        else:
            try:
                args = float(args)
            except:
                print("Use calendar [days] to find out what the date will be in the future.")
                return
        if args < 365*10:
            print("In %s days it will be %s." % (math.floor(args), day_to_date(player["day"] + args)))
        else:
            print("Your calendar only has pages for the next 10 years.")

    do_cal = do_calendar

    def do_map(self, line):
        """List the locations on the map."""
        # TODO: Add an argument to look at the buildings of a certain port.
        print("You are in %s" % player["location"].name)
        print("The map has these ports on it:")
        for key, value in world.items():
            print(value.name)

    # TODO: Make a function to go into a building.

    def do_look(self, line):
        """Look around the port you are currently in."""
        # TODO: Make this command the gointobuilding command with no arguments.
        print("You are in %s" % player["location"].name)
        print("There is a ")
        for k in player["location"].buildings:
            print(k.type)

    def do_sail(self, destination):
        """Set sail for a port.
        sail [destination]"""
        # TODO: Check if you're already there
        print("You set sail for %s" % world[destination].name)
        print(world[destination].landing_message)
        print(world[destination].description)
        player["location"] = world[destination]

    def complete_sail(self, text, line, begidx, endidx):
        """Tab completion for the sail command."""
        return [key for key, value in world.items() if key.startswith(text)]

    def do_rename(self, args):
        """Rename a ship.
        rename [old name]>[new name]"""
        args = args.split(">")
        if len(args) != 2:
            print("Use [old name]>[new name] to rename a ship.")
        else:
            rename_ship(args[0], args[1])
            print("%s is now named %s" % (args[0], args[1]))

    def do_fleet(self, arg):
        """Get information about a single ship or your whole fleet.
        fleet [ship name]"""
        # TODO: Properly test this command with a large fleet.
        if arg == "":
            print("Your fleet has %s ship(s)" % len(player["fleet"]))
            for k in player["fleet"]:
                print_ship_information(k)
        else:
            for k in player["fleet"]:
                if arg == k.nickname:
                    print_ship_information(k)
                    return
            print("Use fleet [ship name] to get information about a ship.")


    def do_wait(self, args):
        """Wait for a specified number of days.
        wait [number of days]"""
        try:
            args = float(args)
        except:
            print("%s is not a valid number" % args)
            return
        if args <= 7:
            days_passed(args)
            print("You wait around for %s days." % math.floor(args))
        else:
            print("You can only wait for one week at a time.")

    def do_quit(self, line):
        """Quit the game."""
        return True


IlhaFormosa().cmdloop()
print('Thank you for playing Ilha Formosa!')
