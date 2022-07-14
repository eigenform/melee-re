# meleegci-py
A Python library and example programs for manipulating Super Smash Bros. Melee 
savefiles.

**NOTE:** You probably don't want to use any of this code (it's kind of old), 
and it might be more useful as documentation. I'm keeping it in this repo 
solely for reference. For a more complete solution, consider looking at
[dansalvato/melee-gci-compiler](https://github.com/dansalvato/melee-gci-compiler).

```
├── cyclic.py		# Script for fuzzing the memory card region layout
├── data/		    # Savefile templates
├── fill-snapshot	# Fill a snapshot file with data
├── meleegci.py		# Library for manipulating savefiles
├── prepare-ace		# Prepare a savefile with wParam's nametag exploit
├── README.md		# This file
├── savefile		# [Un]pack a regular savefile
├── snapshot		# [Un]pack a snapshot
└── ssbmpack.py		# Library wrapping libssbmpack.so
```

## About wParam's Nametag Exploit
See wParam's original write-up [here](http://wparam.com/ssbm/exploit.html) 
for more reference. 

This is a classic stack-smashing exploit. The call stack in question looks 
like this:

```
80239a24
  803a6b98
    80323dc8 (vsprintf)
      80324044 (__pformatter)
        80323f80 (__StringWrite)
          800031f4 (memmove)
```

1. Upon entering the parent at `803a6b98`, we save the return address 
   (normally `0x80239e44`) on the first word after the stack pointer 
   (in this case, where `r1=0x804ee828`).

2. `strchr()` and `strlen()` calls inside of `__pformatter()` determine the 
   length of the copy. `vsprintf()` is rendering a string onto the stack.

3. There are probably a handful of different ways to groom input in order to 
   get this behaviour, but the `memmove` call in the example I'm working with 
   (the 20XXTE UCF savefile) is something like `memmove(0x804ee830, 0x8045d92c, 0xdd)`. 

The `memmove` call in this path immediately writes over the stored LR used to 
return from the parent function at `803a6b98`. Arbitrary code execution starts 
when `803a6b98` returns. 


### Savefile layout (in GCI)
All of the information in wParam's original write-up references addresses of 
savefiles loaded in memory. This view of the layout includes offsets within 
*unpacked* savefiles. 

**NOTE:** `memmove` copies "up" the GCI moving from high-to-low addresses.

| In-memory Address | Unpacked GCI Offset  | Description |
| ------------- | ------------- | ------------- |
| 0x8045d850 | 0x41f8 | Top of corrupted nametag data |
| 0x8045d924 | 0x42cc | Second word copied by `memmove` (other stack data - maybe doesn't matter?) |
| 0x8045d928 | 0x42d0 | First word copied by `memmove` (the user-controlled target LR)  |
| 0x8045d92c | 0x42d4 | Word of NUL bytes (for terminating the copy) |


