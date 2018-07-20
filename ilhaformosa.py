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
    def do_enter(self, arg):
        """Enter a building.
        enter [building type]"""
        arg = arg.split()
        if len(arg) == 1:  # check if a valid name was entered
            arg = arg[0]
            if arg in all_building_types:  # check if argument is a building that exists
                if arg in player["location"].buildings:  # check if argument is in this port
                    print("You enter %s" % world["taipei"].buildings[arg].name)
                    return
                else:
                    print("There is no %s in %s." % (arg, player["location"]))
                    return
            else:
                print("There is no building called %s. Use look to see the buildings in this port." % arg)
                return
        else:
            print("Use enter [building type] to go into a building.")
            return

    def do_look(self, line):
        """Look around the port you are currently in."""
        # TODO: Make this command the gointobuilding command with no arguments.
        print("You are in %s" % player["location"].name)
        print("There is a ")
        for key, value in player["location"].buildings.items():
            print("%s called %s" % (value.type, value.name))

    def do_sail(self, arg):
        """Set sail for a port.
        sail [destination]"""
        if arg == "":  # check if an argument was entered
            print("Use sail [destination] to sail to a port. You can see a list of ports using the 'map' command.")
            return
        else:
            arg = arg.lower()  # make the argument lowercase
            arg = arg.replace(" ", "")  # remove spaces from argument
            if arg in world:  # check if port object exists as a key
                # TODO: Find out if it is more efficient to compare names or dicts.
                if player["location"].name == world[arg].name:  # check if the player is already at their destination
                    print("You are already in %s." % player["location"].name)
                    return
                else:
                    player["building"] = None
                    from_name = player["location"].name
                    to_name = world[arg].name
                    journey_distance = ports_distances[from_name][to_name]
                    journey_speed = 8  # TODO: Change this to top speed.
                    journey_time = (journey_distance / 8)/24
                    day_increase(journey_time)
                    print("You sail %s nautical miles at %s knots for %s days." % (journey_distance, journey_speed, math.floor(journey_time)))
                    print("You land in %s." % to_name)
                    print("It is %s." % day_to_date(player["day"]))
                    player["location"] = world[arg]
                    return
            else:
                print("%s is not a port on your map. You can see a list of ports using the 'map' command." % arg)
                return

    def complete_sail(self, text, line, begidx, endidx):
        """Tab completion for the sail command."""
        # TODO: Remove the current port from the tab completion list.
        return [key for key, value in world.items() if key.startswith(text)]

    def do_rename(self, args):
        """Rename a ship.
        rename [old name]>[new name]"""
        args = args.split(">")
        if len(args) != 2:
            print("Use rename [old name]>[new name] to rename a ship.")
            return
        else:
            old_nickname = args[0]
            new_nickname = args[1]
            if new_nickname == "":
                print("Use rename [old name]>[new name] to rename a ship.")
                return
            for k in player["fleet"]:
                if k.nickname == old_nickname:
                    k.nickname = new_nickname
                    print("%s is now named %s" % (old_nickname, new_nickname))
                    return
            print("No ship with the name %s found." % old_nickname)

    # TODO: Add tab completion for the rename command

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


    def do_cash(self, line):
        """Show your current cash, bank balance and debt."""
        print("Cash: " + money(player["cash"]))
        print("Bank balance: " + money(player["balance"]))
        print("Debt: " + money(player["debt"]))
        print("Total: " + money(player["cash"] + player["balance"] - player["debt"]))


    def do_wait(self, args):
        """Wait for a specified number of days.
        wait [number of days]"""
        try:
            args = float(args)
        except:
            print("%s is not a valid number" % args)
            return
        if args <= 7:
            day_increase(args)
            print("You wait around for %s days." % math.floor(args))
        else:
            print("You can only wait for one week at a time.")

    def do_credits(self, line):
        """Print the credits for the game."""
        print("Game by Hannes Smit (hasnep.github.io)")
        # print("Map modified from Wikimedia Commons (Asia Countries Gray)")

    def do_quit(self, line):
        """Quit the game."""
        return True


IlhaFormosa().cmdloop()
print('Thank you for playing Ilha Formosa!')
