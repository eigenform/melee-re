#!/usr/bin/python3
""" char_global_as.py
"""

import json
from sys import argv
from hexdump import hexdump
from struct import pack,unpack

# Definitions and resources specific to GALE01 NTSC-U v1.02
from ntsc102_defs import *

from ramdump_util import *

class anim_ft(function_table):
    def __init__(self, *args, **kwargs):
        super(anim_ft, self).__init__(*args, **kwargs)
        self.idx = self.data[0]
        self.functions = {
            'animInterrupt': self.data[3],
            'inputInterrupt': self.data[4],
            'actionPhysics': self.data[5],
            'collisionInterrupt': self.data[6],
            'cameraBehaviour': self.data[7],
        }

# There appears to be 341 (0x155) entries in this array, indexed by action 
# state ID. This array does not account for all action state IDs.

base = 0x803c2800
functions = {}
dupes = {}
for action in (actionState):
    as_id = action.value
    
    # This array terminates after entry 0x155
    if (as_id > 0x155):
        break

    as_name = action.name
    ft = anim_ft(u32table(dump(base, 0x20)))

    # If the anim_id is -1, just skip parsing entry (for now)
    if (ft.idx == 0xffffffff):
        base += 0x20
        continue

    # Construct an entry for each function
    for funcname in ft.functions:
        addr = ft.functions[funcname]
        if (validptr(addr)):
            size = getsymbolsize(addr)
            new_name = "AS_{}_{}".format(as_name, funcname)
            entry = {'addr': addr, 'size': size, 'name': new_name, 'funcname': funcname,
                    'as_id': as_id, 'as_name': as_name}

            # If the function is in one of our duplicate buckets, we should
            # add it there and not to the final map
            if (dupes.get(addr) != None):
                new_entry = entry
                new_pair = "as_id{:03x} {}".format(new_entry['as_id'], new_entry['name'])
                dupes[addr]['info'].append(new_pair)
                dupes[addr]['as_id'].append(new_entry['as_id'])
                dupes[addr]['uniq_funcname'][new_entry['funcname']] = True
                continue

            # If the function appears unique, add it to the list of output
            if (functions.get(addr) == None):
                functions[addr] = entry
            else:

                # This generic cameraBehaviour function is used a lot,
                # and also in tables other than ones from this global array
                if (addr == 0x800761c8):
                    functions[addr]['name'] = "AS_Generic_cameraBehaviour"
                    continue


                # If we can't easily prune certain duplicates, start counting
                # dupes into buckets this time - easier to sift through later

                # If duplicate bucket doesnt exist
                if (dupes.get(addr) == None):
                    old_entry = functions.get(addr)
                    new_entry = entry

                    # Create a new bucket
                    dupe_entry = {'addr': old_entry['addr'],
                            'size': old_entry['size'],
                            'uniq_funcname': {},
                            'info': [],
                            'as_id': [],
                    }
                    dupes[addr] = dupe_entry

                    # Add the two duplicates
                    old_pair = "as_id{:03x} {}".format(old_entry['as_id'], old_entry['name'])
                    dupes[addr]['info'].append(old_pair)
                    dupes[addr]['as_id'].append(old_entry['as_id'])

                    dupes[addr]['uniq_funcname'][old_entry['funcname']] = True

                    new_pair = "as_id{:03x} {}".format(new_entry['as_id'], new_entry['name'])
                    dupes[addr]['info'].append(new_pair)
                    dupes[addr]['as_id'].append(new_entry['as_id'])
                    dupes[addr]['uniq_funcname'][new_entry['funcname']] = True

                    # Remove the duplicate from the final list
                    del functions[addr]

                # If bucket exists
                else:
                    new_entry = entry
                    new_pair = "as_id{:03x} {}".format(new_entry['as_id'], new_entry['name'])
                    dupes[addr]['info'].append(new_pair)
                    dupes[addr]['as_id'].append(new_entry['as_id'])
                    dupes[addr]['uniq_funcname'][new_entry['funcname']] = True

    # Go to the next struct
    base += 0x20


