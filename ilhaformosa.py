import cmd
import pyreadline  # used for tab completion

from title import *
from player import *
from commandsyntax import *


class IlhaFormosa(cmd.Cmd):
    prompt = '\n > '  # set the prompt

    def do_help(self, args):
        """List all the available commands or show help for a specific command."""
        args = argument_parser(args, command_syntax["help"])
        if len(args) == 0:
            widest_command = max([len(command_name) for command_name in all_commands])
            print("All commands:")
            n_commands_per_line = math.floor(90/(widest_command+1))
            for line_of_commands in [all_commands[i:i + n_commands_per_line] for i in range(0, len(all_commands), n_commands_per_line)]:
                print(" ".join([align_text(command_name, widest_command, "l") for command_name in line_of_commands]))
            print("Use help [command] to get more information about a command.")
            return
        else:
            command_name = args[0]
            if command_name == "all":
                for command_name in all_commands:
                    print(command_name + ": " + getattr(self, "do_" + command_name).__doc__)
                return
            else:
                print(getattr(self, "do_" + command_name).__doc__)
                if command_name in command_syntax and len(command_syntax[command_name]) > 0:
                    selected_command_syntax = command_syntax[command_name]
                    command_syntax_string = command_name
                    for argument in selected_command_syntax:
                        if argument["required"]:
                            brackets = "<>"
                        else:
                            brackets = "[]"
                        command_syntax_string += " " + brackets[0] + argument["name"] + brackets[1]
                    print(command_syntax_string)
                    return
                else:
                    return

    def do_options(self, args):
        """View or modify an option or reset all options to default."""
        args = argument_parser(command_string=args, command_syntax=command_syntax["options"])
        if args is None:
            return
        else:
            if len(args) > 2:  # if too many options have been entered
                print("Use options [option name] [new value] to set an option.")
                return
            elif len(args) == 2:  # if an option and a value were specified
                option_name = args[0]
                option_value = args[1]
                if option_value == "default":  # if the value specified was "default"
                    options.reset_option(option_name)
                    return
                else:
                    options.set_option(option_name, option_value)  # set the option to the specified value
                    return
            elif len(args) == 1:  # if only an option was specified
                option_name = args[0]
                if option_name == "default":  # if resetting all options to default
                    options.reset_all_options()
                    return
                else:  # if only an option name was specified
                    options.print_option(option_name)
                    return
            elif len(args) == 0:  # if no option name was specified
                options.print_all_options()
                return

    def complete_options(self, text, line, begidx, endidx):
        """Tab completion for the options command."""
        args = split_args(line)
        if len(args) == 1:
            return [option_name for option_name in options.choices]
        elif len(args) == 2:
            return [option_name for option_name in options.choices if option_name.startswith(text)]
        elif len(args) == 3 and args[1] in options.choices:
            option_name = args[1]
            return [option_choice for option_choice in options.choices[option_name] if option_choice.startswith(text)]
        else:
            return ""

    def do_calendar(self, args):
        """Find out what the date is or what the date will be in the future."""
        args = argument_parser(command_string=args, command_syntax=command_syntax["calendar"])
        if args is None:
            return
        else:
            if len(args) == 0:
                print("It is {}.".format(day_to_date(player.day)))
                return
            else:
                print("In {} days it will be {}.".format(args, day_to_date(player.day + args)))
                return

    def do_map(self, line):
        """List the locations on the map."""
        # TODO: Add an argument to look at the buildings of a certain port.
        print("You are in {}.".format(player.location.name))
        print("Your map has these ports on it: {}".format(", ".join(all_ports)))
        # TODO: Show an ascii map of the world.

    def do_look(self, line):
        """Look around the port you are currently in."""
        print("You are in {}.".format(player.location.name))
        print("There is a {}".format(", ".join(player.location.buildings)))

    def do_sail(self, arg):
        """Set sail for a port."""
        if arg == "":  # check if an argument was entered
            print("Use sail [destination] to sail to a port. You can see a list of ports using the map command.")
            return
        else:
            destination_id = format_arg(arg)
            if destination_id not in world:  # TODO: Check if discovered port
                print("{} is not a port on your map. You can see a list of ports using the 'map' command.".format(arg))
                return
            else:
                destination_port = world[destination_id]
                # TODO: Find out if it is more efficient to compare names or dicts.
                if player.location == destination_port:  # check if the player is already at their destination
                    print("You are already in {}.".format(destination_port.name))
                    return
                else:
                    if player.get_cargo_weight() > player.get_cargo_capacity():
                        print("Your ships are too full to sail. You have {} but your ships' capacity is {}. Sell some cargo or buy a ship to continue.".format(weight(player.get_cargo_weight()), weight(player.get_cargo_capacity())))
                    else:
                        departing_port = player.location
                        arriving_port = world[arg]
                        # before leaving
                        departing_port.visited = player.day
                        # while travelling
                        journey_distance = ports_distances[departing_port.name][arriving_port.name]
                        journey_speed = 8  # TODO: Change this to top speed.
                        journey_time = int(math.ceil(journey_distance / 8)/24)
                        cargo.global_values = cargo.randomise_values(cargo.global_values, journey_time)
                        player.day += journey_time
                        print("You sail {} nautical miles at {} knots for {} days.".format(journey_distance, journey_speed, math.floor(journey_time)))
                        # TODO: Add a sailing animation.
                        # upon arriving
                        if arriving_port.last_visited is None:
                            since_last_visit = 100
                        else:
                            since_last_visit = player.day - arriving_port.last_visited
                        # shipyard
                        if "shipyard" in arriving_port.buildings:
                            ship_type_class = random.choice(all_ship_objects)
                            arriving_port.for_sale_ship = ship_type_class()
                            arriving_port.for_sale_ship_price = random_price(arriving_port.for_sale_ship.value, base=100)
                        # market
                        arriving_port.local_values = cargo.randomise_values(arriving_port.local_values, since_last_visit)
                        arriving_port.local_prices = cargo.calculate_prices(arriving_port.local_values)
                        player.location = arriving_port
                        print("You land in {} on {}.".format(arriving_port.name, day_to_date(player.day)))
                        return

    def complete_sail(self, text, line, begidx, endidx):
        """Tab completion for the sail command."""
        return [port for port in world if (port.startswith(text) and port != player.location.id)]

    def do_market(self, args):
        """Get the market's prices or buy and sell cargo."""
        args = split_args(args)
        if len(args) == 0:
            cargo.table_cargo_prices(player.location.local_prices, player.cargo)
            return
        else:
            if args[0] in ["buy", "sell"] and len(args) >= 2:
                if args[1] in cargo.types:
                    self.onecmd(" ".join(args))
                    return
                else:
                    print("Buy a cargo: {}".format(", ".join(cargo.types)))
                    return
            else:
                print("Use market [buy/sell] [item] [quantity/max/all] to buy or sell cargo.")
                return

    def do_cargo(self, line):  # TODO: Add cargo tetris? Add more detailed cargo management?
        """Show the fleet's current cargo."""
        table_aligned_print(column_names=["owned"], column_aligns=["r"], row_keys=cargo.types, column_dicts=[weight(player.cargo)], show_header=True, show_row_keys=True)
        print("")
        bar(player.get_cargo_weight(), player.get_cargo_capacity(), units=weight)

    def do_rename(self, args):
        """Rename a ship."""
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
                        print("{} is now named {}.".format(k.nickname, new_nickname))
                        k.nickname = new_nickname
                        return
                print("No ship with the name {} found.".format(old_nickname))
        else:
            print("Use rename [old name]>[new name] to rename a ship.")
            return

    def complete_rename(self, text, line, begidx, endidx):  # TODO: Add a more complex regex matching algorithm to return all matches
        """Tab completion for the rename command."""
        return [format_arg(k.nickname) for k in player.fleet if format_arg(k.nickname).startswith(format_arg(text))]

    def do_buy(self, args):
        """Buy something from a shop."""
        args = split_args(args)
        if len(args) == 0:
            print("Use buy [item] [quantity/max/all] to buy something.")
            return
        elif len(args) >= 2:
            quantity = args[1]
            if quantity not in ["max", "all"]:
                try:
                    quantity = int(float(quantity))
                except ValueError:
                    print("'{}' is not a valid quantity. Use buy [item] [quantity/max/all] to buy something.".format(quantity))
                    return
        else:
            quantity = 1
        product = args[0]
        if product == "food":
            if quantity in ["max", "all"]:
                quantity = 10
            price = quantity * random_price(5.5, sd=1)  # TODO: change random_price to accept a quantity variable.
            if player.cash > price:
                food = random.choice(["rice", "noodles", "soup"])
                player.cash -= price
                print("You spend {} on {}.".format(money(price), food))
                return
            else:
                print("You can't find any food you can afford.")
                return
        if product == "ship" or (player.location.for_sale_ship is not None and product == player.location.for_sale_ship.type):
            if "shipyard" in player.location.buildings:
                if player.location.for_sale_ship is None:
                    print("There are no ships for sale here.")
                    return
                else:
                    price = player.location.for_sale_ship_price
                    if player.cash >= price:
                        print("You buy {} for {}.".format(player.location.for_sale_ship.nickname, money(price)))
                        player.cash -= price
                        player.fleet.append(player.location.for_sale_ship)
                        player.location.remove_for_sale_ship()
                        return
                    else:
                        print("You do not have enough money to buy this ship.")
                        return
            else:
                print("There is no shipyard in {}.".format(player.location.name))
                return
        elif product in cargo.types:
            empty_space = player.get_cargo_capacity() - player.get_cargo_weight()
            if empty_space == 0:
                print("You have no room on your fleet for more cargo.")
                return
            if quantity in ["max", "all"]:
                max_quantity_cash = math.floor(player.cash/player.location.local_prices[product])
                quantity = min(max_quantity_cash, empty_space)
            price = quantity * player.location.local_prices[product]
            if quantity <= empty_space:
                if price <= player.cash:
                    print("You buy {} of {} for {}.".format(weight(quantity), product, money(price)))
                    player.cash -= price
                    player.set_cargo_quantity(product, player.get_cargo_weight(product) + quantity)
                    return
                else:
                    print("You do not have enough money to buy {} of {}.".format(weight(quantity), product))
                    return
            else:
                print("You do not have enough empty space on your fleet to buy {} of {}. You have room for {} of cargo.".format(weight(quantity), product, weight(empty_space)))
                return
        else:
            print("You can't buy '{}'.".format(product))
            return

    def complete_buy(self, text, line, begidx, endidx):
        """Tab completion for the buy command."""
        args = split_args(line)
        if len(args) == 2:
            return [k for k in ["food", "ship"] + cargo.types if k.startswith(format_arg(text))]
        else:
            return []

    # TODO: add a buy argument to the shipyard and make the buy command call this
    # TODO: add a repair argument with an all/max subcommand

    def do_shipyard(self, line):
        """Look at what's for sale in the shipyard."""
        if "shipyard" in player.location.buildings:
            if player.location.for_sale_ship is None:
                print("There are no ships for sale here.")
                return
            else:
                print("Price: " + money(player.location.for_sale_ship_price))
                print_ship_information(player.location.for_sale_ship)
                return
        else:
            print("There is no shipyard in {}.".format(player.location.name))
            return

    def do_cash(self, line):
        """Show your current cash, bank balance and debt."""
        print("Cash: " + money(player.cash))
        print("Bank balance: " + money(player.balance))
        print("Debt: " + money(player.debt))
        print("Total: " + money(player.total_money))

    def do_deposit(self, arg):
        """Deposits money into a bank account."""
        arg = format_arg(arg)
        if "bank" in player.location.buildings:  # if there is a bank here
            if arg == "max" or arg == "all":
                deposit_amount = player.cash
            else:  # deposit amount is not "max/all"
                try:
                    deposit_amount = int(math.floor(float(arg)))
                except ValueError:
                    print("Use deposit [amount] to deposit money.")
                    return
            player.move_cash(deposit_amount, "deposit")
            return
        else:
            print("There is no bank in {}.".format(player.location.name))
            return

    def do_withdraw(self, arg):
        """Withdraws money from a bank account."""
        arg = format_arg(arg)
        if "bank" in player.location.buildings:  # if there is a bank here
            if arg == "max" or arg == "all":
                withdraw_amount = player.balance
            else:  # withdraw amount is not "max/all"
                try:
                    withdraw_amount = int(math.floor(float(arg)))
                except ValueError:
                    print("Use withdraw [amount] to deposit money.")
                    return
            player.move_cash(withdraw_amount, "withdraw")
            return
        else:
            print("There is no bank in {}.".format(player.location.name))
            return

    def do_bank(self, args):
        """Check your balance and deposit or withdraw cash."""
        if args == "":
            if "bank" in player.location.buildings:
                print("Interest rate: " + percent(player.bank_rate))
                self.onecmd("cash")
                return
            else:
                print("There is no bank in {}.".format(player.location.name))
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

    def do_borrow(self, arg):
        """Borrows money from the moneylender."""
        arg = format_arg(arg)
        if "moneylender" in player.location.buildings:  # if there is a moneylender here
            if arg == "max" or arg == "all":
                borrow_amount = player.max_debt - player.debt
            else:  # borrow amount is not "max/all"
                try:
                    borrow_amount = int(math.floor(float(arg)))
                except ValueError:
                    print("Use borrow [amount] to borrow money.")
                    return
            player.move_cash(borrow_amount, "borrow")
            return
        else:
            print("There is no moneylender in {}.".format(player.location.name))
            return

    def do_repay(self, arg):
        """Repays money to the moneylender."""
        arg = format_arg(arg)
        if "moneylender" in player.location.buildings:  # if there is a moneylender here
            if arg == "max" or arg == "all":
                repay_amount = player.debt
            else:  # repay amount is not "max/all"
                try:
                    repay_amount = int(math.floor(float(arg)))
                except ValueError:
                    print("Use repay [amount] to borrow money.")
                    return
            player.move_cash(repay_amount, "repay")
            return
        else:
            print("There is no moneylender in {}.".format(player.location.name))
            return

    def do_moneylender(self, args):
        """Borrow money or repay a debt."""
        if args == "":
            if "moneylender" in player.location.buildings:
                print("Interest rate: " + percent(player.lend_rate))
                self.onecmd("cash")
                return
            else:
                print("There is no moneylender in {}.".format(player.location.name))
                return
        else:
            args = split_args(args)
            if len(args) != 2:
                print("Use moneylender [borrow/repay] [amount] to borrow money or repay a debt.")
                return
            else:
                amount = args[1]
                if args[0] == "borrow":
                    self.do_borrow(amount)
                    return
                elif args[0] == "repay":
                    self.do_repay(amount)
                    return
                else:
                    print("Use moneylender [borrow/repay] [amount] to borrow money or repay a debt.")
                    return

    def do_fleet(self, arg): # TODO: Turn this into a flexitable
        """Get information about a single ship or your whole fleet."""
        if arg == "":
            is_plural = len(player.fleet) != 1
            print("Your fleet has {} ship{}.".format(len(player.fleet), "s" * is_plural))
            print("")
            for k in player.fleet:
                print_ship_information(k)
                print("")
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
        """Wait for a specified number of days."""
        arg = format_arg(arg)
        try:
            n_days = int(math.floor(float(arg)))
        except ValueError:
            print("{} is not a valid number".format(arg))
            return
        else:
            if n_days > 7:
                print("You can only wait for one week at a time.")
                return
            elif n_days < 0:
                print("You cannot go back in time.")
                return
            elif n_days == 0:
                print("You cannot wait for no days.")
                return
            else:
                player.day += n_days
                print("You wait around for {} days.".format(math.floor(n_days)))
                return

    def do_debug(self, line):
        """Show internal information."""
        print("Location")
        print(" Name: " + player.location.name)
        print(" ID: " + player.location.id)
        print("Market")
        print(" Global values: " + str(cargo.global_values))
        print(" Local values: " + str(player.location.local_values))
        return

    def do_credits(self, line):
        """Print the credits for the game."""
        print("Game by Hannes Smit (hasnep.github.io)")
        # print("Map modified from Wikimedia Commons (Asia Countries Gray)")
        return

    def do_quit(self, line):
        """Quit the game."""
        return True

    def preloop(self):
        title_print("=")

    def postloop(self):
        print("Thank you for playing Ilha Formosa!")

    def default(self, args):
        args = split_args(args)
        command_name = args[0]
        print("'{}' is not a known command. Type ? for a list of commands.".format(command_name))


if __name__ == "__main__":
    IlhaFormosa().cmdloop()
