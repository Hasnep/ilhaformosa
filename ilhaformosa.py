from title import *
import cmd, textwrap, pyreadline
from player import *
# from pdb import * # use set_trace() to debug


def split_args(input_string):
    input_string = input_string.lower()
    input_string = input_string.split()
    return input_string


def format_arg(input_string):
    input_string = input_string.lower()
    input_string = input_string.replace(" ", "")
    return input_string


class IlhaFormosa(cmd.Cmd):
    prompt = '\n > '  # set the prompt

    def do_options(self, args):
        """View or modify an option or reset all options to default.
        options [option name] [new value/default] or options default to reset to defaults"""
        args = split_args(args)
        if len(args) > 2:  # if too many options have been entered
            print("Use options [option name] [new value] to set an option.")
            return
        elif len(args) == 2:  # if an option and a value were specified
            option_name = args[0]
            option_value = args[1]
            if option_value == "default":  # if the value specified was "default"
                reset_option(option_name)
                return
            else:
                set_option(option_name, option_value)  # set the option to the specified value
                return
        elif len(args) == 1:  # if only an option was specified
            option_name = args[0]
            if option_name == "default":  # if resetting all options to default
                reset_all_options()
                return
            else:  # if only an option name was specified
                print_option(option_name)
                return
        elif len(args) == 0:  # if no option name was specified
            print_all_options()
            return

    def do_calendar(self, args, _player=player):
        """Find out what the date is or what the date will be in the future.
        calendar [days]"""
        if args == "":
            print("It is %s." % day_to_date(_player.day))
            return
        else:
            try:
                args = float(args)
            except:
                print("Use calendar [days] to find out what the date will be in the future.")
                return
        if args <= 365*10:
            print("In %s days it will be %s." % (math.floor(args), day_to_date(_player.day + args)))
        else:
            print("Your calendar only has pages for the next 10 years.")

    do_cal = do_calendar

    def do_map(self, line):
        """List the locations on the map."""
        # TODO: Add an argument to look at the buildings of a certain port.
        print("You are in %s" % player.location.name)
        print("The map has these ports on it:")
        for key, value in world.items():
            print(value.name)
        # TODO: Show an ascii map of the world.

    def do_enter(self, arg):
        """Enter a building.
        enter [building type]"""
        building_type = format_arg(arg)
        if building_type in all_building_types:  # check if argument is a building that exists
            if building_type in player.location.buildings:  # check if argument is in this port
                building_object = player.location.buildings[building_type]
                print("You enter %s" % building_object.name)
                player.building = building_object
                building_object.enter_building()
                return
            else:
                print("There is no %s in %s." % (building_type, player.location))
                return
        else:
            print("There is no building called %s. Use look to see the buildings in this port." % building_type)
            return

    # TODO: Add tab completion for the enter command.

    def do_look(self, line):
        """Look around the port you are currently in."""
        # TODO: Make this command the enter building command with no arguments.
        print("You are in %s" % player.location.name)
        print("There is a ")
        for key, value in player.location.buildings.items():
            print("%s called %s" % (value.type, value.name))

    def do_sail(self, arg):
        """Set sail for a port.
        sail [destination]"""
        if arg == "":  # check if an argument was entered
            print("Use sail [destination] to sail to a port. You can see a list of ports using the 'map' command.")
            return
        else:
            destination_id = format_arg(arg)
            if destination_id in world:  # check if port object exists as a key
                destination_port = world[destination_id]
                # TODO: Find out if it is more efficient to compare names or dicts.
                if player.location == destination_port:  # check if the player is already at their destination
                    print("You are already in %s." % destination_port.name)
                    return
                else:
                    player.leave_building()
                    from_name = player.location.name
                    to_name = world[arg].name
                    journey_distance = ports_distances[from_name][to_name]
                    journey_speed = 8  # TODO: Change this to top speed.
                    journey_time = (journey_distance / 8)/24
                    player.day_increase(journey_time)
                    # TODO: Add a sailing animation.
                    print("You sail %s nautical miles at %s knots for %s days." % (journey_distance, journey_speed, math.floor(journey_time)))
                    print("You land in %s." % to_name)
                    print("It is %s." % day_to_date(player.day))
                    player.set_location(arg)
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
        if len(args) == 2:
            old_nickname = args[0]
            new_nickname = args[1]
            if old_nickname == "" or new_nickname == "":
                print("Use rename [old name]>[new name] to rename a ship.")
                return
            else:
                for k in player.fleet:
                    if k.nickname == old_nickname:
                        k.nickname = new_nickname
                        print("%s is now named %s" % (old_nickname, new_nickname))
                        return
                print("No ship with the name %s found." % old_nickname)
        else:
            print("Use rename [old name]>[new name] to rename a ship.")
            return

    # TODO: Add tab completion for the rename command

    def do_buy(self, arg):  # TODO: Add the ability to buy ships.
        if player.building is None:
            print("Enter a building to buy something.")
            return
        else:
            if player.building.wares is None:
                print("You can't buy anything here.")
                return
            else:
                if player.cash >= player.building.sale_price:
                    player.cash_decrease(player.building.sale_price)
                    player.fleet.append(player.building.wares)
                    player.building.reset_wares()
                    return
                else:
                    print("Not enough money.")
                    return

    def do_deposit(self, arg):
        """Deposits money into a bank account.
        deposit [amount/max/all]"""
        if player.building is not None and player.building.type.lower() == "bank":
            if arg == "max" or arg == "all":
                deposit_amount = player.cash
            else:
                try:
                    deposit_amount = float(arg)
                except:
                    print("Use deposit [amount] to deposit.")
                    return
                if deposit_amount > player.cash:
                    print("You cannot deposit more money than you have on you.")
                    return
                elif deposit_amount == 0:
                    print("You cannot deposit nothing.")
                    return
                elif deposit_amount < 0:
                    print("Use withdraw [amount] to withdraw money.")
                    return
            player.deposit_cash(deposit_amount)
            print("You deposit %s into the bank." % money(deposit_amount))
            return
        else:
            print("Visit a bank to deposit money.")
            return

    def do_withdraw(self, arg):
        """Withdraws money from a bank account.
        withdraw [amount/max/all]"""
        if player.building is not None and player.building.type.lower() == "bank":
            if arg == "max" or arg == "all":
                withdraw_amount = player.balance
            else:
                try:
                    withdraw_amount = float(arg)
                except:
                    print("Use withdraw [amount] to withdraw.")
                    return
                if withdraw_amount > player.balance:
                    print("You cannot withdraw more money than you have in the bank.")
                    return
                elif withdraw_amount == 0:
                    print("You cannot withdraw nothing.")
                    return
                elif withdraw_amount < 0:
                    print("Use deposit [amount] to deposit money.")
                    return
            player.withdraw_cash(withdraw_amount)
            print("You withdraw %s from the bank." % money(withdraw_amount))
            return
        else:
            print("Visit a bank to withdraw money.")
            return

    def do_fleet(self, arg):
        """Get information about a single ship or your whole fleet.
        fleet [ship name]"""
        # TODO: Properly test this command with a large fleet.
        if arg == "":
            print("Your fleet has %s ship(s)" % len(player.fleet))
            for k in player.fleet:
                print_ship_information(k)
        else:
            ship_nickname = arg
            for k in player.fleet:
                if ship_nickname == k.nickname:
                    print_ship_information(k)
                    return
            print("Use fleet [ship name] to get information about a ship.")

    def do_cash(self, line):
        """Show your current cash, bank balance and debt."""
        print("Cash: " + money(player.cash))
        print("Bank balance: " + money(player.balance))
        print("Debt: " + money(player.debt))
        print("Total: " + money(player.cash + player.balance - player.debt))

    def do_wait(self, args):
        """Wait for a specified number of days.
        wait [number of days]"""
        try:
            n_days = float(args)
        except:
            print("%s is not a valid number" % args)
            return
        if n_days <= 7:
            player.day_increase(n_days)
            print("You wait around for %s days." % math.floor(n_days))
        else:
            print("You can only wait for one week at a time.")

    def do_credits(self, line):
        """Print the credits for the game."""
        print("Game by Hannes Smit (hasnep.github.io)")
        # print("Map modified from Wikimedia Commons (Asia Countries Gray)")

    def do_quit(self, line):
        """Quit the game."""
        return True

    # TODO: Add unknown command support.
    # def default(self, arg):
    # print("%s is not a known command. Type ? for a list of commands." % arg.lower())


IlhaFormosa().cmdloop()
print("Thank you for playing Ilha Formosa!")
