#!/usr/bin/python3
""" char_specific_anim.py
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

class anim_ft(function_table):
    def __init__(self, *args, **kwargs):
        super(anim_ft, self).__init__(*args, **kwargs)
        self.idx = self.data[0]
        self.functions = {
            'animInterrupt': self.data[3],
            'IASAInterrupt': self.data[4],
            'actionPhysics': self.data[5],
            'collisionInterrupt': self.data[6],
            'cameraBehaviour': self.data[7],
        }

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
        (charInternal.Luigi.value , charInternal.Mario.value ),
        (charInternal.Samus.value , charInternal.Link.value ),

        # Interestingly, for these particular arrays, it looks like:
        #   - Young Link and Samus share some interrupt functions 
        #   - Jigglypuff and Kirby share some interrupt functions

        (charInternal.Jigglypuff.value , charInternal.Kirby.value ),
        (charInternal.YoungLink.value , charInternal.Samus.value ),
    ]

    for pair in pairs:
        if ((old_id == pair[0]) and (new_id == pair[1])):
            return new_entry
    for pair in pairs:
        if ((new_id == pair[0]) and (old_id == pair[1])):
            return old_entry
    return None




# Walk the array of pointers to anim_ft arrays, starting at 0x803c12e0.
# These are indexed by the internal character ID. The length of each array 
# is variable, and it's not clear where this is determined in-memory or 
# in the actual code yet.

base = 0x803c12e0
functions = {}
unsorted_functions = []

for char in (charInternal):
    charname = char.name
    charidx = char.value

    # Get the pointer to the variable-length array of function tables
    array_ptr = getptr(ram, base)

    if (validptr(array_ptr)):
        # Walk the array until we run up on an invalid entry
        while(True):
            ft = anim_ft(u32table(dump(array_ptr, 0x20)))

            # Just disreguard entries where the anim_id is -1, for now. 
            if (ft.idx == 0xffffffff):
                array_ptr += 0x20
                continue

            # Basically, the only reliable way I can see to determine an entry
            # is garbage is to see if the index field is out of bounds
            if (validptr(ft.data[0]) or (ft.idx > 0x200)):
                    break



            # Construct an entry for each function, but don't do pruning
            # until after we've iterated over all possible tables. 
            # This will make pruning duplicates a lot easier for us.

            for funcname in ft.functions:
                addr = ft.functions[funcname]
                if (validptr(addr)):
                    size = getsymbolsize(addr)
                    #new_name = "AS_{}_AnimID{:03x}_{}".format(charname, 
                    #       ft.idx, funcname)


                    new_name = "AS_{}_AnimID{:03x}_{}".format(
                            charname, ft.idx, funcname)
                    entry = {'addr': addr, 'size': size, 'name': new_name,
                            'anim_id': ft.idx, 'char_id': charidx }
                    unsorted_functions.append(entry)

            # Go to the next entry
            array_ptr += 0x20

    # Go to the next pointer (next array)
    base += 0x4




# Prune certain duplicates from the list here. There are a lot of these. 
# Especially within kirby's table, and across anim_id's that are not adjacent.
# Marth also has a lot of confusing ones. This entire loop is bascially a way
# of hacking around the fact that we haven't enumerated all animIds for each
# character and associated them with some "higher-level" thing. 
#
# The fact that there are many-to-one mappings from "not-adjacent" animIDs
# to some function/s reveals something about the way certain things are 
# implemented, and probably that some of those interrupts deserve more generic 
# names). We can't account for that right now, so just prune symbols instead.

sorted_functions = []
for idx, entry in enumerate(unsorted_functions):
    anim_id = entry['anim_id']
    char_id = entry['char_id']
    funcname = entry['name']

    # Fox AnimID 0x141-0x146 tables are equivalent
    ran = [i for i in range(0x142, 0x146+1)]
    if ((anim_id in ran) and (char_id == charInternal.Fox.value)):
        del unsorted_functions[idx]
        continue

    # DonkeyKong AnimID 0x128-0x12a Interrupts
    # DonkeyKong AnimID 0x132-0x134 Interrupts
    # DonkeyKong AnimID 0x13b-0x13e Interrupts
    ran = [i for i in range(0x129, 0x12a+1)]
    ran += [i for i in range(0x133,0x134+1)]
    ran += [i for i in range(0x13c,0x13e+1)]
    if ((anim_id in ran) and (char_id == charInternal.DonkeyKong.value)):
        del unsorted_functions[idx]
        continue

    # Bowser AnimID 0x12e-0x12f Interrupts
    # Bowser AnimID 0x133-0x134 Interrupts
    if ((anim_id == 0x12f) and (char_id == charInternal.Bowser.value)):
        del unsorted_functions[idx]
        continue
    if ((anim_id == 0x134) and (char_id == charInternal.Bowser.value)):
        del unsorted_functions[idx]
        continue

    # Peach AnimID 0x044-0x048 Interrupts
    # Peach AnimID 0x12a-0x12c Interrupts
    ran = [i for i in range(0x045, 0x048+1)]
    ran += [i for i in range(0x12b,0x12c+1)]
    if ((anim_id in ran) and (char_id == charInternal.Peach.value)):
        del unsorted_functions[idx]
        continue

    # Peach AnimID 0x128-0x129 Interrupts
    # Peach AnimID 0x132-0x133 Interrupts
    if ((anim_id == 0x129) and (char_id == charInternal.Peach.value)):
        del unsorted_functions[idx]
        continue
    if ((anim_id == 0x133) and (char_id == charInternal.Peach.value)):
        del unsorted_functions[idx]
        continue

    # Ness AnimID 0x12c-0x12d Interrupts
    # Ness AnimID 0x130-0x131 Interrupts
    if ((anim_id == 0x12d) and (char_id == charInternal.Ness.value)):
        del unsorted_functions[idx]
        continue
    if ((anim_id == 0x131) and (char_id == charInternal.Ness.value)):
        del unsorted_functions[idx]
        continue


    # DRMario AnimID 0x0ef-0x0f0 Interrupts
    if ((anim_id == 0x0f0) and (char_id == charInternal.DrMario.value)):
        del unsorted_functions[idx]
        continue

    # Young Link AnimID 0x0ef-0x0f0 Interrupts
    if ((anim_id == 0x0f0) and (char_id == charInternal.YoungLink.value)):
        del unsorted_functions[idx]
        continue

    # GameNWatch AnimID 0x129-0x131 Interrupts
    # GameNWatch AnimID 0x132-0x13a Interrupts
    ran = [i for i in range(0x12a, 0x131+1)]
    ran += [i for i in range(0x133,0x13a+1)]
    if ((anim_id in ran) and (char_id == charInternal.MrGameNWatch.value)):
        del unsorted_functions[idx]
        continue

    # Jigglypuff AnimID 0x12c-0x12d Interrupts
    # Jigglypuff AnimID 0x132-0x133 Interrupts
    # Jigglypuff AnimID 0x134-0x135 Interrupts
    # Jigglypuff AnimID 0x13a-0x13b Interrupts
    if ((anim_id == 0x12d) and (char_id == charInternal.Jigglypuff.value)):
        del unsorted_functions[idx]
        continue
    if ((anim_id == 0x133) and (char_id == charInternal.Jigglypuff.value)):
        del unsorted_functions[idx]
        continue
    if ((anim_id == 0x135) and (char_id == charInternal.Jigglypuff.value)):
        del unsorted_functions[idx]
        continue
    if ((anim_id == 0x13b) and (char_id == charInternal.Jigglypuff.value)):
        del unsorted_functions[idx]
        continue


    # Kirby AnimID 0x137-0x139 Interrupts
    ran = [i for i in range(0x138, 0x139+1)]
    if ((anim_id in ran) and (char_id == charInternal.Kirby.value)):
        del unsorted_functions[idx]
        continue

    # Interrupts with AnimID0x127-0x130 for Kirby and Puff are all equivalent. 
    # Puff is considered a clone of Kirby in the context of this table, so 
    # Puff's functions will be pruned later on this script

    # Kirby AnimID 0x127-0x130 Interrupts
    ran = [i for i in range(0x128, 0x130+1)]
    if ((anim_id in ran) and (char_id == charInternal.Kirby.value)):
        del unsorted_functions[idx]
        continue

    # Kirby AnimID 0x173-0x174 Interrupts
    # Kirby AnimID 0x177-0x178 Interrupts
    # Kirby AnimID 0x19a-0x19b Interrupts
    # Kirby AnimID 0x1a0-0x1a1 Interrupts
    # Kirby AnimID 0x1a2-0x1a3 Interrupts
    # Kirby AnimID 0x1a8-0x1a9 Interrupts
    # Kirby AnimID 0x1ad-0x1ae Interrupts
    # Kirby AnimID 0x1b1-0x1b2 Interrupts
    if ((anim_id == 0x174) and (char_id == charInternal.Kirby.value)):
        del unsorted_functions[idx]
        continue
    if ((anim_id == 0x178) and (char_id == charInternal.Kirby.value)):
        del unsorted_functions[idx]
        continue
    if ((anim_id == 0x19b) and (char_id == charInternal.Kirby.value)):
        del unsorted_functions[idx]
        continue
    if ((anim_id == 0x1a1) and (char_id == charInternal.Kirby.value)):
        del unsorted_functions[idx]
        continue
    if ((anim_id == 0x1a3) and (char_id == charInternal.Kirby.value)):
        del unsorted_functions[idx]
        continue
    if ((anim_id == 0x1a9) and (char_id == charInternal.Kirby.value)):
        del unsorted_functions[idx]
        continue
    if ((anim_id == 0x1ae) and (char_id == charInternal.Kirby.value)):
        del unsorted_functions[idx]
        continue
    if ((anim_id == 0x1b2) and (char_id == charInternal.Kirby.value)):
        del unsorted_functions[idx]
        continue

    # This is a set of animID ranges which share the same interrupts as other
    # animID ranges within the total space of all animIDs in Kirby's array.
    # Here, we will just prune the higher range and be done with it until this
    # is understood at a higher level. 
    # 
    # Entries with these animIDs have equivalent interrupts (but do not 
    # necessarily share all of their functions). More plainly:
    # "The function table entry in Kirby's array with the ID on the left 
    #  shares some [or all] functions with the function table entry tagged 
    #  with the ID on the right" :
    # 
    #   152 1bf
    #   153 1c0
    #   154 1c1
    #   155 1c2
    #   156 1c3
    #   157 1c4
    #   158 1c5
    #   159 1c6
    #   
    #   166 1c7
    #   167 1c8
    #   168 1c9
    #   169 1ca
    #   16a 1cb
    #   16b 1cc
    #   16c 1cd
    #   16d 1ce
    #   
    #   170 1cf
    #   171 1d0
    #   
    #   1ab 1d1
    #   1ac 1d2
    #   
    #   1ad 1d3
    #   1ad 1d4
    #   
    #   1af 1d5
    #   1b0 1d6
    #   
    #   1b1 1d7
    #   1b1 1d8
    #   
    #   17a 1d9
    #   17b 1da
    #   17c 1db
    #   17d 1dc
    #   17e 1dd
    #   17f 1de

    ran = [i for i in range(0x1bf, 0x1de+1)]
    if ((anim_id in ran) and (char_id == charInternal.Kirby.value)):
        del unsorted_functions[idx]
        continue

    # Like the above comment for Kirby: pairs of Jigglypuff's entries tagged
    # with these AnimID values share [some or all] functions:
    #
    # 13f 141
    # 140 142
    # 143 145
    # 144 146
    #
    # Just remove the symbols for the higher anim ID, for now

    if ((anim_id == 0x141) and (char_id == charInternal.Jigglypuff.value)):
        del unsorted_functions[idx]
        continue
    if ((anim_id == 0x142) and (char_id == charInternal.Jigglypuff.value)):
        del unsorted_functions[idx]
        continue
    if ((anim_id == 0x145) and (char_id == charInternal.Jigglypuff.value)):
        del unsorted_functions[idx]
        continue
    if ((anim_id == 0x146) and (char_id == charInternal.Jigglypuff.value)):
        del unsorted_functions[idx]
        continue


    # TODO
    # For Marth, prune the symbols for the following combinations of function
    # name and anim ID. Various different sets are shared. I think I did this
    # incorrectly and probably removed some unique symbols for marth (and
    # perhaps Roy). It's confusing. Oh well. We'll get them back, sometime.

    # only animInterrupt is unique for 0x138
    if ((anim_id == 0x138) and (char_id == charInternal.Marth.value)  and ("animInterrupt" not in funcname)):
        del unsorted_functions[idx]
        continue
    # 0x139-0x140 can be pruned (shared with lower AnimID ones)
    ran = [i for i in range(0x139, 0x140+1)]
    if ((anim_id in ran) and (char_id == charInternal.Marth.value)):
        del unsorted_functions[idx]
        continue

    # animInterrupts for Roy, with 0x133,0x134, 0x13b-0x13d are shared with 0x132
    ran = [0x133, 0x134, 0x13b, 0x13c, 0x13d] 
    if ((anim_id in ran) and (char_id == charInternal.Roy.value) and ("animInterrupt" in funcname)):
        del unsorted_functions[idx]
        continue

    # Marth AnimID 0x129-0x12a Interrupts
    # Marth AnimID 0x12d-0x12e Interrupts
    # Marth AnimID 0x130-0x131 Interrupts
    if ((anim_id == 0x12a) and (char_id == charInternal.Marth.value)):
        del unsorted_functions[idx]
        continue
    if ((anim_id == 0x12e) and (char_id == charInternal.Marth.value)):
        del unsorted_functions[idx]
        continue
    if ((anim_id == 0x131) and (char_id == charInternal.Marth.value)):
        del unsorted_functions[idx]
        continue

    # Marth AnimID 0x132-0x134
    # Marth AnimID 0x135-0x137
    ran = [i for i in range(0x133, 0x134+1)]
    ran += [i for i in range(0x136,0x137+1)]
    if ((anim_id in ran) and (char_id == charInternal.Marth.value)):
        del unsorted_functions[idx]
        continue

    # Crazyhand/masterhand (too tired to annotate)
    ran = [0x128, 0x12b, 0x13a, 0x14b, 0x158]
    if ((anim_id in ran) and (char_id == charInternal.MasterHand.value)):
        del unsorted_functions[idx]
        continue
    ran = [0x128, 0x130, 0x136, 0x140, 0x154, 0x157]
    if ((anim_id in ran) and (char_id == charInternal.CrazyHand.value)):
        del unsorted_functions[idx]
        continue




    
    # If we reach the end, that means we can allow the function into the
    # "final" list where it's easier to do pruning by comparing two entries
    sorted_functions.append(entry)




for entry in sorted_functions:
    addr = entry['addr']

    # 0x800761c8 is a generic camera behaviour function
    # that occurs over 1000 times in this table. This occurs
    # elsewhere (like in the global table), so just ignore it here
    if (addr == 0x800761c8):
        #functions[addr]['name'] = "AS_Generic_cameraBehaviour"
        continue

    # If the function appears unique, add it to the list of output
    if (functions.get(addr) == None):
        functions[addr] = entry
    
    # Otherwise, deal with duplicate functions
    else:
        
    
        # Duplicates across character in a table
        preferred = prefer_char(functions.get(addr), entry)
        if (preferred != None):
            functions[addr] = preferred
            continue

        print("Duplicate entry for addr {:08x}".format(addr))
        print(json.dumps(entry))
        print(json.dumps(functions[addr]))




# Print symbols to standard output
for addr in functions:
    size = functions[addr]['size']
    name = functions[addr]['name']
    print(MAPFMT.format(addr, size, addr, name))
