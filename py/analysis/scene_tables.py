#!/usr/bin/python3
""" scene_tables.py
"""

import json
from sys import argv
from hexdump import hexdump
from struct import pack,unpack

# Definitions and resources specific to GALE01 NTSC-U v1.02
from ntsc102_defs import *

from ramdump_util import *

class major_scene_ft(function_table):
    """ Representation of a major scene function table """
    def __init__(self, *args, **kwargs):
        super(major_scene_ft, self).__init__(*args, **kwargs)
        self.scene_id = (self.data[0] & 0x00ff0000) >> 16
        self.functions = {
            'Load': self.data[1],
            'Unload': self.data[2],
            'Init': self.data[3],
        }
        self.min_scene_table_ptr = self.data[4]

class minor_scene_ft(function_table):
    """ Representation of a minor scene function table? """
    def __init__(self, *args, **kwargs):
        super(minor_scene_ft, self).__init__(*args, **kwargs)
        self.minor_id = (self.data[0] & 0xff000000) >> 24
        self.functions = {
            'Prep': self.data[1],
            'Decide': self.data[2],
        }
        self.shared_id = (self.data[3] & 0xff000000) >> 24

class minor_scene_shared_ft(function_table):
    """ Representation of a shared minor scene function table """
    def __init__(self, *args, **kwargs):
        super(minor_scene_shared_ft, self).__init__(*args, **kwargs)
        self.shared_id = (self.data[0] & 0xff000000) >> 24
        self.functions = {
            'Think': self.data[1],
            'Load': self.data[2],
            'Leave': self.data[3],
        }

# Walk the major Scene tables. Each major scene entry has a pointer to some 
# variable-length array of minor scene entries. Unfortunately, this array is 
# not perfectly indexed by major scene ID. Entries are arranged in the order:
#
#       0x2, ..., 0x14, 0x1, 0x15, ... 0x2d
#
# Note that, for later when we are actually giving names to minor scene IDs,
# we will need to basically need to use the shared ID as a way to distinguish
# the function of a particular minor scene. Additionally, there is a kind of
# ordering to entries in the associated minor scene table in the sense that 
# they are arranged in the order that they would occur in-game (w.r.t time).

maj_base = 0x803dacb8
functions = {}

