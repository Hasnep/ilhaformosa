import math

from options import *
from cargo import *

all_commands = sorted(
    ["bank", "borrow", "buy", "calendar", "cargo", "cash", "credits", "deposit", "fleet", "help", "look", "map",
     "market", "moneylender", "options", "quit", "rename", "repay", "sail", "shipyard", "wait", "withdraw"]
)

command_syntax = {
    "help": [
        {
            "name": "command",
            "type": "string",
            "required": False,
            "valid_values": all_commands + ["all"]
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
            "name": "quantity/all/max",
            "type": "integer",
            "required": False,
            "valid_values": (1, math.inf, ["all", "max"]),
            "default": 1
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
    "calendar": [
        {
            "name": "days",
            "type": "integer",
            "required": False,
            "valid_values": (1, 365 * 10),
            "error_wrong_type": "Use calendar [days] to find out what the date will be in the future.",
            "error_too_high": "Your calendar only has pages for the next 10 years."
        }
    ]
}
