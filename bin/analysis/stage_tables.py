#!/usr/bin/python3
""" stage_tables.py - Dump symbols from stage function tables
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
        self.entity_table_ptr = self.data[1]
        self.functions = {
                'stageInit': self.data[3],
                'unk1': self.data[4],
                'onLoad': self.data[5],
                'onGO': self.data[6],
                'unk3': self.data[7],
                'unk4': self.data[8],
                'unk5': self.data[9],
        }

class stage_entity_ft(function_table):
    """ Representation of a stage entity function table. """
    def __init__(self, *args, **kwargs):
        super(stage_entity_ft, self).__init__(*args, **kwargs)
        self.functions = {
                'onCreate': self.data[0],
                'onUnk': self.data[1],
                'perFrame': self.data[2],
                'onDestroy': self.data[3],
        }


# Parse the top-level stage function tables

functions = {}
dupes = {}

base = 0x803dfedc
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
            new_name = "Stage_{}_{}".format(stage.name, funcname)
            entry = {'addr': addr, 'size': size, 'name': new_name }

            # If the function appears unique, add it to the list of output
            if (functions.get(addr) == None):
                functions[addr] = entry
            else:
                print("Duplicate entry for addr {:08x}".format(addr))
                print(json.dumps(entry))
                print(json.dumps(functions[addr]))

    # Walk the associated array of stage entity function tables. The length of
    # these is encoded somewhere not-in-the-DOL. Will define them all later?
    et_base = ft.entity_table_ptr
    entity_idx = 0
    while (validptr(et_base)):
        et_ft = stage_entity_ft(u32table(dump(et_base, 0x14)))

        # It seems like sometimes, valid entries are zeroed out in an array.
        # Also, the end of arrays tend to sit right above some strings. Maybe
        # checking like this is a suitable way to detect when we should stop?
        # Looking over the entries manually: it looks like this is correct.

        if ((et_ft.data[0] > 0x817fffff) or 
                ((et_ft.data[0] < 0x80000000) and (et_ft.data[0] != 0))):
            break


        # Construct an entry for each function
        for funcname in et_ft.functions:
            addr = et_ft.functions[funcname]
            if (validptr(addr)):
                size = getsymbolsize(addr)
                new_name = "Stage_{}_Entity{:02x}_{}".format(stage.name, 
                        entity_idx, funcname)
                entry = {'addr': addr, 'size': size, 'name': new_name,
                        'entity_idx': entity_idx, 'stage_id': stage.value, 
                        'funcname': funcname,  }


                # Catch duplicates
                if (dupes.get(addr) != None):
                    new_entry = entry
                    new_pair = "entity_idx{:02x} {}".format(new_entry['entity_idx'], new_entry['name'])
                    dupes[addr]['info'].append(new_pair)
                    dupes[addr]['entity_idx'].append(new_entry['entity_idx'])
                    dupes[addr]['stage_id'].append(new_entry['stage_id'])
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
                                'entity_idx': [],
                                'stage_id': [],
                        }
                        dupes[addr] = dupe_entry

                        # Add the two duplicates
                        old_pair = "entity_idx{:02x} {}".format(old_entry['entity_idx'], old_entry['name'])
                        dupes[addr]['info'].append(old_pair)
                        dupes[addr]['entity_idx'].append(old_entry['entity_idx'])
                        dupes[addr]['stage_id'].append(old_entry['stage_id'])

                        dupes[addr]['uniq_funcname'][old_entry['funcname']] = True

                        new_pair = "entity_idx{:02x} {}".format(new_entry['entity_idx'], new_entry['name'])
                        dupes[addr]['info'].append(new_pair)
                        dupes[addr]['entity_idx'].append(new_entry['entity_idx'])
                        dupes[addr]['stage_id'].append(new_entry['stage_id'])
                        dupes[addr]['uniq_funcname'][new_entry['funcname']] = True

                        # Remove the duplicate from the final list
                        del functions[addr]

                    # If bucket exists
                    else:
                        new_entry = entry
                        new_pair = "entity_idx{:03x} {}".format(new_entry['entity_idx'], new_entry['name'])
                        dupes[addr]['info'].append(new_pair)
                        dupes[addr]['entity_idx'].append(new_entry['entity_idx'])
                        dupes[addr]['uniq_funcname'][new_entry['funcname']] = True

        # Go to next entity struct in list
        et_base += 0x14
        entity_idx += 1

    # Go to the next pointer in the list
    base += 0x4




# Resolve duplicate buckets before committing them into the final list. 
for addr in dupes:

    # List of associated underlying function names
    x = dupes[addr]['uniq_funcname']
    uniq_funcname = []
    for funcname in x:
        uniq_funcname.append(funcname)

    # List of associated action state ids
    entity_idx = dupes[addr]['entity_idx']
    stage_id = dupes[addr]['stage_id']


    if ((entity_idx == [5, 7, 17]) and (len(uniq_funcname) == 1)):
        dupes[addr]['newname'] = "Stage_Castle_Entity05and07and11_{}".format(uniq_funcname[0])
    if ((entity_idx == [8,9,10,11,12,13,14,15,16]) and (len(uniq_funcname) == 1)):
        dupes[addr]['newname'] = "Stage_Castle_Entity08-10_{}".format(uniq_funcname[0])
    if ((entity_idx == [18, 19, 20]) and (len(uniq_funcname) == 1)):
        dupes[addr]['newname'] = "Stage_Castle_Entity12-14_{}".format(uniq_funcname[0])

    if ((entity_idx == [1, 2]) and (len(uniq_funcname) == 1)):
        dupes[addr]['newname'] = "Stage_KongoJungle_Entity01-02_{}".format(uniq_funcname[0])
    if ((entity_idx == [7, 8, 9]) and (len(uniq_funcname) == 1)):
        dupes[addr]['newname'] = "Stage_KongoJungle_Entity07-09_{}".format(uniq_funcname[0])

    if ((entity_idx == [5,6,7,8]) and (len(uniq_funcname) == 1)):
        dupes[addr]['newname'] = "Stage_GreatBay_Entity05-08_{}".format(uniq_funcname[0])

    if ((entity_idx == [5,6,7,8,9,10]) and (len(uniq_funcname) == 1)):
        dupes[addr]['newname'] = "Stage_Fountain_Entity05-0a_{}".format(uniq_funcname[0])

    if ((entity_idx == [13,14,15,16,17,18]) and (len(uniq_funcname) == 1)):
        dupes[addr]['newname'] = "Stage_Corneria_Entity0d-12_{}".format(uniq_funcname[0])

    if ((entity_idx == [10,11,12,13,14,15]) and (len(uniq_funcname) == 1)):
        dupes[addr]['newname'] = "Stage_Venom_Entity0a-1f_{}".format(uniq_funcname[0])

    if ((entity_idx == [7,8]) and (len(uniq_funcname) == 1)):
        dupes[addr]['newname'] = "Stage_PokemonStadium_Entity07-08_{}".format(uniq_funcname[0])

    pokefloats_shared = [2,3,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]
    if ((entity_idx == pokefloats_shared) and (len(uniq_funcname) == 1)):
        dupes[addr]['newname'] = "Stage_PokeFloats_Entity02-1a_{}".format(uniq_funcname[0])

    if ((entity_idx == [36,37]) and (len(uniq_funcname) == 1)):
        dupes[addr]['newname'] = "Stage_MuteCity_Entity24-25_{}".format(uniq_funcname[0])

    if ((entity_idx == [3,4]) and (len(uniq_funcname) == 1)):
        dupes[addr]['newname'] = "Stage_MushroomKingdomII_Entity03-04_{}".format(uniq_funcname[0])

    if ((entity_idx == [1,3]) and (len(uniq_funcname) == 1)):
        dupes[addr]['newname'] = "Stage_Unk20_Entity01and03_{}".format(uniq_funcname[0])

    if (dupes[addr].get('newname') != None):
        # If we gave the symbol a new name, continue to the next
        continue
    else:
        # Otherwise, print some info
        print("########### dupe {}".format(hex(addr)))
        print(json.dumps(dupes[addr], indent=4))


# One final iteration to add renamed symbols to the final list
for addr in dupes:

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