for idx in range(len(majScene)):
    maj_ft = major_scene_ft(u32table(dump(maj_base, 0x14)))
    maj_id = maj_ft.scene_id
    maj_scene_name = majScene(maj_id).name

    # Construct an entry for each function in the major table
    for funcname in maj_ft.functions:
        addr = maj_ft.functions[funcname]
        if (validptr(addr)):
            size = getsymbolsize(addr)
            new_name = "{}_{}_{}".format("MajorScene", maj_scene_name, funcname)
            entry = {'addr': addr, 'size': size, 'name': new_name,
                    'maj_id' : maj_id, }

            # If the function appears unique, add it to the list of output
            if (functions.get(addr) == None):
                functions[addr] = entry

            # The only duplicates in the Major tables are among the scenes in
            # Multi-man Melee (N-Man Melee, N-Minute Melee, Cruel, Endless),
            # for the Load and Init functions. For now, just prefix the symbol 
            # names with "MultiManMelee" to reflect this
            else:
                if (addr == 0x801b685c):
                    functions[addr]['name'] = "MajorScene_MultiManMelee_Load"
                    continue
                if (addr == 0x801b6834):
                    functions[addr]['name'] = "MajorScene_MultiManMelee_Init"
                    continue
                print("Duplicate entry for addr {:08x}".format(addr))
                print(json.dumps(entry))
                print(json.dumps(functions[addr]))


    # Dereference the pointer to the associated minor scene table array and 
    # walk the entries until we reach the end of the array. The length of each
    # array is variable and specific to some particular major scene.
    #
    # Annotate functions directly with the minor scene ID, until we eventually
    # produce a set of mappings with meaningful/unique names for all the IDs 
    # within each major scene.

    min_base = maj_ft.min_scene_table_ptr
    while (validptr(min_base)):
        min_ft = minor_scene_ft(u32table(dump(min_base, 0x18)))
        min_id = min_ft.minor_id

        # The array ends with an entry where (min_id == 0xff)
        if (min_id == 0xff):
            break

        shared_id = min_ft.shared_id
        try:
            min_scene_name = minSceneShared(shared_id).name
        except ValueError as e:
            min_scene_name = "NotFound"

        # Construct an entry for each function in the minor table
        for funcname in min_ft.functions:
            addr = min_ft.functions[funcname]
            if (validptr(addr)):
                size = getsymbolsize(addr)
                new_name = "{}_{}_MinID{:03x}_{}".format("MajorScene", maj_scene_name, 
                        min_id, funcname)
                entry = {'addr': addr, 'size': size, 'name': new_name,
                        'min_id' : min_id, 'maj_id': maj_id,
                        'maj_name': maj_scene_name, 'min_name': min_scene_name, }
                # If the function appears unique, add it to the list of output
                if (functions.get(addr) == None):
                    functions[addr] = entry

                # Otherwise, handle duplicates before commiting to the list
                else:

                    # MinID 0x80, 0x81, and 0xc0 are used consistently across
                    # certain major scenes in order to deal with having to 
                    # move into new scenes for unlocking characters: 0x80 is
                    # for the "Challenger Approaching" message, 0x81 is used
                    # while in-game during the match, and 0xc0 is used for the
                    # message displayed when a character is finally unlocked 

                    if (addr == 0x801bfa6c):
                        functions[addr]['name'] = "MajorScene_Generic_ChallengerApproachMsg_Prep"
                        continue
                    if (addr == 0x801bfabc):
                        functions[addr]['name'] = "MajorScene_Generic_ChallengerInGame_Prep"
                        continue
                    if (addr == 0x801a6254): 
                        functions[addr]['name'] = "MajorScene_Generic_ChallengerInGame_Decide"
                        continue
                    if (addr == 0x801bfcfc): 
                        functions[addr]['name'] = "MajorScene_Generic_ChallengerUnlockedMsg_Prep"
                        continue
                    if (addr == 0x801a6308): 
                        functions[addr]['name'] = "MajorScene_Generic_ChallengerUnlockedMsg_Decide"
                        continue

                    # In Classic and Adventure mode, each scene representing
                    # a match and each scene representing a splash screen in
                    # between matches are indexed with unique minor scene ids.
                    # The underlying functions in this table are equal within
                    # each major.

                    if (addr == 0x801b3500): 
                        functions[addr]['name'] = "MajorScene_ClassicMode_Splash_Prep"
                        continue
                    if (addr == 0x801b3a34): 
                        functions[addr]['name'] = "MajorScene_ClassicMode_InGame_Prep"
                        continue
                    if (addr == 0x801b3b40): 
                        functions[addr]['name'] = "MajorScene_ClassicMode_InGame_Decide"
                        continue
                    
                    if (addr == 0x801b3f40): 
                        functions[addr]['name'] = "MajorScene_AdventureMode_Splash_Prep"
                        continue
                    if (addr == 0x801b4064): 
                        functions[addr]['name'] = "MajorScene_AdventureMode_InGame_Prep"
                        continue
                    if (addr == 0x801b4170): 
                        functions[addr]['name'] = "MajorScene_AdventureMode_InGame_Decide"
                        continue

                    # All of the minor scenes associated with cutscenes inside
                    # Adventure mode share the same functions here
                    if (addr == 0x801b4430):
                        functions[addr]['name'] = "MajorScene_AdventureMode_Cutscene_Prep"
                        continue

                    # In All-Star mode, all minor scenes where we are "in-game"
                    # are split into two types: one for matches, and one for the
                    # rest area in-between matches

                    if (addr == 0x801b5624): 
                        functions[addr]['name'] = "MajorScene_AllStarMode_InGame_Prep"
                        continue
                    if (addr == 0x801b59ac): 
                        functions[addr]['name'] = "MajorScene_AllStarMode_InGame_Decide"
                        continue
                    if (addr == 0x801b5acc): 
                        functions[addr]['name'] = "MajorScene_AllStarMode_InGameRest_Prep"
                        continue
                    if (addr == 0x801b5e7c): 
                        functions[addr]['name'] = "MajorScene_AllStarMode_InGameRest_Decide"
                        continue

                    # In the MainDebugMenu scene, the minor IDs 0x6, 0x7, 0x8,
                    # 0x9, 0xa, and 0xc share the same Decide function. This
                    # is probably because they all return back to the menu 
                    # after completion. These live in "MODE : KIM".

                    if (addr == 0x801b099c):
                        functions[addr]['name'] = "MajorScene_MainDebugMenu_ModeKimExit_Decide"
                        continue

                    # Various other functions that we can give generic names 

                    if (addr == 0x801b16a8):
                        functions[addr]['name'] = "MajorScene_VSMode_ResultScreen_Prep"
                        continue
                    if (addr == 0x801bef84):
                        functions[addr]['name'] = "MajorScene_1PMode_EndingMovie_Decide"
                        continue
                    if (addr == 0x801bee9c):
                        functions[addr]['name'] = "MajorScene_1PMode_Congratulations_Decide"
                        continue
                    if (addr == 0x801bf4dc):
                        functions[addr]['name'] = "MajorScene_OpeningMovie_Prep"
                        continue

                    print("Duplicate entry for addr {:08x}".format(addr))
                    print(json.dumps(entry))
                    print(json.dumps(functions[addr]))

        # Go to the next minor scene struct
        min_base += 0x18
 
    # Go to the next major scene struct 
    maj_base += 0x14



