# Global Structures


## Generic Animation/Action-State function tables
`0x803c2800` is the base of an array of function pointer tables that seem to 
hold either animation-specific or action-state-specific functions. These are 
probably for more general animations/action-states shared between all characters.
There seem to be 341 entries of 0x20 bytes. I _believe_ that this array is 
indexed by action state ID. The ID _inside_ these structures _is not_ the
action state ID.

```
// 0x20 bytes long
struct anim_func_table
{

/* This is not an action state ID. Some are set to -1. This is also an index 
 * into some 24-byte wide structures up on the heap somewhere (typically high 
 * memory? ie. 0x81zzzzzz). Mechanics not understood yet.
 */
	u32 id;

/* UP has a lot of notes that suggest these are bitfields
 */
	u32 unk_flags0;
	u32 unk_flags1;

/* These function pointers are not always unique to a particular entry in
 * the whole array.
 */
	unk_t (animationInterrupt*)(...);

	// UP has this labeled as "IASA interrupt"
	unk_t (inputInterrupt*)(...);		

	unk_t (actionPhysics*)(...);
	unk_t (collisionInterrupt*)(...);
	unk_t (cameraBehaviour*)(...);
}

struct anim_func_table[341] = (struct anim_func_table*)0x803c2800;
```


## Character-specific Animation/Action State function tables
`struct anim_func_table` (in the section above) is also used to hold animation 
data for character-specific states. 

`0x803c12e0` is an array of pointers (apparently 0x90 bytes in length) to some arrays
of `struct anim_func_table`. They are indexed by the internal character ID.
This pointer to some table of `struct anim_func_table` is linked into the player 
block. The length of each character's array is different (and unknown right now).
The entry lowest in memory is at `0x803c7120` (for Mario), and the entry highest 
in memory is at `0x803d41f8` (Crazy Hand). There is some [yet unarticulated]
mapping from animation ID to action state which is different per-character.

### Special B Moves
`0x803c13e8` is the start of an array of 8 function pointer tables, each of
0x84 bytes (indexed by internal character ID), holding action-state functions 
for all special B moves.

### onHit Table
`0x803c1cac` is an array of pointers to functions, indexed by internal character ID,
which appear to be functions called when characters are hit.


### onRespawn Table
`0x803c1ebc` is an array of pointers to functions, indexed by internal character ID,
which appear to be functions called when characters respawn.

### Item Action Table
`0x803c1808` is the base of 7 adjacent, 0x84-byte function pointer tables indexed
by internal character ID. Their order is approximately:

- "onAbsorb"
- "onItemPickup"
- "onMakeItemInvisible"
- "onMakeItemVisible"
- "onItemDrop"
- "onItemCatch" (always equivalent to the "onItemPickup" table)
- "unkItemRelated" (always equivalent to the "onItemDrop" table, except for Link/YLink)


### Unknown tables
`0x803c1d30` is an array of pointers to functions, indexed by internal character ID.

`0x803c1db4` is an array of pointers to functions, indexed by internal character ID.
Functions are zeroed out for many characters, except Kirby, Bowser, and Giga-Bowser (???).


`0x803c1ba4` and `0x803c1c28` are two arrays of pointers to functions, indexed by 
internal character ID. There are only entries for Pikachu (???).


`0x803c21d4` is an array of pointers to functions, indexed by internal character ID.
There are only entries for Jigglypuff and Kirby.



```
// 0x84 bytes
struct move_table
{
	unk_t (*actionstate_func[0x20])(...);
	u32 pad; // zeroed out
};
```

- `0x803c13e8` - Grounded Side-B
- `0x803c146c` - Up-B
- `0x803c14f0` - Aerial Down-B
- `0x803c1574` - Unknown
- `0x803c15f8` - Aerial Neutral-B
- `0x803c167c` - Grounded Neutral-B
- `0x803c1700` - Grounded Down-B
- `0x803c1784` - Unknown


## Table of pointers to Stage-specific Function Tables

There's a table of pointers, `0x1bc` bytes long, starting at `803dfedc`.
Each of these pointers is a stage-specific function table. They are
arranged according to the "internal stage ID." 

There's also a pointer to a different table of function pointers, 
but the table itself isn't always populated, and is missing for 
the following stages:

- Princess Peach's Castle
- Kongo Jungle
- Brinstar
- Yoshi's Story
- Pokemon Stadium
- Mute City
- Onett

```
// Ox14 bytes long
struct stage_func_subtable
{
	unk_t (*func1)(...);
	unk_t (*func2)(...);
	unk_t (*func3)(...);
	unk_t (*func4)(...);
	u32 pad; // zeroed out
};

// 0x30 bytes long
struct stage_func_table
{
	u32 internal_id;

	struct *stage_func_subtable;
	char *stage_filename;

/* For many stages, some of these are pointers to functions that simply
 * return zero or non-zero. If I had to guess: it probably depends on how 
 * complicated some stage geometry is, or something.

	unk_t (*StageInit)(...);
	unk_t (*unk_1)(...);
	unk_t (*OnLoad)(...);
	unk_t (*OnGO)(...);
	unk_t (*unk_3)(...);

/* For some stages, these are spatially distinct from the ones above.
 * I believe these are dispatched once [or more times] per-frame.
 */
	unk_t (*unk_4)(...);
	unk_t (*unk_5)(...);


/* Don't know what these three words are for, yet. */

	u32 unk_0;
	unk_t *unk_1;
	unk_t *unk_2;

};

struct stage_func_table[0x70] = (struct stage_func_table*)0x803dfedc;
```

## 



## Heap Data

Some kind of heap starts at `0x80bd5c40`. Entries for objects always look
like this:

```
struct heap_object
{
    struct heap_object *next;
    struct heap_object *prev;
    u32 size;
    char data[size];
};

```

This may be only _one particular_ kind of region for dynamic allocations.
I don't know which one it is, yet.
