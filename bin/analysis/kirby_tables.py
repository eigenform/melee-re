#!/usr/bin/python3
""" kirby_tables.py - Pull symbols from Kirby's tables
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


base = 0x803c9cc8
functions = {}

ft = u32table(dump(base, 0x100))
for ptr in ft:
    print(hex(ptr))


