import math

from options import *
from cargo import *
from ports import *

all_commands = ["bank", "borrow", "buy", "calendar", "cargo", "cash", "credits", "deposit", "fleet", "help", "look",
                "map", "market", "moneylender", "options", "quit", "rename", "repay", "sail", "shipyard", "wait",
                "withdraw"]

command_syntax = {
    "bank": [
        {
            "name": "deposit/withdraw",
            "type": "string",
            "required": False,
            "valid_values": ["deposit", "withdraw"]
        },
        {
            "name": "amount",
            "type": "integer",
            "required": False,
            "valid_values": (1, math.inf, ["max", "all"])
        }
    ],
    "borrow": [
        {
            "name": "amount",
            "type": "integer",
            "required": True,
            "valid_values": (1, math.inf, ["max", "all"])
        }
    ],
    "buy": [
        {
            "name": "product",
            "type": "string",
            "required": True,
            "valid_values": ["food", "ship"] + cargo.types
        },
        {
            "name": "quantity",
            "type": "integer",
            "required": False,
            "valid_values": (1, math.inf, ["all", "max"]),
            "default": 1
        }
    ],
    "calendar": [
        {
            "name": "days",
            "type": "integer",
            "required": False,
            "valid_values": (1, 365 * 10),
            "error_wrong_type": "Use calendar [days] to find out what the date will be in the future.",
            "error_too_high": "Your calendar only has pages for the next 10 years."
        }
    ],
    "cargo": [],
    "cash": [],
    "credits": [],
    "debug": [],
    "deposit": [
        {
            "name": "amount",
            "type": "integer",
            "required": True,
            "valid_values": (1, math.inf, ["max", "all"])
        }
    ],
    "fleet": [
        {
            "name": "ship",
            "type": "string",
            "required": False,
            "default": "all"
        }
    ],
    "help": [
        {
            "name": "command",
            "type": "string",
            "required": False,
            "valid_values": all_commands + ["all"]
        }
    ],
    "look": [],
    "map": [],
    "market": [
        {
            "name": "buy/sell",
            "type": "string",
            "required": False,
            "valid_values": ["buy", "sell"]
        },
        {
            "name": "product",
            "type": "string",
            "required": False,
            "valid_values": ["food", "ship"] + cargo.types
        },
        {
            "name": "quantity",
            "type": "integer",
            "required": False,
            "valid_values": (1, math.inf, ["all", "max"]),
            "default": 1
        }
    ],
    "moneylender": [
        {
            "name": "borrow/repay",
            "type": "string",
            "required": False,
            "valid_values": ["borrow", "repay"]
        },
        {
            "name": "amount",
            "type": "integer",
            "required": False,
            "valid_values": (1, math.inf, ["max", "all"])
        }
    ],
    "options": [
        {
            "name": "option",
            "type": "string",
            "required": False,
            "valid_values": [option_name for option_name in options.choices] + ["default"]
        },
        {
            "name": "value",
            "type": "string",
            "required": False
        }
    ],
    "quit": [],
    "rename": [
        {
            "name": "old name>new name",
            "type": "string",
            "required": True
        }
    ],
    "repay": [
        {
            "name": "amount",
            "type": "integer",
            "required": True,
            "valid_values": (1, math.inf, ["max", "all"])
        }
    ],
    "sail": [
        {
            "name": "destination",
            "type": "string",
            "required": True,
            "valid_values": all_port_ids,
            "missing_value":"Use sail [destination] to sail to a port. You can see a list of ports using the map command.",
            "invalid_value": "{} is not a port on your map. You can see a list of ports using the 'map' command."
        }
    ],
    "shipyard": [
        {
            "name": "buy/sell",
            "type": "string",
            "required": False,
            "valid_values": ["buy", "sell"]
        },
        {"name": "ship name",
         "type": "string",
         "required": False
         }
    ],
    "wait": [
        {
            "name": "days",
            "type": "integer",
            "required": False,
            "valid_values": (1, 7),
            "default": 1,
            "too_big": "You can only wait for one week at a time.",
            "too_small": "You cannot go back in time."
        }
    ],
    "withdraw": [
        {"name": "amount",
         "type": "integer",
         "required": True,
         "valid_values": (1, math.inf, ["max", "all"])
         }
    ]
}

commands_no_syntax = [command_name for command_name in all_commands if command_name not in command_syntax]
if commands_no_syntax:
    raise ValueError("Commands in list but without syntax: {}".format(", ".join(commands_no_syntax)))
