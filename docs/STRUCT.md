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

| Virtual Address | Internal ID | Character Name  | Number of entries |
| --------------- | ----------- | --------------- | ----------------- |
| 0x803c7120      | 0           | Mario           | 12                |
| 0x803c72b8      | 1           | Captain Falcon  | 23                |
| 0x803c7788      | 2           | Fox             | 35                |
| 0x803c71e8      | 3           | Link            | 31                |
| 0x803c8368      | 4           | Kirby           | 203               |
| 0x803cb838      | 5           | Donkey Kong     | 46                |
| 0x803cc060      | 6           | Shiek           | 24                |
| 0x803cc650      | 7           | Ness            | 36                |
| 0x803cccb8      | 8           | Peach           | 30                |
| 0x803cd2d0      | 9           | Popo            | 26                |
| 0x803cd838      | 10          | Nana            | 26                |
| 0x803cdd78      | 11          | Pikachu         | 26                |
| 0x803ce2d0      | 12          | Samus           | 18                |
| 0x803ce6d0      | 13          | Yoshi           | 28                |
| 0x803cedc0      | 14          | Bowser          | 23                |
| 0x803cf420      | 15          | Marth           | 32                |
| 0x803cfa58      | 16          | Zelda           | 18                |
| 0x803cfef0      | 17          | Jigglypuff      | 32                |
| 0x803e0628      | 18          | Luigi           | 20                |
| 0x803e0b00      | 19          | Mewtwo          | 20                |
| 0x803e0fa0      | 20          | Young Link      | 21                |
| 0x803e1498      | 21          | Dr. Mario       | 10                |
| 0x803e1848      | 22          | Falco           | 35                |
| 0x803e1ea8      | 23          | Pichu           | 26                |
| 0x803e23e8      | 24          | Game n' Watch   | 40                |
| 0x803e29f8      | 25          | Ganon           | 23                |
| 0x803e2e80      | 26          | Roy             | 32                |
| 0x803e35e8      | 27          | Giga Bowser     | 23                |
| 0x803e3998      | 28          | Sandbag         | 1                 |
| 0x803e3a30      | 29          | Master Hand     | 50                |
| 0x803e41f8      | 30          | Crazy Hand      | 49                |


### Per-character function tables
This region in memory has a lot of function pointer tables, each of
0x84 bytes (indexed by internal character ID), where each word is a pointer
to some character-specific action-state function:

| Virtual Address | Function name |
| ------------- | ------------- |
| 0x803c1154    | `onLoad` |
| 0x803c11d8    | `playerblockOnDeath` |
| 0x803c125c    | Unknown - only an entry for Jigglypuff? |
| 0x803c12e0    | Table of pointers to anim_ft tables |
| 0x803c13e8    | `GroundSideB` |
| 0x803c146c    | `AerialUpB` |
| 0x803c14f0    | `AerialDownB` |
| 0x803c1574    | `AerialSideB` |
| 0x803c15f8    | `AerialNeutralB` |
| 0x803c167c    | `GroundNeutralB` |
| 0x803c1700    | `GroundDownB` |
| 0x803c1784    | `GroundUpB` |
| 0x803c1808    | `onAbsorb` |
| 0x803c188c    | `onItemPickup` |
| 0x803c1910    | `onMakeItemInvisible` |
| 0x803c1994    | `onMakeItemVisible` |
| 0x803c1a18    | `onMakeItemDrop` |
| 0x803c1a9c    | `onItemCatch` |
| 0x803c1b20    | `onMakeItemDrop` (aerial?) |
| 0x803c1ba4    | Unknown (only Pikachu has an entry?) |
| 0x803c1c28    | Unknown (only Pikachu has an entry?) |
| 0x803c1cac    | `onHit` |
| 0x803c1d30    | `onUnk` |
| 0x803c1db4    | Unknown (`perFrame`?) |
| 0x803c1e38    | `chargeNeutralB` |
| 0x803c1ebc    | `onRespawn` |

