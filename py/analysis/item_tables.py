#!/usr/bin/python3
""" item_tables.py
So much code re-use in this. Eventually make this better.

Missing the stage-specific items table right now. Also I kind of feel like 
some of these are indexed perfectly according to item ID. Hmmmm.
"""

import json
from sys import argv
from hexdump import hexdump
from struct import pack,unpack

# Definitions and resources specific to GALE01 NTSC-U v1.02
from ntsc102_defs import *

from ramdump_util import *

class item_ft(function_table):
    def __init__(self, *args, **kwargs):
        super(item_ft, self).__init__(*args, **kwargs)

        # Think this also has functions in it
        self.unk_ptr = self.data[0]

        self.functions = {
                'OnCreate': self.data[1],
                'OnDestroy': self.data[2],
                'OnPickup': self.data[3],
                'OnRelease': self.data[4],
                'OnThrow': self.data[5],
                'OnHitCollision': self.data[6],
                'OnTakeDamage': self.data[7],
                'OnReflect': self.data[8],
                'OnShieldCollision0?': self.data[9],
                'OnCollision_unk2?': self.data[10],
                'unk_5': self.data[11],
                'OnShieldCollision1?': self.data[12],
                'OnShieldCollision2?': self.data[13],
                'unk_8': self.data[14],
        }

def prefer_charproj_id(old_entry, new_entry):
    """
    In the character projectile table, prefer certain names over others.
    """

    old_idx = old_entry['table_idx']
    new_idx = new_entry['table_idx']

    
    # Falco/FoxLaser
    if ((old_idx == 6) and (new_idx == 7)):
        return new_entry
    if ((new_idx == 6) and (old_idx == 7)):
        return old_entry
    # Falco/FoxShadow
    if ((old_idx == 9) and (new_idx == 8)):
        return new_entry
    if ((new_idx == 9) and (old_idx == 8)):
        return old_entry

    # YLink/LinkBomb
    if ((old_idx == 11) and (new_idx == 10)):
        return new_entry
    if ((new_idx == 11) and (old_idx == 10)):
        return old_entry
    # YLink/LinkBoomerang
    if ((old_idx == 13) and (new_idx == 12)):
        return new_entry
    if ((new_idx == 13) and (old_idx == 12)):
        return old_entry
    # YLink/LinkHookshot
    if ((old_idx == 15) and (new_idx == 14)):
        return new_entry
    if ((new_idx == 15) and (old_idx == 14)):
        return old_entry
    # Prefer "Arrow" over "FireArrow"
    if ((old_idx == 17) and (new_idx == 16)):
        return new_entry
    if ((new_idx == 17) and (old_idx == 16)):
        return old_entry

    return None



functions = {}
dupes = {}

# Currently in ntsc102_defs.py, these item IDs are fragmented up in order to 
# deal with the indexing of each of these arrays. In reality, each ID in each
# of these lists is unique and monotonically increasing. Will fix later.




# -----------------------------------------------------------------------------
# Regular items