# Resolve duplicate buckets before committing them into the final list. 
# There are a lot of these. Try to give them generic names based on the set
# of associated action state IDs. This works out in a lot of cases.

for addr in dupes:

    # List of associated underlying function names
    x = dupes[addr]['uniq_funcname']
    uniq_funcname = []
    for funcname in x:
        uniq_funcname.append(funcname)

    # List of associated action state ids
    as_id = dupes[addr]['as_id']


    if (as_id == [6, 7, 8]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("DeadUpFall", uniq_funcname[0])

    if (as_id == [15, 16, 17]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("Walk", uniq_funcname[0])


    if (as_id == [25, 26]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("Jump", uniq_funcname[0])
    if (as_id == [27, 28]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("JumpAerial", uniq_funcname[0])

    if (as_id == [29, 33, 34]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("FallAerial", uniq_funcname[0])
    if (as_id == [32, 33, 34]):
       if ((len(uniq_funcname) == 1) and (uniq_funcname[0] == "inputInterrupt")):
           dupes[addr]['newname'] = "AS_{}_{}".format("FallAerial", uniq_funcname[0])




    if (as_id == [35, 36, 37]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("FallSpecial", uniq_funcname[0])

    if (as_id == [42, 43]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("Landing", uniq_funcname[0])


    if (as_id == [44, 45, 46]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("Attack1", uniq_funcname[0])

    if (as_id == [51,52, 53, 54,55]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("AttackS3", uniq_funcname[0])

    if (as_id == [58,59,60, 61,62]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("AttackS4", uniq_funcname[0])

    if (as_id == [65,66,67, 68,69]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("AttackAir", uniq_funcname[0])

    if (as_id == [70,71,72, 73,74]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("LandingAir", uniq_funcname[0])



    if (as_id == [75,76,77, 78,79,80,81,82,83,84,85,86]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("Damage", uniq_funcname[0])
    if (as_id == [87, 88, 89, 90]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("DamageFly", uniq_funcname[0])

    if (as_id == [92,93]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("LightAndHeavyGet", uniq_funcname[0])


    # There's a lot of reuse for different functions with these throw actions. 

    if (as_id == [94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107,
                108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("LightAndHeavyThrow", uniq_funcname[0])

    if (as_id == [94, 95, 96, 97, 99, 104, 105, 106, 107, 108, 109, 110, 111,116, 117, 118, 119]):
        if ((len(uniq_funcname) == 1) and (uniq_funcname[0] == "actionPhysics")):
           dupes[addr]['newname'] = "AS_{}_{}".format("LightAndHeavyThrow", uniq_funcname[0])

    if (as_id == [94, 95, 96, 97, 108, 109, 110, 111]):
        if ((len(uniq_funcname) == 1) and (uniq_funcname[0] == "collisionInterrupt")):
           dupes[addr]['newname'] = "AS_{}_{}".format("LightAndHeavyThrow", uniq_funcname[0])

    if (as_id == [98,99]):
        if ((len(uniq_funcname) == 1) and (uniq_funcname[0] == "collisionInterrupt")):
           dupes[addr]['newname'] = "AS_{}_{}".format("LightThrow", uniq_funcname[0])

    if (as_id == [100, 101, 102, 103, 112, 113, 114, 115]):
        if ((len(uniq_funcname) == 1) and (uniq_funcname[0] == "actionPhysics")):
           dupes[addr]['newname'] = "AS_{}_{}".format("LightThrowAir", uniq_funcname[0])
    if (as_id == [100, 101, 102, 103, 112, 113, 114, 115]):
        if ((len(uniq_funcname) == 1) and (uniq_funcname[0] == "collisionInterrupt")):
           dupes[addr]['newname'] = "AS_{}_{}".format("LightThrowAir", uniq_funcname[0])

    if (as_id == [104, 105, 106, 107, 116, 117, 118, 119]):
        if ((len(uniq_funcname) == 1) and (uniq_funcname[0] == "collisionInterrupt")):
           dupes[addr]['newname'] = "AS_{}_{}".format("HeavyThrow", uniq_funcname[0])


    # These chunks of swinging action states are all shared

    if (as_id == [120, 121, 122, 123]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("SwordSwing", uniq_funcname[0])
    if (as_id == [124, 125, 126, 127]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("BatSwing", uniq_funcname[0])
    if (as_id == [128, 129, 130, 131]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("ParasolSwing", uniq_funcname[0])
    if (as_id == [132, 133, 134, 135]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("HarisenSwing", uniq_funcname[0])
    if (as_id == [136, 137, 138, 139]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("StarRodSwing", uniq_funcname[0])
    if (as_id == [140, 141, 142, 143]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("LipStickSwing", uniq_funcname[0])


    if (as_id == [148, 150]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("LGunShoot", uniq_funcname[0])
    if (as_id == [149, 151]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("LGunShootAir", uniq_funcname[0])

    if (as_id == [156, 157]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("DamageScrew", uniq_funcname[0])

    if (as_id == [158, 166]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("ItemScopeStart", uniq_funcname[0])
    if (as_id == [159, 167]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("ItemScopeRapid", uniq_funcname[0])
    if (as_id == [160, 168]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("ItemScopeFire", uniq_funcname[0])
    if (as_id == [161, 169]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("ItemScopeEnd", uniq_funcname[0])

    if (as_id == [162, 170]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("ItemScopeAirStart", uniq_funcname[0])
    if (as_id == [163, 171]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("ItemScopeAirRapid", uniq_funcname[0])
    if (as_id == [164, 172]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("ItemScopeAirFire", uniq_funcname[0])
    if (as_id == [165, 173]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("ItemScopeAirEnd", uniq_funcname[0])


    if (as_id == [175, 176]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("LiftWalk", uniq_funcname[0])


    if (as_id == [188, 189, 196,197]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("DownForwardAndBack", uniq_funcname[0])


    if (as_id == [183, 191]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("DownBound", uniq_funcname[0])
    if (as_id == [184, 192]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("DownWait", uniq_funcname[0])
    if (as_id == [185, 193]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("DownDamage", uniq_funcname[0])
    if (as_id == [186, 194]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("DownStand", uniq_funcname[0])
    if (as_id == [187, 195]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("DownAttack", uniq_funcname[0])
    if (as_id == [190, 198]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("DownSpot", uniq_funcname[0])


    if (as_id == [200, 201]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("PassiveStand", uniq_funcname[0])
    if (as_id == [202, 203]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("PassiveWall", uniq_funcname[0])

    if (as_id == [207, 208]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("ShieldBreakDown", uniq_funcname[0])
    if (as_id == [209, 210]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("ShieldBreakStand", uniq_funcname[0])


    if (as_id == [213, 215]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("CatchPull", uniq_funcname[0])


    if (as_id == [233, 234]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("Escape", uniq_funcname[0])

    if (as_id == [242, 243, 274]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("ThrownLw", uniq_funcname[0])

    if (as_id == [247, 248]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("FlyReflect", uniq_funcname[0])


    if (as_id == [252, 253, 254, 255, 256, 257, 258, 259]):
        if ((len(uniq_funcname) == 1) and (uniq_funcname[0] == "cameraBehaviour")):
           dupes[addr]['newname'] = "AS_{}_{}".format("Cliff", uniq_funcname[0])

    if (as_id == [254, 255]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("CliffClimb", uniq_funcname[0])
    if (as_id == [256, 257]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("CliffAttack", uniq_funcname[0])
    if (as_id == [258, 259]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("CliffEscape", uniq_funcname[0])

    if (as_id == [260, 262]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("CliffJump1", uniq_funcname[0])
    if (as_id == [261, 263]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("CliffJump2", uniq_funcname[0])

    if (as_id == [264, 265]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("Appeal", uniq_funcname[0])


    if (as_id == [266, 267, 268, 269, 270]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("Shouldered", uniq_funcname[0])

    if (as_id == [239, 271]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("ThrownF", uniq_funcname[0])
    if (as_id == [240, 272]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("ThrownB", uniq_funcname[0])
    if (as_id == [241, 273]):
       if (len(uniq_funcname) == 1):
           dupes[addr]['newname'] = "AS_{}_{}".format("ThrownHi", uniq_funcname[0])

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