Kirby's table for transformations lives at `0x803c9cc8`.

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
 * complicated some stage geometry is, or something. */

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

| Virtual Address | Stage Name |
| --------------- | ---------- |
| 0x803e5764 | Test |
| 0x803e11a4 | Castle |
| 0x803e4ecc | Rainbow Cruise |
| 0x803e1800 | Kongo Jungle |
| 0x803e52e0 | Jungle Japes |
| 0x803e3f6c | Great Bay |
| 0x803e5130 | Temple |
| 0x803e1b2c | Brinstar |
| 0x803e4d0c | Brinstar Depths |
| 0x803e274c | Yoshi's Story |
| 0x803e51cc | Yoshi's Island |
| 0x803e0e5c | Fountain of Dreams |
| 0x803e76d0 | Green Greens |
| 0x803e1f08 | Corneria |
| 0x803e54cc | Venom |
| 0x803e1334 | Pokemon Stadium |
| 0x803e6a3c | Pokefloats |
| 0x803e33dc | Mute City |
| 0x803e2d20 | Big Blue |
| 0x803e2858 | Onett |
| 0x803e3d94 | Fourside |
| 0x803e4800 | Icicle Mountain |
| 0x803e4950 | Unused? |
| 0x803e4c00 | Mushroom Kingdom II |
| 0x803e7a00 | Flatzone |
| 0x803e6748 | Dreamland |
| 0x803e650c | Yoshi's Island 64 |
| 0x803e65e8 | Kongo Jungle 64 |
| 0x803e584c | Adventure Mode: Mushroom Kingdom? |
| 0x803e5988 | Adventure Mode: Hyrule? |
| 0x803e5e0c | Adventure Mode: Brinstar? |
| 0x803e617c | Adventure Mode: Unknown? |
| 0x803e7e38 | Battlefield |
| 0x803e7f90 | Final Destination |
| 0x803e7d34 | Snag Trophies |
| 0x803e7b10 | Race to the Finish |
| 0x803e85a4 | Target Test: Mario |
| 0x803e8664 | Target Test: Captain Falcon |
| 0x803e872c | Target Test: Young Link |
| 0x803e87ec | Target Test: Donkey Kong |
| 0x803e88ac | Target Test: Dr. Mario |
| 0x803e8974 | Target Test: Falco |
| 0x803e8a34 | Target Test: Fox |
| 0x803e8af4 | Target Test: ICs |
| 0x803e8c0c | Target Test: Kirby |
| 0x803e8ccc | Target Test: Bowser |
| 0x803e8d8c | Target Test: Link |
| 0x803e8e4c | Target Test: Luigi |
| 0x803e8f0c | Target Test: Marth |
| 0x803e8fcc | Target Test: Mewtwo |
| 0x803e908c | Target Test: Ness |
| 0x803e914c | Target Test: Peach |
| 0x803e920c | Target Test: Pichu |
| 0x803e92cc | Target Test: Pikachu |
| 0x803e9394 | Target Test: Jigglypuff |
| 0x803e9454 | Target Test: Samus |
| 0x803e9514 | Target Test: Shiek |
| 0x803e95d4 | Target Test: Yoshi |
| 0x803e9694 | Target Test: Zelda |
| 0x803e9754 | Target Test: Game n' Watch |
| 0x803e981c | Target Test: Roy |
| 0x803e98dc | Target Test: Ganon |
| 0x803e84c4 | All-star Rest stage |
| 0x803e821c | Home Run Contest |
| 0x803e62c0 | Trophy1 |
| 0x803e6370 | Trophy2 |
| 0x803e6420 | Trophy3 |


The `stage_func_subtable` pointer in each of these structures points to some 
variable-length array of subtables containing functions for stage entities:

| Virtual Address | Number of entries | Stage Name             |
| --------------- | ----------------- | ---------------------- |
| 0x803e0d74      | 11	              | Fountain of Dreams |
| 0x803e0ff4      | 21	              | Peach's Castle |
| 0x803e126c      | 10	              | Pokemon Stadium |
| 0x803e1704      | 12	              | Kongo Jungle |
| 0x803e1a30      | 12	              | Brinstar |
| 0x803e1d8c      | 19	              | Corneria |
| 0x803e26f0      | 4	              | Yoshi's Story |
| 0x803e27e0      | 6	              | Onett |
| 0x803e29e0      | 41	              | Big Blue |
| 0x803e30c4      | 39	              | Mute City |
| 0x803e3cfc      | 7	              | Fourside |
| 0x803e3e84      | 11	              | Great Bay |
| 0x803e4718      | 11	              | Icicle Mountain |
| 0x803e48f4      | 4	              | Unused |
| 0x803e4ab4      | 16	              | Mushroom Kingdom II |
| 0x803e4c9c      | 5	              | Brinstar Depths |
| 0x803e4e34      | 7	              | Rainbow Cruise |
| 0x803e50e8      | 3	              | Temple |
| 0x803e5198      | 2	              | Yoshi's Island |
| 0x803e5248      | 7	              | Jungle Japes |
| 0x803e538c      | 16	              | Venom |
| 0x803e5708      | 4	              | Adventure Mode: ?? |
| 0x803e57f0      | 4	              | Adventure Mode: ?? |
| 0x803e58f0      | 7	              | Adventure Mode: ?? |
| 0x803e5db0      | 4	              | Adventure Mode: ?? |
| 0x803e5e78      | 38	              | Adventure Mode: ?? |
| 0x803e6278      | 3	              | Trophy 1 |
| 0x803e6328      | 3	              | Trophy 2 |
| 0x803e63d8      | 3	              | Trophy 3 |
| 0x803e6488      | 6	              | Yoshi's Island 64 |
| 0x803e658c      | 4	              | Kongo Jungle 64 |
| 0x803e6688      | 9	              | Dreamland |
| 0x803e6800      | 28	              | Pokefloats |
| 0x803e7638      | 7	              | Green Greens |
| 0x803e7940      | 9	              | Flatzone |
| 0x803e7ac8      | 3	              | Race to the Finish |
| 0x803e7d00      | 2	              | Snag Trophies |
| 0x803e7da0      | 7	              | Battlefield |
| 0x803e7ebc      | 10	              | Final Destination |
| 0x803e8140      | 11	              | Home Run Contest |
| 0x803e8454      | 5	              | All-star Rest area |
| 0x803e8548      | 4	              | Target Test: Mario |
| 0x803e8608      | 4	              | Target Test: Captain Falcon |
| 0x803e86d0      | 4	              | Target Test: Young Link |
| 0x803e8790      | 4	              | Target Test: Donkey Kong  |
| 0x803e8850      | 4	              | Target Test: Dr. Mario |
| 0x803e8918      | 4	              | Target Test: Falco |
| 0x803e89d8      | 4	              | Target Test: Fox |
| 0x803e8a98      | 4	              | Target Test: ICs |
| 0x803e8bb0      | 4	              | Target Test: Kirby |
| 0x803e8c70      | 4	              | Target Test: Bowser |
| 0x803e8d30      | 4	              | Target Test: Link |
| 0x803e8df0      | 4	              | Target Test: Luigi |
| 0x803e8eb0      | 4	              | Target Test: Marth |
| 0x803e8f70      | 4	              | Target Test: Mewtwo |
| 0x803e9030      | 4	              | Target Test: Ness |
| 0x803e90f0      | 4	              | Target Test: Peach |
| 0x803e91b0      | 4	              | Target Test: Pichu |
| 0x803e9270      | 4	              | Target Test: Pikachu |
| 0x803e9338      | 4	              | Target Test: Jigglypuff |
| 0x803e93f8      | 4	              | Target Test: Samus |
| 0x803e94b8      | 4	              | Target Test: Sheik |
| 0x803e9578      | 4	              | Target Test: Yoshi |
| 0x803e9638      | 4	              | Target Test: Zelda |
| 0x803e96f8      | 4	              | Target Test: Game n' Watch |
| 0x803e97c0      | 4	              | Target Test: Roy |
| 0x803e9880      | 4	              | Target Test: Ganon |