# Now, walk the shared minor scene function tables. The "shared_id" in the 
# minor scene entries (that we walked above) correspond to some entry within
# this array of tables. Entry number 0x6 is missing in this array.

shared_base = 0x803da920
for scene in (minSceneShared):

    # Skip over entry 0x6 (array members 0x5 and 0x7 are adjacent)
    if (scene.value == 6):
        continue

    shared_ft = minor_scene_shared_ft(u32table(dump(shared_base, 0x14)))
    shared_id = shared_ft.shared_id
    shared_name = minSceneShared(shared_id).name

    # Construct an entry for each function in the major table
    for funcname in shared_ft.functions:
        addr = shared_ft.functions[funcname]
        if (validptr(addr)):
            size = getsymbolsize(addr)
            new_name = "{}_{}_{}".format("MinorSceneShared", shared_name, funcname)
            entry = {'addr': addr, 'size': size, 'name': new_name,
                    'shared_id': shared_id }

            # If the function appears unique, add it to the list of output
            if (functions.get(addr) == None):
                functions[addr] = entry
            else:

                # The `Leave` Functions for these three "in-game" types are 
                # equivalent (across IDs 0x2, 0x3, and 0x4)

                if (addr == 0x8016e9c8):
                    functions[addr]['name'] = "MinorSceneShared_InGame_Leave"
                    continue

                # For `Think` functions with "in-game" types, only the Sudden
                # Death and normal InGame types are shared (and the InGame
                # scene for Training Mode is different).

                if (addr == 0x8016d800):
                    functions[addr]['name'] = "MinorSceneShared_InGame_Think"
                    continue

                print("Duplicate entry for addr {:08x}".format(addr))
                print(json.dumps(entry))
                print(json.dumps(functions[addr]))

    # Go to the next struct
    shared_base += 0x14


# Print symbols to standard output
for addr in functions:
    size = functions[addr]['size']
    name = functions[addr]['name']
    print(MAPFMT.format(addr, size, addr, name))
