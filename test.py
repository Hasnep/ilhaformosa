from ilhaformosa import *

test_instance = IlhaFormosa()

test_commands = """
deposit 10
withdraw 10
borrow 10
repay 10
sail naha
"""

for command in test_commands.split("\n")[1:-1]:
    test_instance.onecmd(command)