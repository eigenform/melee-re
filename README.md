![hosaka-corp/melee-re](banner.png)

<br>

This is a collection of scripts and technical documentation used for analyzing
Super Smash Bros. Melee. Right now there basically three or four goals for this project:

- Have tools for walking function tables and other data structures, for automatically
generating symbols used to annotate disassembly
- Approach a complete symbol map for NTSC v1.02
- Collect documentation on various game implementation details, data structures, etc.
- Collect various other tools for understanding the game


## Documentation

| Table-of-Contents  | 
| ------------- | 
| [Notes on the DOL/memory layout](docs/LINKERMAP.md)   |
| [Notes on various data structures/function tables](docs/STRUCT.md)    |
| [Notes on Melee's debug menu functionality](docs/DEBUG.md) |

## Function Table Analysis (`5809` functions named so far)
**Note:** If you'd like to see a copy of my whole symbol map, you can look
at [`meta_GALE01.map`](meta_GALE01.map). Note that this map may not include
the latest automatically-generated symbols from the analysis scripts.

The `py/analysis/` directory contains scripts which are intended to be used
with a Dolphin ram-dump and GALE01 symbol file. These scripts will walk various
function tables and produce symbols. They currently expect that you move a 
`ram.raw` and `GALE01.map` into the directory, in case you want to run them
on your own ram-dump and map.

Many functions are re-used across/within different tables. The process of pruning 
duplicate symbols is complicated and on-going. The re-use of functions across 
different tables often encodes certain decisions about how the game was implemented,
and sometimes these relationships are not obvious. The convention for symbol names is
also up-in-the-air right now.

The [`function_table_analysis.map`](py/analysis/function_table_analysis.map) 
in this directory contains my copy of all script output which _should_ result 
in a list of unique functions. As of right now, there are no guarantees that 
this file is free of duplicates, so be careful if you decide to merge this 
into your current symbol map.


## Tools  
The `py/` directory contains all of the scripts I've collected for doing some
analysis on Melee (specifically, on the executable, or on Dolphin RAM dumps).
Here's a rough set of descriptions for some of them:

```
py/
├── analysis
│   ├── char_global_as.py		# Dump symbols from global action-state function tables
│   ├── char_specific_anim.py		# Dump symbols from character-specific animation function tables
│   ├── char_specific_as.py		# Dump symbols from character-specific action-state function tables
│   ├── mapmerge			# Merge Dolphin symbol maps (very hacky)
│   ├── ntsc102_defs.py			# Definitions specific to NTSC v1.02
│   ├── ramdump_util.py			# Utility functions for analyzing Dolphin ram dumps
│   ├── scene_tables.py			# Dump symbols from scene-specific function tables
│   └── stage_tables.py			# Dump symbols from stage-specific function tables
├── dolparse				# Parse DOL headers
└── melee-stack-dump			# Unwind call chains from a ram dump of the stack region
```

