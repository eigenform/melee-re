#!/usr/bin/python3
""" char_specific_as.py - Dump symbols from char-specific action-state tables
"""

import json
from sys import argv
from hexdump import hexdump
from struct import pack,unpack

# Definitions and resources specific to GALE01 NTSC-U v1.02
from ntsc102_defs import *

from ramdump_util import *

# Final dict of functions
functions = {}

class char_ft(function_table):
    def __init__(self, *args, **kwargs):
        super(char_ft, self).__init__(*args, **kwargs)
        self.functions = {}
        for i in (charInternal):
            self.functions[i.value] = self.data[i.value]


def prefer_char(old_entry, new_entry):
    """ In this context, there are lots of instances where certain functions
    are duplicates from one character to another. This encodes something about
    the way particular characters are implemented, in this situation. In this 
    case, prefer the "original" character over the "cloned" character.
    """

    old_id = old_entry['char_id']
    new_id = new_entry['char_id']

    pairs = [ 
        (charInternal.DrMario.value , charInternal.Mario.value ),
        (charInternal.Roy.value , charInternal.Marth.value ),
        (charInternal.Ganondorf.value , charInternal.CaptainFalcon.value ),
        (charInternal.GigaBowser.value , charInternal.Bowser.value ),
        (charInternal.YoungLink.value , charInternal.Link.value ), 
        (charInternal.Falco.value , charInternal.Fox.value ),
        (charInternal.Nana.value , charInternal.Popo.value ),
        (charInternal.Pichu.value , charInternal.Pikachu.value ),
    ]

    for pair in pairs:
        if ((old_id == pair[0]) and (new_id == pair[1])):
            return new_entry
    for pair in pairs:
        if ((new_id == pair[0]) and (old_id == pair[1])):
            return old_entry
    return None


def prefer_table(old_entry, new_entry):
    """ 
    In some situations, functions are also duplicated across these tables.
    The "function" of the functions in these tables must be internally related
    enough for them to be re-used in certain cases. This probably indicates
    that there are a better set of names for these tables/functions.
    """

    old_func = old_entry['function_name']
    new_func = new_entry['function_name']

    # prefer "onItemPickup" as a name
    if ((old_func == "onMakeItemCatch") and (new_func == "onItemPickup")):
        return new_entry
    if ((new_func == "onMakeItemCatch") and (old_func == "onItemPickup")):
        return old_entry
    # prefer "onMakeItemDrop" as a name
    if ((old_func == "onMakeItemDrop") and (new_func == "unkItemRelated")):
        return old_entry
    if ((new_func == "onMakeItemDrop") and (old_func == "unkItemRelated")):
        return new_entry
    return None


def pull_symbols(ft):
    # Construct an entry for each function
    for charidx in ft.functions:
        addr = ft.functions[charidx]
        charname = charInternal(charidx).name

        # Ignore entries with invalid addresses
        if (validptr(addr)):

            # Rely on the arguments to char_ft() to give us a name for the
            # function here. In this case, the 'table_name' is used as the 
            # name of each function in that particular table.

            size = getsymbolsize(addr)
            new_name = "{}_{}_{}".format("AS", charname, ft.table_name)
            entry = {'addr': addr, 'size': size, 'name': new_name, 'char_id': charidx,
                    'function_name': ft.table_name}

            # If the function appears unique, add it to the list of output
            if (functions.get(addr) == None):
                functions[addr] = entry
                continue

            # If functions aren't unique, try to resolve the issue
            else:
                # Duplicates across character in a table
                preferred = prefer_char(functions.get(addr), entry)
                if (preferred != None):
                    functions[addr] = preferred
                    continue

                # Duplicates across table
                preferred = prefer_table(functions.get(addr), entry)
                if (preferred != None):
                    functions[addr] = preferred
                    continue
                else:
                    print(json.dumps(entry))
                    print(json.dumps(functions.get(addr)))



# Remember that, if you change the names of these tables (and thus, the names 
# of the functions in those tables), you'll need to change the strings that
# you're comparing in the functions used for pruning duplicate symbols.


# These are all adjacent, related to B moves
ft = char_ft(u32table(dump(0x803c13e8, 0x84)), table_name="GroundSideB")
pull_symbols(ft)
ft = char_ft(u32table(dump(0x803c146c, 0x84)), table_name="UpB")
pull_symbols(ft)
ft = char_ft(u32table(dump(0x803c14f0, 0x84)), table_name="AerialDownB")
pull_symbols(ft)
ft = char_ft(u32table(dump(0x803c1574, 0x84)), table_name="Unk1BMove")
pull_symbols(ft)
ft = char_ft(u32table(dump(0x803c15f8, 0x84)), table_name="AerialNeutralB")
pull_symbols(ft)
ft = char_ft(u32table(dump(0x803c167c, 0x84)), table_name="GroundNeutralB")
pull_symbols(ft)
ft = char_ft(u32table(dump(0x803c1700, 0x84)), table_name="GroundDownB")
pull_symbols(ft)
ft = char_ft(u32table(dump(0x803c1784, 0x84)), table_name="Unk2BMove")
pull_symbols(ft)

# These are all adjacent and related to item behaviour
ft = char_ft(u32table(dump(0x803c1808, 0x84)), table_name="onAbsorb")
pull_symbols(ft)
ft = char_ft(u32table(dump(0x803c188c, 0x84)), table_name="onItemPickup")
pull_symbols(ft)
ft = char_ft(u32table(dump(0x803c1910, 0x84)), table_name="onMakeItemInvisible")
pull_symbols(ft)
ft = char_ft(u32table(dump(0x803c1994, 0x84)), table_name="onMakeItemVisible")
pull_symbols(ft)
ft = char_ft(u32table(dump(0x803c1a18, 0x84)), table_name="onMakeItemDrop")
pull_symbols(ft)
ft = char_ft(u32table(dump(0x803c1a9c, 0x84)), table_name="onMakeItemCatch")
pull_symbols(ft)
ft = char_ft(u32table(dump(0x803c1b20, 0x84)), table_name="unkItemRelated")
pull_symbols(ft)

ft = char_ft(u32table(dump(0x803c1ba4, 0x84)), table_name="unkPika1")
pull_symbols(ft)
ft = char_ft(u32table(dump(0x803c1c28, 0x84)), table_name="unkPika2")
pull_symbols(ft)
ft = char_ft(u32table(dump(0x803c1cac, 0x84)), table_name="onHit")
pull_symbols(ft)
ft = char_ft(u32table(dump(0x803c1d30, 0x84)), table_name="onUnk")
pull_symbols(ft)
ft = char_ft(u32table(dump(0x803c1db4, 0x84)), table_name="unk_")
pull_symbols(ft)
ft = char_ft(u32table(dump(0x803c1e38, 0x84)), table_name="chargeNeutralB")
pull_symbols(ft)
ft = char_ft(u32table(dump(0x803c1ebc, 0x84)), table_name="onRespawn")
pull_symbols(ft)

ft = char_ft(u32table(dump(0x803c21d4, 0x84)), table_name="unkJump2")
pull_symbols(ft)


# Print symbols to standard output
for addr in functions:
    size = functions[addr]['size']
    name = functions[addr]['name']
    print(MAPFMT.format(addr, size, addr, name))
