#!/usr/bin/python3
""" subaction_tables.py
"""

import json
from sys import argv
from hexdump import hexdump
from struct import pack,unpack

# Definitions and resources specific to GALE01 NTSC-U v1.02
from ntsc102_defs import *

from ramdump_util import *


# Each entry is a function, from subaction ID 0x28 - 0xe8
base = 0x803c06e8
functions = {}

for subaction in (subactionID):
    subaction_id = subaction.value
    addr = getptr(ram, base)

    if (validptr(addr)):
        size = getsymbolsize(addr)
        new_name = "Subaction_Event_0x{:03x}".format(subaction_id)
        entry = {'addr': addr, 'size': size, 'name': new_name }
        # If the function appears unique, add it to the list of output
        if (functions.get(addr) == None):
            functions[addr] = entry
        else:
            print("Duplicate entry for addr {:08x}".format(addr))
            print(json.dumps(entry))
            print(json.dumps(functions[addr]))

    # Go to the next pointer in the list
    base += 0x4

# Print symbols to standard output
for addr in functions:
    size = functions[addr]['size']
    name = functions[addr]['name']
    print(MAPFMT.format(addr, size, addr, name))
