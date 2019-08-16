# Write this on 0x801a4d98, inside `EngineUpdate()`; this will clobber a 
# `bl USBScreenshot_InitMCC`, which is effectively useless to everyone, unless 
# someone is actually using USB2EXI. Runs every iteration of the engine loop.

.include "../macro.asm"

__start:
	backup

	# If varAllocated is zero, we haven't allocated objects yet
	bl varAllocated
	mflr r4
	lwz r3, 0x0(r4)
	cmpwi r3, 0

	# If we've allocated objects, check to see if we can draw 
	bne checkDrawing

	# If we haven't allocated objects, allocate them and exit.
	# This is literally just the allocation from Develop Mode bonuses,
	# and this corresponds to the arguments to drawing functions.
	branchl r11, 0x80228cf4

	# Set varAllocated to non-zero and exit
	li r3, 1
	stw r3, 0x0(r4)
	b __exit

# First, we need to check to see if drawing has been disabled. If disabled 
# (i.e. after a scene transition), just re-enable it by writing the pointer.
checkDrawing:

	# r3 typically holds a pointer main develop text object
	load r3, 0x804d6e18

	# r4 is typically the address of the main object
	load r4, 0x804a1fd8

	# If the pointer is zero, it means drawing is disabled, so re-enable 
	# it and just exit this function for now
	lwz r5, 0x0(r3)
	cmpwi r5, 0
	beq __enableDrawing
	
# If drawing is enabled, we can mutuate the develop text object/s.
__drawText:
	load r3, 0x804a1fd8
	load r4, 0x803f0000
	branchl r11, DevelopMode_Text_Erase

	load r3, 0x804a1fd8
	li r4, 0
	li r5, 0
	branchl r11, DevelopMode_Text_ResetCursor

	load r3, 0x804a1fd8
	bl string1Ptr
	mflr r4
	branchl r11, DevelopMode_Text_Display

	load r3, 0x804a1fd8
	bl string2Ptr
	mflr r4
	branchl r11, DevelopMode_Text_Display

	b __exit

# Local storage - keep track of when we've allocated text objects. God only 
# knows what happens if you branch into 0x80228cf4 somewhere else (this is
# specific to the Develop Mode Bonuses Text with 'B + DpadLeft' I think ...)
varAllocated:
	blrl
	.word 0x00000000
	.align 4

# Local storage for format strings
string1Ptr:
	blrl
	.string "Hello, world!\n"
	.align 4
string2Ptr:
	blrl
	.string "This is a test!\n"
	.align 4

# Re-enable develop mode text drawing, then fall-though to the end
__enableDrawing:
	stw r4, 0x0(r3)

__exit:
	restore