base = 0x803f14c4
for item in (itemID):
    ft = item_ft(u32table(dump(base, 0x3c)))

    # Construct an entry for each function
    for funcname in ft.functions:
        addr = ft.functions[funcname]
        if (validptr(addr)):
            size = getsymbolsize(addr)
            new_name = "Item_{}_{}".format(item.name, funcname)
            entry = {'addr': addr, 'size': size, 'name': new_name, 
                    'funcname': funcname, 
                    'table_idx': item.value }

            # If the function is in one of our duplicate buckets, we should
            # add it there and not to the final map
            if (dupes.get(addr) != None):
                new_entry = entry
                new_pair = "table_idx{:03x} {}".format(new_entry['table_idx'], new_entry['name'])
                dupes[addr]['info'].append(new_pair)
                dupes[addr]['table_idx'].append(new_entry['table_idx'])
                dupes[addr]['uniq_funcname'][new_entry['funcname']] = True
                continue


            # If the function appears unique, add it to the list of output
            if (functions.get(addr) == None):
                functions[addr] = entry
            else:

                # If duplicate bucket doesnt exist
                if (dupes.get(addr) == None):
                    old_entry = functions.get(addr)
                    new_entry = entry

                    # Create a new bucket
                    dupe_entry = {'addr': old_entry['addr'],
                            'size': old_entry['size'],
                            'uniq_funcname': {},
                            'info': [],
                            'table_idx': [],
                    }
                    dupes[addr] = dupe_entry

                    # Add the two duplicates
                    old_pair = "table_idx{:03x} {}".format(old_entry['table_idx'], old_entry['name'])
                    dupes[addr]['info'].append(old_pair)
                    dupes[addr]['table_idx'].append(old_entry['table_idx'])

                    dupes[addr]['uniq_funcname'][old_entry['funcname']] = True

                    new_pair = "table_idx{:03x} {}".format(new_entry['table_idx'], new_entry['name'])
                    dupes[addr]['info'].append(new_pair)
                    dupes[addr]['table_idx'].append(new_entry['table_idx'])
                    dupes[addr]['uniq_funcname'][new_entry['funcname']] = True

                    # Remove the duplicate from the final list
                    del functions[addr]

                # If bucket exists
                else:
                    new_entry = entry
                    new_pair = "table_idx{:03x} {}".format(new_entry['table_idx'], new_entry['name'])
                    dupes[addr]['info'].append(new_pair)
                    dupes[addr]['table_idx'].append(new_entry['table_idx'])
                    dupes[addr]['uniq_funcname'][new_entry['funcname']] = True

    # Go to next struct
    base += 0x3c

# -----------------------------------------------------------------------------
# Pokemon

base = 0x803f23cc
for item in (pokemonID):
    ft = item_ft(u32table(dump(base, 0x3c)))

    # Construct an entry for each function
    for funcname in ft.functions:
        addr = ft.functions[funcname]
        if (validptr(addr)):
            size = getsymbolsize(addr)
            new_name = "Pkmn_{}_{}".format(item.name, funcname)
            entry = {'addr': addr, 'size': size, 'name': new_name, 
                    'funcname': funcname, 
                    'table_idx': item.value }

            # If the function is in one of our duplicate buckets, we should
            # add it there and not to the final map
            if (dupes.get(addr) != None):
                new_entry = entry
                new_pair = "table_idx{:03x} {}".format(new_entry['table_idx'], new_entry['name'])
                dupes[addr]['info'].append(new_pair)
                dupes[addr]['table_idx'].append(new_entry['table_idx'])
                dupes[addr]['uniq_funcname'][new_entry['funcname']] = True
                continue


            # If the function appears unique, add it to the list of output
            if (functions.get(addr) == None):
                functions[addr] = entry
            else:
                # If duplicate bucket doesnt exist
                if (dupes.get(addr) == None):
                    old_entry = functions.get(addr)
                    new_entry = entry

                    # Create a new bucket
                    dupe_entry = {'addr': old_entry['addr'],
                            'size': old_entry['size'],
                            'uniq_funcname': {},
                            'info': [],
                            'table_idx': [],
                    }
                    dupes[addr] = dupe_entry

                    # Add the two duplicates
                    old_pair = "table_idx{:03x} {}".format(old_entry['table_idx'], old_entry['name'])
                    dupes[addr]['info'].append(old_pair)
                    dupes[addr]['table_idx'].append(old_entry['table_idx'])

                    dupes[addr]['uniq_funcname'][old_entry['funcname']] = True

                    new_pair = "table_idx{:03x} {}".format(new_entry['table_idx'], new_entry['name'])
                    dupes[addr]['info'].append(new_pair)
                    dupes[addr]['table_idx'].append(new_entry['table_idx'])
                    dupes[addr]['uniq_funcname'][new_entry['funcname']] = True

                    # Remove the duplicate from the final list
                    del functions[addr]

                # If bucket exists
                else:
                    new_entry = entry
                    new_pair = "table_idx{:03x} {}".format(new_entry['table_idx'], new_entry['name'])
                    dupes[addr]['info'].append(new_pair)
                    dupes[addr]['table_idx'].append(new_entry['table_idx'])
                    dupes[addr]['uniq_funcname'][new_entry['funcname']] = True

    # Go to next struct
    base += 0x3c


