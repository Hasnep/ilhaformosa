import cmd, textwrap, pyreadline
# from pdb import * # use set_trace() to debug
from ships import *
from ports import *

SCREEN_WIDTH = 80

myFleet = [Junk()]
myLocation = world["taipei"]


def set_sail(destination):
    """A helper function that travels to a location."""
    print("You set sail for %s" % world[destination].name)
    print(world[destination].landing_message)
    print(world[destination].description)
    return world[destination]


def rename_ship(old_nickname, new_nickname):
    """A function that changes the nickname of a ship."""
    for k in myFleet:
        if k.nickname == old_nickname:
            k.nickname = new_nickname


class IlhaFormosa(cmd.Cmd):
    prompt = '\n> '

    def do_map(self, line):
        """List the locations on the map."""
        print("You are in %s" % myLocation.name)
        print("The map has these ports on it:")
        for key, value in world.items():
            print(value.name)

    def do_look(self, line):
        """Look around the port you are currently in."""
        print("You are in %s" % myLocation.name)
        print("There is a ")
        for k in myLocation.buildings:
            print(k.type)

    def do_sail(self, destination):
        """Set sail for a port.
        sail [destination]"""
        myLocation = set_sail(destination)

    def complete_sail(self, text, line, begidx, endidx):
        return [key for key, value in world.items() if key.startswith(text)]

    def do_rename(self, nicknames):
        """Rename a ship.
        rename [old name]>[new name]"""
        nicknames = nicknames.split(">")
        if len(nicknames) != 2:
            print("Use [old name]>[new name] to rename a ship.")
        else:
            rename_ship(nicknames[0], nicknames[1])
            print("%s is now named %s" % (nicknames[0], nicknames[1]))

    def do_fleet(self, line):
        """Get information about your fleet."""
        print("Your fleet has %s ship(s)" % len(myFleet))
        for k in myFleet:
            print_ship_information(k)

    def do_quit(self, line):
        """Quit the game."""
        return True


print('Ilha Formosa')
IlhaFormosa().cmdloop()
print('Thank you for playing Ilha Formosa!')
