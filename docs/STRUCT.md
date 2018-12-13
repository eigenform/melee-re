# Global Structures


## Generic Animation/Action-State function tables
`0x803c2800` is the base of an array of function pointer tables that seem to 
hold either animation-specific or action-state-specific functions. These are 
probably for more general animations/action-states shared between all characters.
There seem to be 341 entries of 0x20 bytes. I _believe_ that this array is 
indexed by action state ID. The ID _inside_ these structures however _is not_ the
action state ID.

```c
// 0x20 bytes long
struct anim_ft
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

struct anim_ft global_as_ft[341] = (struct anim_ft*)0x803c2800;
```

-------------------------------------------------------------------------------

## Character-specific Animation/Action State function tables
`struct anim_ft` (in the section above) is also used to hold animation 
data for certain character-specific states. 

`0x803c12e0` is an array of pointers (apparently 0x90 bytes in length) 
to some arrays of `struct anim_ft`. They are indexed by the internal 
character ID. This pointer to some table of `struct anim_ft` is linked 
into the player block. The length of each character's array is different 
(and unknown right now). These mostly seem relevant to animations for
a character's special move-set. The entry lowest in memory is at 
`0x803c7120` (for Mario), and the entry highest in memory is at 
`0x803d41f8` (Crazy Hand). There is some [yet unarticulated] mapping 
from animation ID to action state which is different per-character.

### Special B Moves
`0x803c13e8` is the start of an array of 8 function pointer tables, each of
0x84 bytes (indexed by internal character ID), where each word is a pointer
to some action-state function for all special B moves.

| Virtual Address | Function name |
| ------------- | ------------- |
| 0x803c13e8    | `GroundSideB?` |
| 0x803c146c    | `UpB?` |
| 0x803c14f0    | `AerialDownB?` |
| 0x803c1574    | `Unk1_BMove` |
| 0x803c15f8    | `AerialNeutralB?` |
| 0x803c167c    | `GroundNeutralB?` |
| 0x803c1700    | `GroundDownB?` |
| 0x803c1784    | `Unk2_BMove` |


### Item Action Table
`0x803c1808` is the base of 7 adjacent, 0x84-byte function pointer tables indexed
by internal character ID. Their order is approximately:

| Virtual Address | Function name |
| ------------- | ------------- |
| 0x803c1808    | `onAbsorb` |
| 0x803c188c    | `onItemPickup` |
| 0x803c1910    | `onMakeItemInvisible` |
| 0x803c1994    | `onMakeItemVisible` |
| 0x803c1a18    | `onMakeItemDrop` |
| 0x803c1a9c    | `onMakeItemCatch` (always equivalent to the `onItemPickup` function |
| 0x803c1b20    | `unkItemRelated` (always equivalent to the `onItemDrop` function |


### Unknown tables
Tables to functions indexed by internal character ID. Not well understood.

| Virtual Address | Function name |
| ------------- | ------------- |
| 0x803c1ba4    | `unkPika1`, only entries for Pikachu's internal character ID |
| 0x803c1c28    | `unkPika2`, |
| 0x803c1cac    | `onHit?`|
| 0x803c1d30    | `onUnk?`|
| 0x803c1db4    | `unk_`, only entries for Kirby, Bowser, and Giga-Bowser? |
| 0x803c1e38    | `chargeNeutralB`, only entries for characters who charge neutral B?|
| 0x803c1ebc    | `onRespawn`|
| 0x803c21d4    | `unkJump2`, only entries for Puff and Kirby?|

-------------------------------------------------------------------------------

## Table of pointers to Stage-specific Function Tables
There's a table of pointers, `0x1bc` bytes long, starting at `0x803dfedc`.
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

```c
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

-----------------------------------------------------------------------------

## Item-related function tables
Depending on the item ID, various related function tables are stored
in different arrays. Each of the following are arrays of `struct item_ft`.
The mapping appears to be:

| Item class | Item ID range | Virtual address |
| ------------- | ------------- | -------------- |
| Regular items | 0x000 - 0x02a | 0x803f14c4 |
| Character projectiles, monsters | 0x02b - 0x0a0 | 0x803f3100 |
| Pokemon | 0x0a1 - 0x0cf | 0x803f23cc |
| Stage-specific items | ??? | 0x803f4d20 |


```c
struct item_ft
{
	void *unk_0; // Pointer to something with other functions?

	unk_t (*OnCreate)(...);
	unk_t (*OnDestroy)(...);
	unk_t (*OnPickup)(...);
	unk_t (*OnRelease)(...);
	unk_t (*OnThrow)(...);
	unk_t (*OnHitCollision)(...);
	unk_t (*OnTakeDamage)(...);
	unk_t (*OnReflect)(...);
	unk_t (*OnShieldCollision0?)(...);
	unk_t (*OnCollision_unk2?)(...);
	unk_t (*unk_5)(...);
	unk_t (*OnShieldCollision1?)(...);
	unk_t (*OnShieldCollision2?)(...);
	unk_t (*unk_8)(...);
};
```

-------------------------------------------------------------------------------

## Scene function tables

Melee is organized into certain "major scenes," each of which contain associated
"minor scenes." Major scenes all have unique IDs, and minor scenes have IDs
which are only unique within some associated major scene. All minor scenes
also have a different ID, called the "class ID," which refers
to some generic class of scene.

The array of major scene function tables begins at `0x803dacb8`, indexed by
the major scene ID.

```c
struct maj_scene_ft
{
	u8 preload;
	u8 major_scene_id;
	u8 unk_0;
	u8 unk_1;

	unk_t (*Load)(...);
	unk_t (*Unload)(...);
	unk_t (*Init)(...);

	struct min_scene_ft *min_scene_array;

};
```

Each of the `struct maj_scene_ft` refers to a variable-length array of 
minor scene function pointer tables. 

```c
struct min_scene_ft
{
	u8 minor_scene_id;
	u8 preload;
	u8 unk_0;
	u8 unk_1;

	unk_t (*Prep)(...);
	unk_t (*Decide)(...);

	u8 class_id;
	u8 unk_2;
	u8 unk_3;
	u8 unk_4;

	void *unk_struct_0;
	void *unk_struct_1;
};
```

The `class_id` for some minor scene is an index into an array of "minor scene 
class function tables" which hold generic functions shared among all minor 
scenes of that particular class. This array starts at `0x803da920`.

```c
struct min_scene_class_ft
{
	u8 class_id;
	u8 unk_0;
	u8 unk_1;
	u8 unk_2;

	unk_t (*Think)(...);
	unk_t (*Load)(...);
	unk_t (*Leave)(...);

	u32 unk_3;
};
```


-------------------------------------------------------------------------------

## Heap Data

Some kind of heap starts at `0x80bd5c40`. Entries for objects always look
like this:

```c
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
