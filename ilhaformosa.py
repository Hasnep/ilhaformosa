import cmd
import pyreadline  # used for tab completion

from title import *
from player import *
from commandsyntax import *


class IlhaFormosa(cmd.Cmd):
    def do_bank(self, input_arguments):
        """Check your balance and deposit or withdraw cash."""
        args = argument_parser(input_arguments, command_syntax["bank"])
        if args is None:
            return
        else:
            if "bank" in player.location.buildings:
                if len(args) == 0:
                    # TODO: Make this use a table
                    print("Interest rate: " + percent(player.bank_rate))
                    self.onecmd("cash")
                    return
                else:
                    self.onecmd(args["deposit/withdraw"] + " " + str(args["amount"]))
                    return
            else:
                print("There is no bank in {}.".format(player.location.name))
                return

    def do_borrow(self, input_arguments):
        """Borrows money from the moneylender."""
        args = argument_parser(input_arguments, command_syntax["borrow"])
        if args is None:
            return
        else:
            if "moneylender" in player.location.buildings:
                if args["amount"] == "max" or args["amount"] == "all":
                    borrow_amount = player.max_debt - player.debt
                else:
                    borrow_amount = args["amount"]
                player.move_cash(borrow_amount, "borrow")
                return
            else:
                print("There is no moneylender in {}.".format(player.location.name))
                return

    def do_buy(self, input_arguments):
        """Buy something from a shop."""
        args = argument_parser(input_arguments, command_syntax["buy"])
        if args is None:
            return
        else:
            product = args["product"]
            quantity = args["quantity"]
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

    def do_calendar(self, input_arguments):
        """Find out what the date is or what the date will be in the future."""
        args = argument_parser(input_arguments, command_syntax["calendar"])
        if args is None:
            return
        else:
            if len(args) == 0:
                print("It is {}.".format(day_to_date(player.day)))
                return
            else:
                print("In {} days it will be {}.".format(args["days"], day_to_date(player.day + args["days"])))
                return

    def do_cargo(self, input_arguments):  # TODO: Add cargo tetris? Add more detailed cargo management?
        """Show the fleet's current cargo."""
        args = argument_parser(input_arguments, command_syntax["cargo"])
        if args is None:
            return
        else:
            table_aligned_print(column_names=["owned"],
                                column_aligns=["r"],
                                row_keys=cargo.types,
                                column_dicts=[weight(player.cargo)],
                                show_header=True,
                                show_row_keys=True)
            print("")
            bar(player.get_cargo_weight(), player.get_cargo_capacity(), units=weight)

    def do_cash(self, input_arguments):  # TODO:  Use a flexitable
        """Show your current cash, bank balance and debt."""
        args = argument_parser(input_arguments, command_syntax["calendar"])
        if args is None:
            return
        else:
            table_aligned_print(
                column_names=["Item", "Value"],
                column_aligns=["r"],
                row_keys=["Cash", "Bank balance", "Debt", "Total"],
                column_dicts=[{
                    "Cash": money(player.cash),
                    "Bank balance": money(player.balance),
                    "Debt": money(player.debt),
                    "Total": money(player.total_money)
                }],
                show_header=False,
                show_row_keys=True
            )

    def do_credits(self, input_arguments):
        """Print the credits for the game."""
        args = argument_parser(input_arguments, command_syntax["credits"])
        if args is None:
            return
        else:
            print("Game by Hannes Smit (hasnep.github.io)")
            # print("Map modified from Wikimedia Commons (Asia Countries Gray)")
            return

    def do_debug(self, input_arguments):
        """Show internal information."""
        args = argument_parser(input_arguments, command_syntax["debug"])
        print("Location")
        print(" Name: " + player.location.name)
        print(" ID: " + player.location.id)
        print("Market")
        print(" Global values: " + str(cargo.global_values))
        print(" Local values: " + str(player.location.local_values))
        return

    def do_deposit(self, input_arguments):
        """Deposits money into a bank account."""
        args = argument_parser(input_arguments, command_syntax["deposit"])
        if args is None:
            return
        else:
            if "bank" in player.location.buildings:
                if args["amount"] == "max" or args["amount"] == "all":
                    deposit_amount = player.cash
                else:
                    deposit_amount = args["amount"]
                player.move_cash(deposit_amount, "deposit")
                return
            else:
                print("There is no bank in {}.".format(player.location.name))
                return

    def do_fleet(self, input_arguments):  # TODO: Turn this into a flexitable
        """Get information about a single ship or your whole fleet."""
        args = argument_parser(input_arguments, command_syntax["fleet"])
        if args is None:
            return
        else:
            if len(args) > 0:
                is_plural = len(player.fleet) != 1
                print("Your fleet has {} ship{}.".format(len(player.fleet), "s" * is_plural))
                print("")
                for k in player.fleet:
                    print_ship_information(k)
                    print("")
            else:
                ship_nickname = format_arg(args["ship name"])
                for k in player.fleet:
                    if ship_nickname == format_arg(k.nickname):
                        print_ship_information(k)
                        return
                print("Use fleet [ship name] to get information about a ship.")

    def complete_fleet(self, text, line, begidx, endidx):  # TODO: Add a more complex regex matching algorithm to return all matches
        """Tab completion for the fleet command."""
        return [format_arg(k.nickname) for k in player.fleet if format_arg(k.nickname).startswith(format_arg(text))]

    def do_help(self, input_arguments):
        """List all the available commands or show help for a specific command."""
        args = argument_parser(input_arguments, command_syntax["help"])
        if args is None:
            return
        else:
            if len(args) == 0:
                widest_command = max([len(command_name) for command_name in all_commands])
                print("All commands:")
                n_commands_per_line = math.floor(90/(widest_command+1))
                for line_of_commands in [all_commands[i:i + n_commands_per_line] for i in range(0, len(all_commands), n_commands_per_line)]:
                    print(" ".join([align_text(command_name, widest_command, "l") for command_name in line_of_commands]))
                print("Use help [command] to get more information about a command.")
                return
            else:
                def show_command_help(command_name,_self=self):
                    command_syntax_string = command_name
                    if command_name in command_syntax and len(command_syntax[command_name]) > 0:
                        selected_command_syntax = command_syntax[command_name]
                        for argument in selected_command_syntax:
                            if argument["required"]:
                                brackets = "<>"
                            else:
                                brackets = "[]"
                            command_syntax_string += " " + brackets[0] + argument["name"] + brackets[1]
                    print(command_syntax_string + " - " + getattr(_self, "do_" + command_name).__doc__)
                    return

                command_name = args["command"]
                if command_name == "all":
                    for command_name in all_commands:
                        show_command_help(command_name)
                    return
                else:
                    show_command_help(command_name)

    def do_look(self, input_arguments):
        """Look around the port you are currently in."""
        print("You are in {}.".format(player.location.name))
        print("There is a {}".format(", ".join(player.location.buildings)))

    def do_map(self, input_arguments):  # TODO: Add an argument to look at the buildings of a certain port.
        """List the locations on the map."""
        args = argument_parser(input_arguments, command_syntax["map"])
        if args is None:
            return
        else:
            print("You are in {}. Your map has these ports on it:".format(player.location.name))
            for port_id in all_port_ids:
                if player.location.id == port_id:
                    print("{} (current location)".format(player.location.name))
                else:
                    print("{} ({} nautical miles)".format(port_id_to_name(port_id), ports_distances[player.location.name][port_id_to_name(port_id)]))
            # TODO: Show an ascii map of the world.

    def do_market(self, input_arguments):
        """Get the market's prices or buy and sell cargo."""
        args = argument_parser(input_arguments, command_syntax["market"])
        if args is None:
            return
        else:
            if len(args) == 0:
                cargo.table_cargo_prices(player.location.local_prices, player.cargo)
                return
            else:
                if args["product"] in cargo.types:
                    self.onecmd(" ".join(args))
                    return
                else:
                    print("Buy a cargo: {}".format(", ".join(cargo.types)))
                    return

    def do_moneylender(self, input_arguments):
        """Borrow money or repay a debt."""
        args = argument_parser(input_arguments, command_syntax["moneylender"])
        if args is None:
            return
        else:
            if "moneylender" in player.location.buildings:
                if len(args) == 0:
                    # TODO: Make this use a table
                    print("Interest rate: " + percent(player.lend_rate))
                    self.onecmd("cash")
                    return
                else:
                    self.onecmd(args["borrow/repay"] + " " + str(args["amount"]))
                    return
            else:
                print("There is no moneylender in {}.".format(player.location.name))
                return

    def do_options(self, input_arguments):
        """View or modify an option or reset all options to default."""
        args = argument_parser(input_arguments, command_syntax["options"])
        if args is None:
            return
        else:
            if len(args) == 0:
                options.print_all_options()
                return
            else:
                option_name = args["option"]
                if len(args) == 1:
                    if option_name == "default":
                        options.reset_all_options()
                        return
                    else:
                        options.print_option(option_name)
                        return
                else:
                    option_value = args["value"]
                    if option_value == "default":
                        options.reset_option(option_name)
                        return
                    else:
                        options.set_option(option_name, option_value)
                        return

    def complete_options(self, text, line, begidx, endidx):
        """Tab completion for the options command."""
        args = split_args(line)
        if len(args) == 1:
            return [option_name for option_name in {**options.choices, **{"default":[]}}]
        elif len(args) == 2:
            return [option_name for option_name in {**options.choices, **{"default":[]}} if option_name.startswith(text)]
        elif len(args) == 3 and args[1] in options.choices:
            option_name = args[1]
            return [option_choice for option_choice in options.choices[option_name] + ["default"] if option_choice.startswith(text)]
        else:
            return []

    def do_quit(self, input_arguments):
        """Quit the game."""
        args = argument_parser(input_arguments, command_syntax["quit"])
        if args is None:
            return
        else:
            return True

    def do_rename(self, input_arguments):
        """Rename a ship."""
        args = split_args(input_arguments, ">")
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

    def do_repay(self, input_arguments):
        """Repays money to the moneylender."""
        args = argument_parser(input_arguments, command_syntax["borrow"])
        if args is None:
            return
        else:
            if "moneylender" in player.location.buildings:
                if args["amount"] == "max" or args["amount"] == "all":
                    repay_amount = player.debt
                else:
                    repay_amount = args["amount"]
                player.move_cash(repay_amount, "repay")
                return
            else:
                print("There is no moneylender in {}.".format(player.location.name))
                return

    def do_sail(self, input_arguments):
        """Set sail for a port."""
        args = argument_parser(input_arguments, command_syntax["sail"])
        if args is None:
            return
        else:
            destination_id = args["destination"]
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
                    arriving_port = destination_port
                    # before leaving
                    departing_port.visited = player.day
                    # while travelling
                    journey_distance = ports_distances[departing_port.name][arriving_port.name]
                    journey_speed = 8  # TODO: Change this to top speed.
                    journey_time = int(math.ceil(journey_distance / 8)/24)
                    cargo.global_values = cargo.randomise_values(cargo.global_values, journey_time)
                    player.day += journey_time
                    print("You sail {} nautical miles at {} knots for {} day{}.".format(journey_distance, journey_speed, math.floor(journey_time),(math.floor(journey_time) >1)*"s"))
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

    def do_shipyard(self, input_arguments):
        # TODO: add a buy argument to the shipyard and make the buy command call this
        # TODO: add a repair argument with an all/max subcommand
        """Look at what's for sale in the shipyard."""
        args = argument_parser(input_arguments, command_syntax["shipyard"])
        if args is None:
            return
        else:
            if "shipyard" in player.location.buildings:
                if player.location.for_sale_ship is None:
                    print("There are no ships for sale here.")
                    return
                else:
                    # TODO: Change to flexitable
                    print("Price: " + money(player.location.for_sale_ship_price))
                    print_ship_information(player.location.for_sale_ship)
                    return
            else:
                print("There is no shipyard in {}.".format(player.location.name))
                return

    def do_wait(self, input_arguments):
        """Wait for a specified number of days."""
        args = argument_parser(input_arguments, command_syntax["wait"])
        if args is None:
            return
        else:
            n_days = args["days"]
            player.day += n_days
            print("You wait around for {} days.".format(n_days))
            return

    def do_withdraw(self, input_arguments):
        """Withdraws money from a bank account."""
        args = argument_parser(input_arguments, command_syntax["withdraw"])
        if args is None:
            return
        else:
            if "bank" in player.location.buildings:
                if args["amount"] == "max" or args["amount"] == "all":
                    withdraw_amount = player.balance
                else:
                    withdraw_amount = args["amount"]
                player.move_cash(withdraw_amount, "withdraw")
                return
            else:
                print("There is no bank in {}.".format(player.location.name))
                return

    # replace cmd defaults
    prompt = '\n > '  # set the prompt

    def default(self, input_arguments):
        """Unrecognised command."""
        command_name = split_args(input_arguments)[0]
        print("'{}' is not a known command. Type ? for a list of commands.".format(command_name))

    def preloop(self):
        title_print()

    def postloop(self):
        print("Thank you for playing Ilha Formosa!")


if __name__ == "__main__":
    IlhaFormosa().cmdloop()
