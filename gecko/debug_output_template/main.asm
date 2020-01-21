# main.asm
# 
# Write this on 0x801a4d98, inside `EngineUpdate()` - this will clobber a 
# `bl USBScreenshot_InitMCC`, which is effectively useless to everyone, unless 
# someone is actually using USB2EXI. Runs every iteration of the engine loop.

.include "../macro.asm"

# __start()
# Save some context to avoid clobbering the function we hooked.
# If varAllocated is zero, this is the first time we've entered this code,
# indicating that we need to fall-through in order to allocate memory.
__start:
	backup
	load_rt r4, f1Backup
	stfs f1, 0(r4)
	load_rt r4, f2Backup
	stfs f2, 0(r4)

	# If we've already allocated memory, skip to check if we can draw
	load_rt r4, varAllocated
	lwz r3, 0x0(r4)
	cmpwi r3, 0
	bne checkDrawing


# __allocateMemory()
# Allocate various objects that we need to continously draw on the screen.
#
# String buffer must be at least `TextData->max_rows * TextData->max_width * 2`
# (I think - according to `DevelopMode_Text_Erase()`?).
#
# The function for creating a TextData object looks something like this:
# void* TextData_Create(r3=some_id?, r4=x_off, r5=y_off, r6=max_width, 
#			r7=max_row, r8=str_ptr);
#
# Text object attributes (position/size/color) are also initialized here.
# I think you can change them on the fly after-the-fact?
__allocateMemory:

	# Allocate some memory for the string to display and save the pointer
	li r3, 0x500
	branchl r11, _HSD_MemAlloc
	load_rt r4, stringPtr
	stw r3, 0x0(r4)

	# Instantiate a new TextData object, then save the pointer to it
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

	# Enable the GXLink-scheduled function to display our text object (?)
	mr r4, r3
	branchl r11, TextData_Init

	# Unhide the object
	load_rt r4, textObjPtr
	lwz r3, 0(r4)
	branchl r11, TextData_Unhide

	# Set background color
	load_rt r4, textObjPtr
	lwz r3, 0(r4)
	load_rt r4, backgroundColor
	branchl r11, TextData_SetBackgroundColor

	# Set size
	load_rt r4, textObjPtr
	lwz r3, 0(r4)
	load_rt r4, textWidth
	lfs f1, 0(r4)
	load_rt r4, textHeight
	lfs f2, 0(r4)
	branchl r11, TextData_SetWidthHeight

	# Set varAllocated to non-zero and exit.
	# 
	li r3, 1
	load_rt r4, varAllocated
	stw r3, 0x0(r4)
	b __exit


# checkDrawing()
# Check the global text data pointer to see if drawing is disabled. 
# If it's disabled (i.e. after some scene transition), just re-enable it by
# re-writing our object's pointer back to the global pointer.
checkDrawing:

	# If this pointer is non-null, we can continue updating our objects
	load r3, GLOBAL_TEXTDATA_PTR
	lwz r3, 0(r3)
	cmpwi r3, 0
	bne __drawText

	# Otherwise, re-initialize our object and branch to the exit
	load_rt r4, textObjPtr
	lwz r4, 0(r4)
	branchl r11, TextData_Init
	b __exit


# __drawtext()
# Update our text object with data from this frame.
__drawText:

	# Clear out the current string data
	load_rt r4, textObjPtr
	lwz r3, 0(r4)
	branchl r11, DevelopMode_Text_Erase

	# Reset the cursor position
	load_rt r4, textObjPtr
	lwz r3, 0(r4)
	li r4, 0
	li r5, 0
	branchl r11, DevelopMode_Text_ResetCursor


# __prepareData()
# Gather 

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

	# Update text (note the creqv is necessary to render floating-point)
	load_rt r4, textObjPtr
	lwz r3, 0(r4)
	load_rt r4, fmtstring1
	creqv 4*cr1+eq,4*cr1+eq,4*cr1+eq
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

	load_rt r4, currentFrame
	lwz r3, 0(r4)
	cmpwi r3, 2

	addi r3, r3, 1
	stw r3, 0(r4)

	bne __exit

	# Load x and y video beam pos and update Text
	load_rt r4, textObjPtr
	lwz r3, 0(r4)
	load_rt r4, fmtstring3

	# Write the x/y video beam position
	load r7, 0xcc002000
	lhz r5, 0x2e(r7)
	lhz r6, 0x2c(r7)
	branchl r11, DevelopMode_Text_Display

	load_rt r4, currentFrame
	li r3, 0
	stw r3, 0(r4)

	b __exit

# This is a trick to embed a tiny data segment into our code.
# Branching with the link register to these symbols allows us to 
currentFrame:
	blrl
	.word 0x00000000
	.align 4
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
	.long 0x010101ff
	.align 4
textWidth:
	blrl
	.long 0x41800000
	.align 4
textHeight:
	blrl
	.long 0x41a00000
	.align 4
f1Backup:
	blrl
	.quad 0x00000000
	.align 4
f2Backup:
	blrl
	.quad 0x00000000
	.align 4
fmtstring1:
	blrl
	.string "X: (%08x) %f\n"
	.align 4
fmtstring2:
	blrl
	.string "Y: (%08x) %f\n"
	.align 4
fmtstring3:
	blrl
	.string "xpos=%04x, ypos=%04x\n"
	.align 4


# Re-enable develop mode text drawing, then fall-though to the end
#__enableDrawing:
#	stw r4, 0x0(r3)


# __exit()
# Restore context and exit this hook
__exit:
	load_rt r4, f1Backup
	lfs f1, 0(r4)
	load_rt r4, f2Backup
	lfs f2, 0(r4)
	restore
