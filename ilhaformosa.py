import cmd, textwrap
from ships import *
from ports import *


SCREEN_WIDTH = 80


myFleet = []
myFleet.append(Junk())
myLocation = world["taipei"]
print(myLocation)


def set_sail(destination):
    """A helper function that travels to a location."""
    print("You set sail for %s" % world[destination].name)
    print(world[destination].landing_message)
    print(world[destination].description)
    return world[destination]


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
        """Set sail for a port."""
        myLocation = set_sail(destination)

    def do_fleet(self, line):
        """Get information about your fleet"""
        print("Your fleet has %s ship(s)" % len(myFleet))
        for k in myFleet:
            print(k.information)

    def do_quit(self, line):
        return True


print('Ilha Formosa')
IlhaFormosa().cmdloop()
print('Thank you for playing Ilha Formosa!')