# -----------------------------------------------------------------------------
# Pokemon projectiles and effects

base = 0x803f2ad4
for item in (pokemonProjectile):
    ft = item_ft(u32table(dump(base, 0x3c)))

    # Construct an entry for each function
    for funcname in ft.functions:
        addr = ft.functions[funcname]
        if (validptr(addr)):
            size = getsymbolsize(addr)
            new_name = "PkmnProjectile_{}_{}".format(item.name, funcname)
            entry = {'addr': addr, 'size': size, 'name': new_name, 
                    'funcname': funcname, 
                    'table_idx': item.value }

            # If the function is in one of our duplicate buckets, we should
            # add it there and not to the final map
            if (dupes.get(addr) != None):
                new_entry = entry
                new_pair = "table_idx{:03x} {}".format(new_entry['table_idx'], new_entry['name'])
                dupes[addr]['info'].append(new_pair)
                dupes[addr]['table_idx'].append(new_entry['table_idx'])
                dupes[addr]['uniq_funcname'][new_entry['funcname']] = True
                continue


            # If the function appears unique, add it to the list of output
            if (functions.get(addr) == None):
                functions[addr] = entry
            else:
                # If duplicate bucket doesnt exist
                if (dupes.get(addr) == None):
                    old_entry = functions.get(addr)
                    new_entry = entry

                    # Create a new bucket
                    dupe_entry = {'addr': old_entry['addr'],
                            'size': old_entry['size'],
                            'uniq_funcname': {},
                            'info': [],
                            'table_idx': [],
                    }
                    dupes[addr] = dupe_entry

                    # Add the two duplicates
                    old_pair = "table_idx{:03x} {}".format(old_entry['table_idx'], old_entry['name'])
                    dupes[addr]['info'].append(old_pair)
                    dupes[addr]['table_idx'].append(old_entry['table_idx'])

                    dupes[addr]['uniq_funcname'][old_entry['funcname']] = True

                    new_pair = "table_idx{:03x} {}".format(new_entry['table_idx'], new_entry['name'])
                    dupes[addr]['info'].append(new_pair)
                    dupes[addr]['table_idx'].append(new_entry['table_idx'])
                    dupes[addr]['uniq_funcname'][new_entry['funcname']] = True

                    # Remove the duplicate from the final list
                    del functions[addr]

                # If bucket exists
                else:
                    new_entry = entry
                    new_pair = "table_idx{:03x} {}".format(new_entry['table_idx'], new_entry['name'])
                    dupes[addr]['info'].append(new_pair)
                    dupes[addr]['table_idx'].append(new_entry['table_idx'])
                    dupes[addr]['uniq_funcname'][new_entry['funcname']] = True

    # Go to next struct
    base += 0x3c

# -----------------------------------------------------------------------------
# "Monsters" and char specific projectiles

base = 0x803f3100
for item in (charProjectile):
    ft = item_ft(u32table(dump(base, 0x3c)))

    # Construct an entry for each function
    for funcname in ft.functions:
        addr = ft.functions[funcname]
        if (validptr(addr)):
            size = getsymbolsize(addr)
            new_name = "CharProjectile_{}_{}".format(item.name, funcname)
            entry = {'addr': addr, 'size': size, 'name': new_name, 
                    'funcname': funcname, 
                    'table_idx': item.value }

            # If the function is in one of our duplicate buckets, we should
            # add it there and not to the final map
            if (dupes.get(addr) != None):
                new_entry = entry
                new_pair = "table_idx{:03x} {}".format(new_entry['table_idx'], new_entry['name'])
                dupes[addr]['info'].append(new_pair)
                dupes[addr]['table_idx'].append(new_entry['table_idx'])
                dupes[addr]['uniq_funcname'][new_entry['funcname']] = True
                continue


            # If the function appears unique, add it to the list of output
            if (functions.get(addr) == None):
                functions[addr] = entry
            else:
                # If duplicate bucket doesnt exist
                if (dupes.get(addr) == None):
                    old_entry = functions.get(addr)
                    new_entry = entry

                    # Create a new bucket
                    dupe_entry = {'addr': old_entry['addr'],
                            'size': old_entry['size'],
                            'uniq_funcname': {},
                            'info': [],
                            'table_idx': [],
                    }
                    dupes[addr] = dupe_entry

                    # Add the two duplicates
                    old_pair = "table_idx{:03x} {}".format(old_entry['table_idx'], old_entry['name'])
                    dupes[addr]['info'].append(old_pair)
                    dupes[addr]['table_idx'].append(old_entry['table_idx'])

                    dupes[addr]['uniq_funcname'][old_entry['funcname']] = True

                    new_pair = "table_idx{:03x} {}".format(new_entry['table_idx'], new_entry['name'])
                    dupes[addr]['info'].append(new_pair)
                    dupes[addr]['table_idx'].append(new_entry['table_idx'])
                    dupes[addr]['uniq_funcname'][new_entry['funcname']] = True

                    # Remove the duplicate from the final list
                    del functions[addr]

                # If bucket exists
                else:
                    new_entry = entry
                    new_pair = "table_idx{:03x} {}".format(new_entry['table_idx'], new_entry['name'])
                    dupes[addr]['info'].append(new_pair)
                    dupes[addr]['table_idx'].append(new_entry['table_idx'])
                    dupes[addr]['uniq_funcname'][new_entry['funcname']] = True

    # Go to next struct
    base += 0x3c


