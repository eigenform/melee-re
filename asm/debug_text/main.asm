# Write this on 0x801a4d98, inside `EngineUpdate()` - this will clobber a 
# `bl USBScreenshot_InitMCC`, which is effectively useless to everyone, unless 
# someone is actually using USB2EXI. Runs every iteration of the engine loop.

.include "../macro.asm"

__start:
	backup
	load_rt r4, f1Backup
	stfs f1, 0(r4)
	load_rt r4, f2Backup
	stfs f2, 0(r4)

	# If varAllocated is zero, we haven't allocated objects yet
	load_rt r4, varAllocated
	lwz r3, 0x0(r4)
	cmpwi r3, 0

	# If we've allocated objects, check to see if we can draw 
	bne checkDrawing

__allocateMemory:
	# This is literally just the allocation from Develop Mode bonuses,
	# and this corresponds to the arguments to drawing functions.
	#branchl r11, 0x80228cf4

	# Allocate some memory for the string to display and save the pointer.
	# Must be at least `TextData->max_rows * TextData->max_width * 2`
	# (this how `DevelopMode_Text_Erase()` calculates string size?)
	li r3, 0x500
	branchl r11, _HSD_MemAlloc
	load_rt r4, stringPtr
	stw r3, 0x0(r4)

	# Instantiate a new TextData object, then save the pointer to it
	# r3=id?, r4=x_off, r5=y_off, r6=max_width, r7=max_row, r8=string ptr
	li r3, 1	
	li r4, 0x10
	li r5, 0x10
	li r6, 32
	li r7, 5
	load_rt r8, stringPtr
	lwz r8, 0(r8)
	branchl r11, TextData_Create
	load_rt r4, textObjPtr
	stw r3, 0(r4)

	# Pass textObjPtr to this function to enable it?
	mr r4, r3
	branchl r11, TextData_Init

	# Set background color
	load_rt r4, textObjPtr
	lwz r3, 0(r4)
	load_rt r4, backgroundColor
	branchl r11, TextData_SetBackgroundColor

	# Unhide the object
	load_rt r4, textObjPtr
	lwz r3, 0(r4)
	branchl r11, TextData_Unhide

	# Set varAllocated to non-zero and exit
	li r3, 1
	load_rt r4, varAllocated
	stw r3, 0x0(r4)
	b __exit

# First, we need to check to see if drawing has been disabled. If disabled 
# (i.e. after a scene transition), just re-enable it by writing the pointer.
checkDrawing:
	# r3 typically holds a pointer main develop text object
	#load r3, 0x804d6e18

	# r4 is typically the address of the main object
	#load r4, 0x804a1fd8

	# If the pointer is zero, it means drawing is disabled, so re-enable 
	# it and just exit this function for now
	#lwz r5, 0x0(r3)
	#cmpwi r5, 0
	#beq __enableDrawing

	# If this pointer is non-null, it's probably the pointer to our
	# object, so we can continue updating our objects
	load r3, 0x804d6e18
	lwz r3, 0(r3)
	cmpwi r3, 0
	bne __drawText

	# Otherwise, if the pointer was null, re-initialize our object
	# and exit
	load_rt r4, textObjPtr
	lwz r4, 0(r4)
	branchl r11, TextData_Init
	b __exit


	
# If drawing is enabled, we're free to mutate our text objects
__drawText:
	load_rt r4, textObjPtr
	lwz r3, 0(r4)
	branchl r11, DevelopMode_Text_Erase

	load_rt r4, textObjPtr
	lwz r3, 0(r4)
	li r4, 0
	li r5, 0
	branchl r11, DevelopMode_Text_ResetCursor

	load r3, 0x81118dec # p1 x
	lfs f1, 0(r3)

	load_rt r4, textObjPtr
	lwz r3, 0(r4)
	load_rt r4, fmtstring1
	creqv 4*cr1+eq,4*cr1+eq,4*cr1+eq
	branchl r11, DevelopMode_Text_Display

	load r4, 0x81118df0 # p1 y
	lfs f1, 0(r4)

	load_rt r4, textObjPtr
	lwz r3, 0(r4)
	load_rt r4, fmtstring2
	creqv 4*cr1+eq,4*cr1+eq,4*cr1+eq
	branchl r11, DevelopMode_Text_Display

	b __exit


# Local storage - stuff we allocate for our objects
varAllocated:
	blrl
	.word 0x00000000
	.align 4
textObjPtr:
	blrl
	.word 0x00000000
	.align 4
stringPtr:
	blrl
	.word 0x00000000
	.align 4
backgroundColor:
	blrl
	.word 0x00000000
	.align 4
f1Backup:
	blrl
	.quad 0x00000000
	.align 4
f2Backup:
	blrl
	.quad 0x00000000
	.align 4


# Local storage - format strings for rendering text
fmtstring1:
	blrl
	.string "x %f\n"
	.align 4
fmtstring2:
	blrl
	.string "y %f\n"
	.align 4

# Re-enable develop mode text drawing, then fall-though to the end
#__enableDrawing:
#	stw r4, 0x0(r3)

__exit:
	load_rt r4, f1Backup
	lfs f1, 0(r4)
	load_rt r4, f2Backup
	lfs f2, 0(r4)


	restore
