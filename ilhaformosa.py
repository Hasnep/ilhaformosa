from title import *
import cmd, textwrap, pyreadline
from player import *
import math
# from pdb import *  # use set_trace() to debug

# TODO: Use the ctypes library to set the title, width and font of the window.

def money(amount):
    """A function to add the currency symbol to money."""
    # TODO: Add commas to currency.
    currency_option = options["currency"]
    if currency_option == "pound":
        symbol = "£"
    elif currency_option == "dollar":
        symbol = "$"
    else:
        symbol = "?"
    return symbol + str(int(math.floor(amount)))


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

    def do_calendar(self, args):
        """Find out what the date is or what the date will be in the future.
        calendar [days]"""
        if args == "":
            print("It is %s." % day_to_date(_player.day))
            return
        else:
            try:
                args = float(args)
            except ValueError:
                print("Use calendar [days] to find out what the date will be in the future.")
                return
            else:
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

    def do_look(self, line):
        """Look around the port you are currently in."""
        print("You are in %s" % player.location.name)
        print("There is a ")
        for k in player.location.buildings:
            print("%s" % k)

    def do_sail(self, arg):
        """Set sail for a port.
        sail [destination]"""
        if arg == "":  # check if an argument was entered
            print("Use sail [destination] to sail to a port. You can see a list of ports using the map command.")
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
                    player.location.arrive()
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
                    if format_arg(k.nickname) == format_arg(old_nickname):
                        print("%s is now named %s" % (k.nickname, new_nickname))
                        k.nickname = new_nickname
                        return
                print("No ship with the name %s found." % old_nickname)
        else:
            print("Use rename [old name]>[new name] to rename a ship.")
            return

    def complete_rename(self, text, line, begidx, endidx):  # TODO: Add a more complex regex matching algorithm to return all matches
        """Tab completion for the rename command."""
        return [format_arg(k.nickname) for k in player.fleet if format_arg(k.nickname).startswith(format_arg(text))]

    def do_buy(self, arg):
        product = format_arg(arg)
        if product == "":
            print("Use buy [item] to buy something.")
            return
        elif player.cash == 0:
            print("You have no money on you.")
            return
        else:
            if product == "food":
                price = random_price(5.5, sd=1)
                if player.cash > price:
                    food = random.choice(["rice", "noodles", "soup"])
                    player.cash_decrease(price)
                    print("You spend %s on %s." % (money(price), food))
                    return
                else:
                    print("You can't find any food you can afford.")
                    return
            if product == "ship" or product == player.location.for_sale_ship.type:
                if "shipyard" in player.location.buildings:
                    if player.location.for_sale_ship is None:
                        print("There are no ships for sale here.")
                        return
                    else:
                        if player.cash >= player.location.for_sale_ship_price:
                            print("You buy %s for %s" % (player.location.for_sale_ship.nickname, money(player.location.for_sale_ship_price)))
                            player.cash_decrease(player.location.for_sale_ship_price)
                            player.fleet.append(player.location.for_sale_ship)
                            player.location.remove_for_sale_ship()
                            return
                        else:
                            print("You do not have enough money to buy this ship.")
                            return
                else:
                    print("There is no shipyard in %s." % player.location.name)
                    return

    # TODO: add a buy argument to the shipyard and make the buy command call this
    # TODO: add a look argument to look at the ship
    # TODO: add a repair argument with an all/max subcommand

    def do_shipyard(self, line):
        """Look at what's for sale in the shipyard"""
        if "shipyard" in player.location.buildings:
            if player.location.for_sale_ship is None:
                print("There are no ships for sale here.")
                return
            else:
                print("Price: " + money(player.location.for_sale_ship_price))
                print_ship_information(player.location.for_sale_ship)
                return
        else:
            print("There is no shipyard in %s." % player.location.name)
            return

    def do_cash(self, line):
        """Show your current cash, bank balance and debt."""
        print("Cash: " + money(player.cash))
        print("Bank balance: " + money(player.balance))
        print("Debt: " + money(player.debt))
        print("Total: " + money(player.cash + player.balance - player.debt))

    def do_deposit(self, arg):
        """Deposits money into a bank account.
        deposit [amount/max/all]"""
        arg = format_arg(arg)
        if "bank" in player.location.buildings:  # if there is a bank here
            if arg == "max" or arg == "all":
                deposit_amount = player.cash
            else:  # deposit amount is not "max/all"
                try:
                    deposit_amount = int(math.floor(float(arg)))
                except ValueError:
                    print("Use deposit [amount] to deposit.")
                    return
                else:  # successfully converted deposit amount to float
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
            print("There is no bank in %s." % player.location.name)
            return

    def do_withdraw(self, arg):
        """Withdraws money from a bank account.
        withdraw [amount/max/all]"""
        if "bank" in player.location.buildings:
            if arg == "max" or arg == "all":
                withdraw_amount = player.balance
            else:  # withdraw amount is not "max/all"
                try:
                    withdraw_amount = int(math.floor(float(arg)))
                except ValueError:
                    print("Use withdraw [amount] to withdraw.")
                    return
                else:
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
            print("%s does not have a bank." % player.location.name)
            return

    def do_bank(self, args):
        """Check your balance and deposit or withdraw cash.
        bank [deposit] [amount]"""
        if args == "":
            if "bank" in player.location.buildings:
                print("Interest rate: " + percent(player.bank_rate))
                self.do_cash(line=None)
                return
            else:
                print("There is no bank in %s." % player.location.name)
                return
        else:
            args = split_args(args)
            if len(args) != 2:
                print("Use bank [deposit/withdraw] [amount] to withdraw or deposit money.")
                return
            else:
                amount = args[1]
                if args[0] == "deposit":
                    self.do_deposit(amount)
                    return
                elif args[0] == "withdraw":
                    self.do_withdraw(amount)
                    return
                else:
                    print("Use bank [deposit/withdraw] [amount] to withdraw or deposit money.")
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
            ship_nickname = format_arg(arg)
            for k in player.fleet:
                if ship_nickname == format_arg(k.nickname):
                    print_ship_information(k)
                    return
            print("Use fleet [ship name] to get information about a ship.")

    def complete_fleet(self, text, line, begidx, endidx):  # TODO: Add a more complex regex matching algorithm to return all matches
        """Tab completion for the fleet command."""
        return [format_arg(k.nickname) for k in player.fleet if format_arg(k.nickname).startswith(format_arg(text))]

    def do_wait(self, arg):
        """Wait for a specified number of days.
        wait [number of days]"""
        arg = format_arg(arg)
        try:
            n_days = float(arg)
        except ValueError:
            print("%s is not a valid number" % arg)
            return
        else:
            if n_days <= 7:
                player.day_increase(n_days)
                print("You wait around for %s days." % math.floor(n_days))
                return
            else:
                print("You can only wait for one week at a time.")
                return

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
