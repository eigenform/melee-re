#!/usr/bin/python3
""" ramdump_util.py
Helper functions for doing some operations on a Dolphin ram dump.
When you import this, your script will automatically:

    - Attempt to read some ram.raw from the current working directory
    - Attempt to read some GALE01.map from the current working directory

Maybe I'll do this a different way sometime in the future.
"""

from struct import pack, unpack

class function_table(object):
    """ Simple containter to hold data about some function table.
    We expect that some other script will override this with a more specifc
    definition, depending on exactly what part of memory we're looking at.
    """
    def __init__(self, data, table_name=None):
        self.data = data
        self.table_name = table_name
        self.functions = {}


# When you import this script, you should inherit these. 
symbols = None
ram = None

# Format string for Dolphin map files
MAPFMT = "{:08x} {:08x} {:08x} 0 {}"

# -----------------------------------------------------------------------------
# Helper functions go here

def getptr(data, offset):
    """ Return the pointer at some offset in the given bytearray """
    return getword(data, offset)

def getword(data, offset):
    """ Return the pointer at some offset in the given bytearray """
    return unpack(">L", data[to_off(offset):to_off(offset+4)])[0]

def to_off(addr):
    """ Translate from an address to an offset into the ram dump """
    return (addr & 0x01ffffff)

def u32table(data):
    """ Convert some binary data into a table of u32s """
    table = []
    if (len(data) % 4 != 0):
        print("arg to u32table() call must be divisible by 4")

    off = 0
    for i in range((len(data) // 4)):
        table.append(unpack(">L", data[off:off+4])[0])
        off += 4
    return table

def genericname(addr):
    return "zz_{:06x}".format(addr & 0x00ffffff)

def validptr(ptr):
    if ((ptr == 0) or (ptr < 0x80000000) or (ptr > 0x817fffff)):
        return None
    else:
        return True

def dump(addr, length):
    """ Return a bytearray from some location in ram """
    return ram[to_off(addr):to_off(addr+length)]

def getsymbol(addr):
    """ Return the symbol name corresponding to some address in the map. """
    for symbol in symbols:
        if (addr == symbol[0]):
            return symbol[2]
    return None

def getsymbolsize(addr):
    """ Return the size of the symbol name in the map """
    for symbol in symbols:
        if (addr == symbol[0]):
            return symbol[1]


# -----------------------------------------------------------------------------
# Try to read in a Dolphin ram-dump and GALE01 symbol map.
# There's no error-handling here right now.

with open("ram.raw", "rb") as f:
    ram = f.read()

with open("GALE01.map", "r") as f:
    symbols = []
    for line in f:
        symbol = []
        line = line.strip()
        entry = line.split(" ")
        if ((entry[0] == '') or (entry[0] == '.text') or (entry[0] == '.data')):
            continue
        symbol = [int(entry[0], 16), int(entry[1], 16), entry[4]]
        symbols.append(symbol)

