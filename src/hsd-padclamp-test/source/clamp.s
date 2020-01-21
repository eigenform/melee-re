#include "macro.s"

.global clamptest
clamptest:
	mflr r12
	# Do the thing
	bl __melee_padclamp
	mtlr r12
	blr

	# Render a float
	#bl __convert_to_float


# Converts some s8 (in r3) into a float
# __convert_to_float(s8 input, double *output)
.global __convert_to_float
__convert_to_float:
	li r0, 0x50
	load r6, __tmp_table
	lis r5, 0x4330
	lfd f30, 0x10(r6)

	extsb r3, r3
	extsb r0, r0
	xoris r3, r3, 0x8000
	xoris r0, r0, 0x8000
	stw r3, 0x04(r6)
	stw r0, 0x0c(r6)
	stw r5, 0x00(r6)
	stw r5, 0x08(r6)

	lfd f1, 0x00(r6)
	lfd f0, 0x08(r6)

	fsubs f1, f1, f30
	fsubs f0, f0, f30
	fdivs f0, f1, f0

	# result in f0
	# ...
	stfd f0, 0(r4)
	blr
	

# Literally just HSD_PadClamp, but with constants and less args
# void __melee_padclamp(s8 *xval, s8 *yval);
__melee_padclamp:
	stwu      r1,-0x70(r1)

	# Fix some of the arguments
	li	  r5, 0x01
	li	  r6, 0x00
	li	  r7, 0x50
	load	  r11, __table

	lis       r8,0x4330
	lbz       r0,0x0(r3)
	lbz       r10,0x0(r4)
	extsb     r0,r0
	lfd       f5,0x10(r11)
	#lfd       f5,-0x1410(r2) # 0x4330000080000000
	xoris     r9,r0,0x8000
	lfs       f0,0x30(r11)
	#lfs       f0,-0x1430(r2) # 0x0000000000000000?
	extsb     r0,r10
	stw       r9,0x6c(r1)
	xoris     r0,r0,0x8000
	stw       r9,0x64(r1)
	stw       r0,0x5c(r1)
	stw       r0,0x54(r1)
	stw       r8,0x68(r1)
	stw       r8,0x60(r1)
	lfd       f2,0x68(r1)
	lfd       f1,0x60(r1)
	stw       r8,0x58(r1)
	fsubs     f4,f2,f5
	fsubs     f3,f1,f5
	stw       r8,0x50(r1)
	lfd       f2,0x58(r1)
	lfd       f1,0x50(r1)
	fmuls     f3,f4,f3
	fsubs     f2,f2,f5
	fsubs     f1,f1,f5
	fmuls     f1,f2,f1
	fadds     f4,f3,f1
	fcmpo     cr0,f4,f0
	ble       LAB_80376f58
	frsqrte   f1,f4
	lfd       f3,0x28(r11)
	lfd       f2,0x20(r11)
	#lfd       f3,-0x1428(r2) # 0x3fe0000000000000
	#lfd       f2,-0x1420(r2) # 0x4008000000000000
	fmul      f0,f1,f1
	fmul      f1,f3,f1
	fnmsub    f0,f4,f0,f2
	fmul      f1,f1,f0
	fmul      f0,f1,f1
	fmul      f1,f3,f1
	fnmsub    f0,f4,f0,f2
	fmul      f1,f1,f0
	fmul      f0,f1,f1
	fmul      f1,f3,f1
	fnmsub    f0,f4,f0,f2
	fmul      f0,f1,f0
	fmul      f0,f4,f0
	frsp      f0,f0
	stfs      f0,0x18(r1)
	lfs       f4,0x18(r1)

LAB_80376f58:
	extsb     r0,r6
	lfd       f5,0x10(r11)
	#lfd       f5,-0x1410(r2) # 0x4330000000000000
	xoris     r0,r0,0x8000
	stw       r0,0x54(r1)
	lis       r8,0x4330
	stw       r8,0x50(r1)
	lfd       f0,0x50(r1)
	fsubs     f0,f0,f5
	fcmpo     cr0,f4,f0
	bge       LAB_80376f90
	li        r0,0x0
	stb       r0,0x0(r4)
	stb       r0,0x0(r3)
	b         LAB_803771cc

