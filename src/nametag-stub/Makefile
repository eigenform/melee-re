
PREFIX		:= powerpc-eabi
OBJCOPY		:= $(PREFIX)-objcopy
CC		:= $(PREFIX)-gcc
LD		:= $(PREFIX)-ld

# Earliest entrypoint afforded by the nametag exploit (?)
ENTRY		:= 0x8045d930

# Symbol definitions for game functions
SYM		:= ssbm_ntsc_usa_12.sym
LS		:= wparam-nametag.ld

ASFLAGS		:= -mregnames -c
C_CCFLAGS	:= -s -Qn -Wa,$(ASFLAGS)
OBJFLAGS	:= -O binary --only-section=.text
LDFLAGS 	:= --just-symbols=$(SYM) -T $(LS) \
		   --section-start=.text=$(ENTRY)

.PHONY: clean
all: loader.bin

# Entrypoint stub in assembly; program body written in C
entry.o: entry.S
	$(CC) $(ASFLAGS) $< -o $@
main.o: main.c
	$(CC) $(C_CCFLAGS) $< -o $@

# Link everything up and strip the ELF container
loader.elf: main.o entry.o
	$(LD) $(LDFLAGS) entry.o main.o -o $@
loader.bin: loader.elf
	$(OBJCOPY) $(OBJFLAGS) $< $@

clean:
	rm -fv entry.o main.o loader.{bin,elf}
