#!/usr/bin/python3

import os, sys
import struct
import binascii

from meleegci import *

DATA_BLOCK_SIZE = 0x1fe0

# Haplessly taken from https://github.com/rgov - thanks!
# See https://gist.github.com/rgov/891712 for original source
def deBruijn(n, k):
   '''
   An implementation of the FKM algorithm for generating the de Bruijn
   sequence containing all k-ary strings of length n, as described in
   "Combinatorial Generation" by Frank Ruskey.
   '''
   a = [ 0 ] * (n + 1)
   def gen(t, p):
      if t > n:
         for v in a[1:p + 1]:
           yield v
      else:
         a[t] = a[t - p]
         for v in gen(t + 1, p):
           yield v
         for j in range(a[t - p] + 1, k):
            a[t] = j
            for v in gen(t + 1, t):
              yield v
   
   return gen(1, 1)


if len(sys.argv) < 3:
    print("Usage: test.py <input> <output>")
    exit(0)
else:
    input_fn = sys.argv[1]
    output_fn = sys.argv[2]

# -----------------------------------------------------------------------------
# Load an unpacked Melee GCI into memory
input_gci = gci(input_fn)
print("Read GCI: {}".format(input_gci.get_filename()))

# -----------------------------------------------------------------------------
# Perform some transformations on the GCI here

# Map debruijn sequence over all data blocks to help determine layout in RAM
cyclic = bytearray(''.join([ chr(ord('a') + x) for x in deBruijn(4, 26) ]).encode('utf8'))

input_gci.set_block(0, cyclic[0:DATA_BLOCK_SIZE])
print("Cyclic offset 0x0 starts at GCI block 0".format(hex(DATA_BLOCK_SIZE)))
print("(should be {})".format(cyclic[0:0x4]))
print()

input_gci.set_block(1, cyclic[DATA_BLOCK_SIZE:(DATA_BLOCK_SIZE*2)])
print("Cyclic offset {} starts at GCI block 1".format(hex(DATA_BLOCK_SIZE)))
print("(should be {})".format(cyclic[DATA_BLOCK_SIZE:DATA_BLOCK_SIZE+4]))
print()

input_gci.set_block(2, cyclic[(DATA_BLOCK_SIZE*2):(DATA_BLOCK_SIZE*3)])
print("Cyclic offset {} starts at GCI block 2".format(hex(DATA_BLOCK_SIZE*2)))
print("(should be {})".format(cyclic[DATA_BLOCK_SIZE*2:DATA_BLOCK_SIZE*2+4]))
print()

input_gci.set_block(3, cyclic[(DATA_BLOCK_SIZE*3):(DATA_BLOCK_SIZE*4)])
print("Cyclic offset {} starts at GCI block 3".format(hex(DATA_BLOCK_SIZE*3)))
print("(should be {})".format(cyclic[DATA_BLOCK_SIZE*3:DATA_BLOCK_SIZE*3+4]))
print()

input_gci.set_block(4, cyclic[(DATA_BLOCK_SIZE*4):(DATA_BLOCK_SIZE*5)])
print("Cyclic offset {} starts at GCI block 4".format(hex(DATA_BLOCK_SIZE*4)))
print("(should be {})".format(cyclic[DATA_BLOCK_SIZE*4:DATA_BLOCK_SIZE*4+4]))
print()

input_gci.set_block(5, cyclic[(DATA_BLOCK_SIZE*5):(DATA_BLOCK_SIZE*6)])
print("Cyclic offset {} starts at GCI block 5".format(hex(DATA_BLOCK_SIZE*5)))
print("(should be {})".format(cyclic[DATA_BLOCK_SIZE*5:DATA_BLOCK_SIZE*5+4]))
print()

input_gci.set_block(6, cyclic[(DATA_BLOCK_SIZE*6):(DATA_BLOCK_SIZE*7)])
print("Cyclic offset {} starts at GCI block 6".format(hex(DATA_BLOCK_SIZE*6)))
print("(should be {})".format(cyclic[DATA_BLOCK_SIZE*6:DATA_BLOCK_SIZE*6+4]))
print()

input_gci.set_block(7, cyclic[(DATA_BLOCK_SIZE*7):(DATA_BLOCK_SIZE*8)])
print("Cyclic offset {} starts at GCI block 7".format(hex(DATA_BLOCK_SIZE*7)))
print("(should be {})".format(cyclic[DATA_BLOCK_SIZE*7:DATA_BLOCK_SIZE*7+4]))
print()

input_gci.set_block(8, cyclic[(DATA_BLOCK_SIZE*8):(DATA_BLOCK_SIZE*9)])
print("Cyclic offset {} starts at GCI block 8".format(hex(DATA_BLOCK_SIZE*8)))
print("(should be {})".format(cyclic[DATA_BLOCK_SIZE*8:DATA_BLOCK_SIZE*8+4]))
print()

# It looks like the regions that are contiguous in memory are each 0x1f2c-bytes
#
# Block 5 (kyap) starts at 8045d6b8 - 8045f5e4
#   From 0xc060 to 0xdf8c incl.

# Block 3 (najf) starts at 8045f5e4
#   From  0x8060 to 0x9f8c incl.

# Block 2 (agdj) starts at 80461510
#   From  0x6060 to 0x7f8c incl.

# Block 6 (easo) starts at 8046343c
#   From 0xe060 to 0xff8c incl.

# Block 8 (ayvs) starts at 80465368
#   From 0x12060 to 0x13f8c incl.

# Black 7 (tavr) starts at 80467294
#   From 0x10060 to 0x11f8c incl.

# Block 4 (bami) starts at 804691c0
#   From 0xa060 to 0xbf8c incl.


# -----------------------------------------------------------------------------
# Write the new GCI to a file
print("Writing to {}".format(output_fn))
ofd = open(output_fn, "wb")
ofd.write(input_gci.raw_bytes)
ofd.close()

# Write the cyclic bytes 
print("Writing cyclic pattern to /tmp/cyclic.string")
ofd = open('/tmp/cyclic.string', "wb")
ofd.write(cyclic)
ofd.close()


