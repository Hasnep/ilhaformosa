from ilhaformosa import *

test_instance = IlhaFormosa()

test_commands = """
help
bank
borrow 10
buy food
buy ship
buy tea 2
buy jade all
calendar
calendar 10
cargo
cash
credits
deposit 10
fleet
look
map
market
moneylender
options
options currency
options currency dollar
options currency default
options default
repay all
sail naha
shipyard
wait 1
withdraw max
spooble
"""

for command in test_commands.split("\n")[1:-1]:
    test_instance.onecmd(command)