LAB_80376f90:
	extsb     r0,r7
	xoris     r7,r0,0x8000
	stw       r7,0x54(r1)
	stw       r8,0x50(r1)
	lfd       f0,0x50(r1)
	fsubs     f0,f0,f5
	fcmpo     cr0,f4,f0
	ble       LAB_803770f4
	lbz       r0,0x0(r3)
	stw       r7,0x5c(r1)
	extsb     r0,r0
	xoris     r0,r0,0x8000
	stw       r8,0x58(r1)
	stw       r0,0x54(r1)
	lfd       f0,0x58(r1)
	stw       r8,0x50(r1)
	fsubs     f0,f0,f5
	lfd       f1,0x50(r1)
	stw       r7,0x4c(r1)
	fsubs     f1,f1,f5
	stw       r8,0x48(r1)
	fmuls     f1,f1,f0
	lfd       f0,0x48(r1)
	fsubs     f0,f0,f5
	fdivs     f1,f1,f4
	fctiwz    f1,f1
	stfd      f1,0x60(r1)
	lwz       r0,0x64(r1)
	stb       r0,0x0(r3)
	lbz       r0,0x0(r4)
	extsb     r0,r0
	xoris     r0,r0,0x8000
	stw       r0,0x6c(r1)
	stw       r8,0x68(r1)
	lfd       f1,0x68(r1)
	fsubs     f1,f1,f5
	fmuls     f0,f1,f0
	fdivs     f0,f0,f4
	fctiwz    f0,f0
	stfd      f0,0x40(r1)
	lwz       r0,0x44(r1)
	stb       r0,0x0(r4)
	lbz       r0,0x0(r3)
	lbz       r9,0x0(r4)
	extsb     r0,r0
	lfs       f0,-0x1430(r2)
	xoris     r7,r0,0x8000
	extsb     r0,r9
	stw       r7,0x3c(r1)
	xoris     r0,r0,0x8000
	stw       r7,0x34(r1)
	stw       r0,0x2c(r1)
	stw       r0,0x24(r1)
	stw       r8,0x38(r1)
	stw       r8,0x30(r1)
	lfd       f2,0x38(r1)
	lfd       f1,0x30(r1)
	stw       r8,0x28(r1)
	fsubs     f4,f2,f5
	fsubs     f3,f1,f5
	stw       r8,0x20(r1)
	lfd       f2,0x28(r1)
	lfd       f1,0x20(r1)
	fmuls     f3,f4,f3
	fsubs     f2,f2,f5
	fsubs     f1,f1,f5
	fmuls     f1,f2,f1
	fadds     f4,f3,f1
	fcmpo     cr0,f4,f0
	ble       LAB_803770f4
	frsqrte   f1,f4
	lfd       f3,0x28(r11)
	lfd       f2,0x20(r11)
	#lfd       f3,-0x1428(r2) # 0x3fe0000000000000
	#lfd       f2,-0x1420(r2) # 0x4008000000000000
	fmul      f0,f1,f1
	fmul      f1,f3,f1
	fnmsub    f0,f4,f0,f2
	fmul      f1,f1,f0
	fmul      f0,f1,f1
	fmul      f1,f3,f1
	fnmsub    f0,f4,f0,f2
	fmul      f1,f1,f0
	fmul      f0,f1,f1
	fmul      f1,f3,f1
	fnmsub    f0,f4,f0,f2
	fmul      f0,f1,f0
	fmul      f0,f4,f0
	frsp      f0,f0
	stfs      f0,0x14(r1)
	lfs       f4,0x14(r1)

LAB_803770f4:
	rlwinm    r0,r5,0x0,0x18,0x1f
	cmplwi    r0,0x1
	bne       LAB_803771cc
	lfs       f0,-0x1418(r2) # 0x2edbe6ff
	fcmpo     cr0,f4,f0
	ble       LAB_803771cc
	lbz       r5,0x0(r3)
	extsb     r0,r6
	xoris     r0,r0,0x8000
	lfd       f3,0x10(r11)
	#lfd       f3,-0x1410(r2) # 0x4330000080000000
	extsb     r5,r5
	xoris     r6,r5,0x8000
	stw       r0,0x34(r1)
	lis       r5,0x4330
	stw       r6,0x2c(r1)
	stw       r5,0x28(r1)
	stw       r5,0x30(r1)
	lfd       f1,0x28(r1)
	lfd       f0,0x30(r1)
	fsubs     f1,f1,f3
	stw       r6,0x24(r1)
	fsubs     f0,f0,f3
	stw       r5,0x20(r1)
	fmuls     f0,f1,f0
	lfd       f1,0x20(r1)
	stw       r0,0x54(r1)
	fsubs     f2,f1,f3
	fdivs     f1,f0,f4
	stw       r5,0x50(r1)
	lfd       f0,0x50(r1)
	fsubs     f1,f2,f1
	fsubs     f0,f0,f3
	fctiwz    f1,f1
	stfd      f1,0x38(r1)
	lwz       r0,0x3c(r1)
	stb       r0,0x0(r3)
	lbz       r0,0x0(r4)
	extsb     r0,r0
	xoris     r0,r0,0x8000
	stw       r0,0x4c(r1)
	stw       r5,0x48(r1)
	lfd       f1,0x48(r1)
	stw       r0,0x44(r1)
	fsubs     f1,f1,f3
	stw       r5,0x40(r1)
	fmuls     f0,f1,f0
	lfd       f1,0x40(r1)
	fsubs     f1,f1,f3
	fdivs     f0,f0,f4
	fsubs     f0,f1,f0
	fctiwz    f0,f0
	stfd      f0,0x58(r1)
	lwz       r0,0x5c(r1)
	stb       r0,0x0(r4)

LAB_803771cc:
	addi      r1,r1,0x70
	blr


# These are also some more constants? I think __1418 has those in the low bits
# and not in the high bits?

__table:
	.quad 0xffffffffffffffff
	.quad 0xffffffffffffffff
__1410:
	.quad 0x4330000080000000
__1418:
	.quad 0x2edbe6ff
__1420:
	.quad 0x4008000000000000
__1428:
	.quad 0x3fe0000000000000
__1430:
	.quad 0x0000000000000000
	.quad 0x0000000000000000
__1440:
	.quad 0xffffffffffffffff
	.quad 0xffffffffffffffff


# Takes some s8 in r3
__tmp_table:
	.quad 0x0000000000000000
	.quad 0x0000000000000000
	.quad 0x4330000080000000

