
MEXTK_HEADERS 	:= /home/meta/src/m-ex/MexTK/include/

# Use of --nmagic here is just to avoid phdr alignment (otherwise all the file
# offsets are inflated unnecessarily, though I'm not sure why)

PAL_LINK 	:= pal.ld
LDFLAGS 	:= -Wl,--script=$(PAL_LINK),--nmagic,--sdata-got

# Some quick notes about codegen:
#
# You want -mlongcall so we emit branches with CTR.
#
# I went on a tangent trying to build this with -fpic, but it doesn't seem like
# GCC wants to correctly emit code that references constants via the GOT. It 
# grabs function addresses just fine, but it tries to resolve the offsets to 
# constants (the floats in scene_change.c) by just dereferencing them, instead
# of what it *should* be doing (just adding them to r30).
#
# Other option (currently used here) is to just know the base of the program at 
# compile-time (which we *can* know), but imho it's a bit less desirable.

CFLAGS 		:= -mlongcall -mcpu=750 -mbig-endian -mhard-float
CFLAGS 		+= -nostdlib -fno-asynchronous-unwind-tables
CFLAGS 		+= -fdata-sections -O3
CFLAGS 		+= -I$(MEXTK_HEADERS)

all:
	powerpc-eabi-gcc $(CFLAGS) $(LDFLAGS) scene_change.c -o scene_change.elf
	powerpc-eabi-objdump -t scene_change.elf
	powerpc-eabi-strip -R .comment -R .gnu.attributes scene_change.elf
	powerpc-eabi-objcopy -O binary scene_change.elf scene_change.bin
	gecko build -c build_pal.json

clean:
	rm -rfv *.o *.bin *.elf