# -----------------------------------------------------------------------------
# Deal with duplicate symbols before committing to the final list. There will
# be a significant number of these.

for addr in dupes:

    # List of associated underlying function names
    x = dupes[addr]['uniq_funcname']
    uniq_funcname = []
    for funcname in x:
        uniq_funcname.append(funcname)

    # List of associated action state ids
    table_idx = dupes[addr]['table_idx']

    # We're doing transformations from functions on all tables here, so
    # ideally you might also want to collect the table name to make sure
    # you're pruning the right functions (considering that all the different 
    # table index values are not totally unique right now). You might 
    # accidentally prune some unrelated set of duplicates that happen to have
    # the same index in the table. Deal with this later.

    

    # Going to call out some specific ones here because it's more reasonable
    # than matching by the shared table indicies in this case

    if (addr == 0x802c9c78):
           dupes[addr]['newname'] = "PkmnProjectile_Chicorita_OnHitCollision"

    if (addr == 0x802cc5a4):
           dupes[addr]['newname'] = "PkmnProjectile_Charizard_OnShieldCollision0?"
    if (addr == 0x802cc5cc):
           dupes[addr]['newname'] = "PkmnProjectile_Charizard_unk5"
    if (addr == 0x802cc5c4):
           dupes[addr]['newname'] = "PkmnProjectile_Charizard_OnShieldCollision2?"
    if (addr == 0x802cc584):
           dupes[addr]['newname'] = "PkmnProjectile_Charizard_unk8"

    if (addr == 0x802cb778):
           dupes[addr]['newname'] = "PkmnProjectile_Weezing_unk8"

    if (addr == 0x802d23d4):
           dupes[addr]['newname'] = "PkmnProjectile_Lugia_unk8"

    if (addr == 0x8029ca78):
           dupes[addr]['newname'] = "CharProjectile_FoxLaser_OnCollision"
    if (addr == 0x8029ca80):
           dupes[addr]['newname'] = "CharProjectile_FoxLaser_OnCollision0"
    if (addr == 0x8029cc4c):
           dupes[addr]['newname'] = "CharProjectile_FoxLaser_unk_5"
    if (addr == 0x8029cc54):
           dupes[addr]['newname'] = "CharProjectile_FoxLaser_OnShieldCollision1"
    if (addr == 0x8029ccf0):
           dupes[addr]['newname'] = "CharProjectile_FoxLaser_OnShieldCollision2"
    if (addr == 0x8029ccf8):
           dupes[addr]['newname'] = "CharProjectile_FoxLaser_unk_8"

    if ((table_idx == [13, 14]) and (len(uniq_funcname) == 1)):
           dupes[addr]['newname'] = "CharProjectile_FoxShadow_{}".format(uniq_funcname[0])

    if ((table_idx == [15, 16]) and (len(uniq_funcname) == 1)):
           dupes[addr]['newname'] = "CharProjectile_LinkBomb_{}".format(uniq_funcname[0])
    if ((table_idx == [17, 18]) and (len(uniq_funcname) == 1)):
           dupes[addr]['newname'] = "CharProjectile_LinkBoomerang_{}".format(uniq_funcname[0])
    if ((table_idx == [19, 20]) and (len(uniq_funcname) == 1)):
           dupes[addr]['newname'] = "CharProjectile_LinkHookshot_{}".format(uniq_funcname[0])

    if ((table_idx == [21, 22, 97, 98]) and (len(uniq_funcname) == 1)):
           dupes[addr]['newname'] = "CharProjectile_Arrow_{}".format(uniq_funcname[0])

    if ((table_idx == [31, 32, 95, 96]) and (len(uniq_funcname) == 1)):
           dupes[addr]['newname'] = "CharProjectile_FoxBlaster_{}".format(uniq_funcname[0])

    if ((table_idx == [33, 34, 99, 100]) and (len(uniq_funcname) == 1)):
           dupes[addr]['newname'] = "CharProjectile_LinkBow_{}".format(uniq_funcname[0])

    if ((table_idx == [38, 39]) and (len(uniq_funcname) == 1)):
           dupes[addr]['newname'] = "CharProjectile_PikachuThunder_{}".format(uniq_funcname[0])

    if ((table_idx == [40, 41]) and (len(uniq_funcname) == 1)):
           dupes[addr]['newname'] = "CharProjectile_MarioCape_{}".format(uniq_funcname[0])

    if ((table_idx == [46, 48, 104, 106]) and (len(uniq_funcname) == 1)):
           dupes[addr]['newname'] = "CharProjectile_PikachuNeutralBAir_{}".format(uniq_funcname[0])
    if ((table_idx == [47, 49, 105, 107]) and (len(uniq_funcname) == 1)):
           dupes[addr]['newname'] = "CharProjectile_PikachuNeutralBGround_{}".format(uniq_funcname[0])



    # The relations between entries in this block are unknown right now
    if (addr == 0x802f044c):
           dupes[addr]['newname'] = "CharProjectile_Unk52and54_unk8"
    if (addr == 0x802f0bc8):
           dupes[addr]['newname'] = "CharProjectile_Unk53and55_unk8"
    if (addr == 0x80294a90):
           dupes[addr]['newname'] = "Item_BunnyHoodandMetalBox_unk8"
    if (addr == 0x8027c8b0):
           dupes[addr]['newname'] = "CharProjectile_GenericMonster_OnDestroy?"



    # Lots of Kirby's functions are duplicates: just pop off the info list and
    # check this later on when adding them back

    kirby_indicies = [87, 88, 89, 90, 91, 92, 101, 102, 103, 108, 109, 110,
            111, 112, 114, 116 ]
    for idx in kirby_indicies:
        if (idx in table_idx):
            dupes[addr]['info'].pop()
            dupes[addr]['table_idx'].pop()


    if (dupes[addr].get('newname') != None):
        # If we gave the symbol a new name, continue to the next
        continue


    if ( (len(dupes[addr]['info']) == 1) and (len(dupes[addr]['table_idx']) == 1)):
        # If we popped off one of kirby's entries, continue
        continue

    else:
        # Otherwise, print some info
        print("########### dupe {}".format(hex(addr)))
        print(json.dumps(dupes[addr], indent=4))



# -----------------------------------------------------------------------------
# Format the final output

# One final iteration to add renamed symbols to the final list
for addr in dupes:

    if (len(dupes[addr]['info']) == 1):
        dupes[addr]['newname'] = dupes[addr]['info'][0].split(" ")[1]

    dupes[addr]['name'] = dupes[addr]['newname']

    if (functions.get(addr) == None):
        functions[addr] = dupes[addr]
        continue
    else:
        print("Duplicate entry for addr {:08x}".format(addr))
        print(json.dumps(dupes[addr]))
        print(json.dumps(functions[addr]))




# Print symbols to standard output
for addr in functions:
    size = functions[addr]['size']
    name = functions[addr]['name']
    print(MAPFMT.format(addr, size, addr, name))

