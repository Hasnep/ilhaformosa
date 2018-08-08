from ilhaformosa import *

test_instance = IlhaFormosa()

test_commands = """
help
bank
borrow 10
buy food
buy ship
calendar
cal 10
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
repay all
sail naha
shipyard
wait 1
withdraw max
"""

for command in test_commands.split("\n")[1:-1]:
    test_instance.onecmd(command)