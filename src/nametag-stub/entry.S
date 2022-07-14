// Load some literal 'val' into the register 'dest'
.macro literal	dest:req val:req
	lis	\dest, \val@h
	ori	\dest, \dest, \val@l
.endm

_start:
	literal	r12, 0x81700200
	stw	r0, 0(r12)
	stw	r1, 4(r12)
	stw	r2, 8(r12)
	stw	r3, 12(r12)
	stw	r4, 16(r12)
	stw	r5, 20(r12)
	stw	r6, 24(r12)
	stw	r7, 28(r12)
	stw	r8, 32(r12)
	stw	r9, 36(r12)
	stw	r10, 40(r12)
	stw	r11, 44(r12)
	stw	r13, 52(r12)
	stw	r14, 56(r12)
	stw	r15, 60(r12)
	stw	r16, 64(r12)
	stw	r17, 68(r12)
	stw	r18, 72(r12)
	stw	r19, 76(r12)
	stw	r20, 80(r12)
	stw	r21, 84(r12)
	stw	r22, 88(r12)
	stw	r23, 92(r12)
	stw	r24, 96(r12)
	stw	r25, 100(r12)
	stw	r26, 104(r12)
	stw	r27, 108(r12)
	stw	r28, 112(r12)
	stw	r29, 116(r12)
	stw	r30, 120(r12)
	stw	r31, 124(r12)

_do_main:
	literal r1, 0x81700000
	bl	loader_main

_restore_regs:
	literal	r12, 0x81700200
	lwz	r0, 0(r12)
	lwz	r1, 4(r12)
	lwz	r2, 8(r12)
	lwz	r3, 12(r12)
	lwz	r4, 16(r12)
	lwz	r5, 20(r12)
	lwz	r6, 24(r12)
	lwz	r7, 28(r12)
	lwz	r8, 32(r12)
	lwz	r9, 36(r12)
	lwz	r10, 40(r12)
	lwz	r11, 44(r12)
	lwz	r13, 52(r12)
	lwz	r14, 56(r12)
	lwz	r15, 60(r12)
	lwz	r16, 64(r12)
	lwz	r17, 68(r12)
	lwz	r18, 72(r12)
	lwz	r19, 76(r12)
	lwz	r20, 80(r12)
	lwz	r21, 84(r12)
	lwz	r22, 88(r12)
	lwz	r23, 92(r12)
	lwz	r24, 96(r12)
	lwz	r25, 100(r12)
	lwz	r26, 104(r12)
	lwz	r27, 108(r12)
	lwz	r28, 112(r12)
	lwz	r29, 116(r12)
	lwz	r30, 120(r12)
	lwz	r31, 124(r12)
_exit:
	lis	r12, saved_lr@h
	ori	r12, r12, saved_lr@l
	lwz	r12, 0(r12)
	mtlr	r12
	blr

/* The "normal LR" typically appears to be 0x80239e44.
 * This should let us return cleanly into the nametag menu.
 */

.global saved_lr
saved_lr: .long 0x80239e9c
