
MEXTK_HEADERS 	:= /home/meta/src/m-ex/MexTK/include/

# Use of --nmagic here is just to avoid phdr alignment (otherwise all the file
# offsets are inflated unnecessarily, though I'm not sure why)

PAL_LINK 	:= pal.ld
NTSC_LINK 	:= ntsc102.ld
LDFLAGS 	:= -Wl,--script=$(NTSC_LINK),--nmagic,--sdata-got

CFLAGS 		:= -mcpu=750 -mbig-endian -mhard-float
CFLAGS 		+= -nostdlib -fno-asynchronous-unwind-tables
CFLAGS 		+= -fdata-sections -O0
CFLAGS 		+= -I$(MEXTK_HEADERS)

all:
	# Compile the actual function
	powerpc-eabi-gcc $(CFLAGS) $(LDFLAGS) scene_change.c -o scene_change.elf
	powerpc-eabi-objdump -t scene_change.elf
	powerpc-eabi-objcopy -O binary scene_change.elf scene_change.bin
	powerpc-eabi-as scene_change_hook.s -o hook.o
	# Lol this is so cursed, all this work just to emit a branch :^)
	powerpc-eabi-ld --defsym EngineTemplate=0x8019628c \
		--section-start .text=0x801a40f0 \
		hook.o -o hook.elf
	powerpc-eabi-objcopy -O binary hook.elf hook.bin
	# Translate everything into Gecko codes
	gecko build -c build_ntsc102.json

clean:
	rm -rfv *.o *.bin *.elf
