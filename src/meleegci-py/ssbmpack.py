#!/usr/bin/python3
""" ssbmpack.py - a simple Python wrapper around libssbmpack.so """

from ctypes import *
import os

# We expect the user to pass the path to libssbmpack.so
LIBSSBMPACK = os.getenv("LIBSSBMPACK")
if ((LIBSSBMPACK == "") or (LIBSSBMPACK == None)):
    print("err: Your shell must pass $LIBSSBMPACK with the path to libssbmpack.so")
    exit(-1)

try:
    ssbmpack = cdll.LoadLibrary(LIBSSBMPACK)
except OSError as e:
    print(e)
    exit(-1)

# Wrapper functions with ctypes
unpack = ssbmpack['decompress_byte']
unpack.argtypes = [c_uint8, c_uint8]
unpack.restype = c_uint8

pack = ssbmpack['compress_byte']
pack.argtypes = [c_uint8, c_uint8]
pack.restype = c_uint8
