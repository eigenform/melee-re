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

	# Allocate some memory for the string to display and save the pointer.
	# Must be at least `TextData->max_rows * TextData->max_width * 2`
	# (this how `DevelopMode_Text_Erase()` calculates string size?)

	li r3, 0x500
	branchl r11, _HSD_MemAlloc
	load_rt r4, stringPtr
	stw r3, 0x0(r4)

	# Instantiate a new TextData object, then save the pointer to it.
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

	# This function enables the GXLink-scheduled function to display
	# our text object (I think ...)
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

	# If this pointer is non-null, it's probably the pointer to our
	# object, so we can continue updating our objects

	load r3, GLOBAL_TEXTDATA_PTR
	lwz r3, 0(r3)
	cmpwi r3, 0
	bne __drawText

	# Otherwise, if the pointer was null, re-initialize our object
	# and branch to the exit

	load_rt r4, textObjPtr
	lwz r4, 0(r4)
	branchl r11, TextData_Init
	b __exit

# If drawing is enabled, we're free to mutate our text objects
__drawText:

	# Clear out the string data
	load_rt r4, textObjPtr
	lwz r3, 0(r4)
	branchl r11, DevelopMode_Text_Erase

	# Reset the cursor position
	load_rt r4, textObjPtr
	lwz r3, 0(r4)
	li r4, 0
	li r5, 0
	branchl r11, DevelopMode_Text_ResetCursor


	# Resolve a pointer to the P1 cursor struct.
	# If the pointer is null, just do nothing until we're in the CSS.
	# Otherwise, load the floats and use them to render text.
	# The cursor structure members we care about are:
	#	0x0c - f32 x_pos
	#	0x10 - f32 y_pos

	load r3, GLOBAL_P1CURSOR_PTR
	lwz r3, 0(r3)
	cmpwi r3, 0
	beq __exit

	# Load cursor x position
	lfs f1, 0x0c(r3)
	lwz r5, 0x0c(r3)

	# Update text
	load_rt r4, textObjPtr
	lwz r3, 0(r4)
	load_rt r4, fmtstring1
	creqv 4*cr1+eq,4*cr1+eq,4*cr1+eq # necessary to render floating-point
	branchl r11, DevelopMode_Text_Display

	# Load cursor y position
	load r3, GLOBAL_P1CURSOR_PTR
	lwz r3, 0(r3)
	lfs f1, 0x10(r3)
	lwz r5, 0x10(r3)

	# Update text
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
	.string "X: (%08x) %f\n"
	.align 4
fmtstring2:
	blrl
	.string "Y: (%08x) %f\n"
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
