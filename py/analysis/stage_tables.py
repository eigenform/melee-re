#!/usr/bin/python3
""" stage_tables.py
"""

import json
from sys import argv
from hexdump import hexdump
from struct import pack,unpack

# Definitions and resources specific to GALE01 NTSC-U v1.02
from ntsc102_defs import *

from ramdump_util import *

class stage_ft(function_table):
    """ Representation of a stage function table. """
    def __init__(self, *args, **kwargs):
        super(stage_ft, self).__init__(*args, **kwargs)
        self.idx = self.data[0]
        self.subtable = self.data[1]
        self.functions = {
                'stageInit': self.data[3],
                'unk1': self.data[4],
                'onLoad': self.data[5],
                'onGO': self.data[6],
                'unk3': self.data[7],
                'unk4': self.data[8],
                'unk5': self.data[9],
        }


base = 0x803dfedc
functions = {}
for stage in (stageInternal):

    # Skip the first two entries in the array (no idea what they are)
    if ((stage.value == 0x00) or (stage.value == 0x01)):
        base += 0x4
        continue

    # Get the pointer to the entry and retrieve the functions
    ptr = getptr(ram, base)
    if (ptr == 0x00000000):
        base += 0x4
        continue
    ft = stage_ft(u32table(dump(ptr, 0x34)))

    # Construct an entry for each function
    for funcname in ft.functions:
        addr = ft.functions[funcname]
        if (validptr(addr)):
            size = getsymbolsize(addr)
            new_name = "{}_{}_{}".format("Stage", stage.name, funcname)
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
