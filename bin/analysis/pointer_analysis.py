#!/usr/bin/python3
""" pointer_analysis.py - Walk though all pointers in some ramdump
"""

import json
from sys import argv
from hexdump import hexdump
from struct import pack,unpack
from ntsc102_defs import *
from ramdump_util import *

MAX_DEPTH = 30

cursor = 0x80000000
while (cursor < 0x817fffff):
    isPtr = None
    symbol = None

    ''' If this address is a function, skip it '''

    size = getsymbolsize(cursor)
    symbol = symbolmap.get(cursor)
    if (symbol):
        cursor += symbol['size']
        continue

    ''' Get the value at this address '''

    val = getword(ram, cursor)

    pointer = val
    depth = 0
    indent = " "

    ''' If the value is potentially a pointer, walk it up to MAX_DEPTH  '''

    while (validptr(pointer)):
        symbol = symbolmap.get(pointer)

        # Bottom out at function pointers
        if (symbol):
            print("{}0x{:08x}: {}".format(indent, pointer, symbol['name']))
            break

        if (depth > MAX_DEPTH):
            print("{}Truncated at {} references".format(indent, MAX_DEPTH))
            break

        # Get the new value
        newval = getword(ram, pointer)
        #print("{}0x{:08x}: {:08x}".format(indent, pointer, newval))

        if (validptr(newval)):
            print("{}0x{:08x}: {:08x}".format(indent, pointer, newval))

        pointer = newval
        depth += 1
        indent += " "


    cursor += 4
