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

## Function Table Analysis (`7201` functions named so far)
**Note:** If you'd like to see a copy of my whole symbol map, you can look
at [`meta_GALE01.map`](meta_GALE01.map). Note that this map may not include
the latest automatically-generated symbols from the analysis scripts.

The `py/analysis/` directory contains scripts which are intended to be used
with a Dolphin ram-dump and GALE01 symbol file. These scripts will walk various
function tables and produce symbols. They currently expect that you move a 
`ram.raw` and `GALE01.map` into the directory, in case you want to run them
on your own ram-dump and map.

The [`function_table_analysis.map`](py/analysis/function_table_analysis.map) 
in this directory contains my copy of all script output which _should_ result 
in a list of unique functions. This list *should* be free of duplicates,
but it's always possible that I may have missed something, so keep that in
mind if you're merging this with your map.

Many functions are re-used across/within different tables. The process of pruning 
duplicate symbols is complicated right now: especially considering that these 
scripts are somewhat hacky at the moment. The re-use of functions across different 
tables often encodes certain decisions about how the game was implemented, and 
sometimes these relationships are not obvious, which makes naming the actual
symbols kind of difficult. There are a lot of cases where, in the absence of
a more "generic" name for some symbol, I've opted to simply rename symbols with
the set of table indicies or ID values that they're used across. 


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