-----------------------------------------------------------------------------

## Item-related function tables
Depending on the item ID, various related function tables are stored
in different arrays. Each of the following are arrays of `struct item_ft`.
The mapping appears to be:

| Virtual Address | Item class/description    | Item ID range |
| ------------- | --------------------------- | ------------- |
| 0x803f14c4    | Regular items               | 0x000 - 0x02a |
| 0x803f3100    | Projectiles, monsters       | 0x02b - 0x0a0 | 
| 0x803f23cc    | Pokemon                     | 0x0a1 - 0x0cf | 
| 0x803f4d20    | Stage-specific items        | Unknown?      | 


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
scenes of that particular class. This array (45 entires) starts at `0x803da920`.

```c
struct min_scene_class_ft
{
	u8 class_id;
	u16 unk;
	u8 unk;

	unk_t (*OnFrame)(...);
	unk_t (*OnLoad)(...);
	unk_t (*OnLeave)(...);
	unk_t (*unk_func)(...);
};
```

-------------------------------------------------------------------------------

## Scene structures and state

```c
struct scene_state
{
	u8 current_major;
	u8 pending_major;
	u8 previous_major;
	u8 current_minor;

	u8 previous_minor;
	u8 pending_minor;
	u32 unk_06;
	u16 unk_0a;

	u8 pending;
	u8 pad[3];

	unk_t (*MajorSceneExitCallback)(...);
};
```

Some "scene controller state" of `struct scene_state` lives at `0x80479d30`.

-------------------------------------------------------------------------------

## Camera Functions

```c
struct camera_ft
{
	u32 unk;
	unk_t (*unk_func)(...);
	unk_t (*think)(...);
};
```

There's some unknown table of these 9 `camera_ft` structures at `0x803da6b4`.
They seem to hold camera-related functions.

Additionally, there's also a table of camera mode functions at `0x803bcb18`:

| Virtual Address | Camera Mode Function |
| --------------- | -------------------- |
| 0x8002b3d4      | CameraType_Normal |
| 0x8002cddc      | CameraType_Pause |
| 0x8002d318      | Unknown? |
| 0x8002d85c      | Unknown? |
| 0x8002ddc4      | CameraType_FixedCamera |
| 0x8002c908      | CameraMode_CameraThink |
| 0x8002e490      | Unknown? |


-------------------------------------------------------------------------------

## Menu Functions

```c
struct menu_ft
{
	void *unk_float_ptr;
	f32 unk_float;
	void *text_id_ptr;
	s8 num_options;
	u8 padding[3];
	unk_t (*think)(...);
};
```

An array of 34 `menu_ft` structures representing menu functions starts at `0x803eb6b0`.

-------------------------------------------------------------------------------

## Subaction Events

A table at `0x803c06e8` is filled with 98 function pointers to subaction event functions.

-------------------------------------------------------------------------------

## Audio/Sound

Some unknown function table with 10 entries at `0x803bca24`.
These are most likely related to audio/SFX.

-------------------------------------------------------------------------------

## Event Match Functions

```c
struct eventmatch_ft
{
	unk_t (*unk_func)(...);
	unk_t (*think)(...);
};
```

Some unknown table of 51 pointer entries to some `struct eventmatch_ft` starts at `0x803df94c`.
The actual structures are stored contiguously in an array of `struct eventmatch_ft` at `0x0804d4330`.
It's not clear how the table and pointer table are indexed.

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


```c
struct persistent_heap_obj
{
	u8 preload_status;
	u8 heap_id;
	u8 unk_02;
	u8 unk_03;
	u16 unk_04;
	u16 file_entrynum;
	u16 unk_08;
	u16 unk_0a;
	u32 file_len;
	void *persistent_heap_allocation_ptr;
	void *file_data_ptr;
	u32 persistent_file_id;
};
```

Some array of `struct persistent_heap_obj` (80 entries) lives at `0x80432124`.
