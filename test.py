from ilhaformosa import *

test_instance = IlhaFormosa()

test_commands = """
help
help bank
help all

asdf

bank
bank asdf
bank deposit
bank deposit 0
bank deposit 1
bank withdraw 1

borrow
borrow asdf
borrow 0
borrow 10

buy
buy asdf
buy food
buy food 0
buy food 2
buy ship
buy tea
buy tea 2
buy jade all

calendar
calendar asdf
calendar 0
calendar 10

cargo

cash

credits

deposit
deposit asdf
deposit 0
deposit 10
deposit all
withdraw all

fleet

look

map

market

moneylender
moneylender asdf
moneylender borrow
moneylender borrow 0
moneylender borrow 1
moneylender repay 1

options
options asdf
options currency asdf
options currency
options currency dollar
options currency default
options default

repay all

sail
sail naha

shipyard

wait 1

withdraw
withdraw asdf
withdraw 0
withdraw 10
withdraw all
"""

for command in test_commands.split("\n")[1:-1]:
    if command == "":
        print("=" * 80)
    else:
        print(" > " + command)
        test_instance.onecmd(command)
