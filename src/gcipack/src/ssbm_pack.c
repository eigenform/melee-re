#include "ssbm_pack.h"

/*  [De]obfuscation routines seem to depend on this array of 32-bit numbers.
 *  This array always seems to be totally static during runtime in memory.
 *  An emulator doesn't catch any writes on this region during startup, and
 *  it doesn't seem like we ever write back into to this table.
 *
 *  This is the table used by NTSC v1.02 code. Be aware that this table may
 *  be different in other versions of the game. I haven't verified whether
 *  or not this is the case.
 */

static uint32_t unk_arr[] = {
	0x00000026,
	0x000000FF,
	0x000000E8,
	0x000000EF,
	0x00000042,
	0x000000D6,
	0x00000001,
	0x00000054,
	0x00000014,
	0x000000A3,
	0x00000080,
	0x000000FD,
	0x0000006E,
};


/* These functions should approximate the behaviour of the `rlwinm` and `rlwimi`
 * instructions. There is probably a more beautiful solution to this problem.
 */

uint32_t mask(uint32_t mb, uint32_t me)
{
	uint32_t x = 0xffffffff >> mb;
	uint32_t y = 0xffffffff << (31 - me);

	if (mb <= me)
		return x & y;
        else
		return x | y;
}

uint32_t rotl(uint32_t rx, uint32_t sh)
{
	return ( rx << sh ) | (rx >> ((32 - sh) & 31));
}

uint32_t rlwinm(uint32_t rs, uint32_t sh, uint32_t mb, uint32_t me)
{
	return rotl(rs, sh) & mask(mb, me);
}

uint32_t rlwimi(uint32_t ra, uint32_t rs, uint32_t sh, uint32_t mb, uint32_t me)
{
	uint32_t m = mask(mb, me);
	uint32_t r = rotl(rs, sh);

	return (r & m) | (ra & ~m);
}

/* In both cases, the [de]obfuscation takes some previous byte and a current
 * byte. Note that, for multiplication, you need to do it in 64-bits and move
 * the high-order bits into the register.
 *
 * For reference (and assuming NTSC v1.02):
 *
 *	- Bytes are obfuscated by the function starting at 0x803b2e04
 *	- Bytes are deobfuscated by the function starting at 0x803b302c
 *
 * These were written by disassembling an NTSC v1.02 copy of the game.
 * It's not clear if other versions are implemented exactly the same way.
 */

uint8_t decompress_byte(uint8_t prev_byte, uint8_t current_byte)
{
	uint32_t r0, r3, r4, r5, r6, r7;

	//printf("decompress_byte(r3=%08x, r4=%08x)\n", prev_byte, current_byte);

	// Careful with the multiplication here
	if (prev_byte == 0x00) {
		r5 = 0x92492493;
		r5 = (int32_t)( ((int64_t)r5*(int64_t)prev_byte) >> 32 );
	}
	else {
		r5 = ~0x92492493;
		r5 = (int32_t)( ~((int64_t)r5*(int64_t)prev_byte) >> 32 );
	}

	r5 = r5 + prev_byte;
	r5 = r5 >> 2;
	r6 = rlwinm(r5, 1, 31, 31);
	r5 = r5 + r6;
	r5 = r5 * 7;
	r7 = prev_byte - r5;
	//printf("(switch r7=%08x)\n", r7);

	if (r7 <= 6) {
		switch(r7) {
		case 0:
			r5 = rlwinm(current_byte, 1, 29, 29);
			r5 = rlwimi(r5, current_byte, 0, 31, 31);
			r5 = rlwimi(r5, current_byte, 2, 27, 27);
			r5 = rlwimi(r5, current_byte, 3, 25, 25);
			r5 = rlwimi(r5, current_byte, 29, 30, 30);
			r5 = rlwimi(r5, current_byte, 30, 28, 28);
			r5 = rlwimi(r5, current_byte, 31, 26, 26);
			r5 = rlwimi(r5, current_byte, 0, 24, 24);
			r4 = rlwinm(r5, 0, 24, 31);
			break;
		case 1:
			r5 = rlwinm(current_byte, 6, 24, 24);
			r5 = rlwimi(r5, current_byte, 1, 30, 30);
			r5 = rlwimi(r5, current_byte, 0, 29, 29);
			r5 = rlwimi(r5, current_byte, 29, 31, 31);
			r5 = rlwimi(r5, current_byte, 1, 26, 26);
			r5 = rlwimi(r5, current_byte, 31, 27, 27);
			r5 = rlwimi(r5, current_byte, 29, 28, 28);
			r5 = rlwimi(r5, current_byte, 31, 25, 25);
			r4 = rlwinm(r5, 0, 24, 31);
			break;
		case 2:
			r5 = rlwinm(current_byte, 2, 28, 28);
			r5 = rlwimi(r5, current_byte, 2, 29, 29);
			r5 = rlwimi(r5, current_byte, 4, 25, 25);
			r5 = rlwimi(r5, current_byte, 1, 27, 27);
			r5 = rlwimi(r5, current_byte, 3, 24, 24);
			r5 = rlwimi(r5, current_byte, 28, 30, 30);
			r5 = rlwimi(r5, current_byte, 26, 31, 31);
			r5 = rlwimi(r5, current_byte, 30, 26, 26);
			r4 = rlwinm(r5, 0, 24, 31);
			break;
		case 3:
			r5 = rlwinm(current_byte, 31, 31, 31);
			r5 = rlwimi(r5, current_byte, 4, 27, 27);
			r5 = rlwimi(r5, current_byte, 3, 26, 26);
			r5 = rlwimi(r5, current_byte, 30, 30, 30);
			r5 = rlwimi(r5, current_byte, 31, 28, 28);
			r5 = rlwimi(r5, current_byte, 1, 25, 25);
			r5 = rlwimi(r5, current_byte, 1, 24, 24);
			r5 = rlwimi(r5, current_byte, 27, 29, 29);
			r4 = rlwinm(r5, 0, 24, 31);
			break;
		case 4:
			r5 = rlwinm(current_byte, 4, 26, 26);
			r5 = rlwimi(r5, current_byte, 3, 28, 28);
			r5 = rlwimi(r5, current_byte, 31, 30, 30);
			r5 = rlwimi(r5, current_byte, 4, 24, 24);
			r5 = rlwimi(r5, current_byte, 2, 25, 25);
			r5 = rlwimi(r5, current_byte, 29, 29, 29);
			r5 = rlwimi(r5, current_byte, 30, 27, 27);
			r5 = rlwimi(r5, current_byte, 25, 31, 31);
			r4 = rlwinm(r5, 0, 24, 31);
			break;
		case 5:
			r5 = rlwinm(current_byte, 5, 25, 25);
			r5 = rlwimi(r5, current_byte, 5, 26, 26);
			r5 = rlwimi(r5, current_byte, 5, 24, 24);
			r5 = rlwimi(r5, current_byte, 0, 28, 28);
			r5 = rlwimi(r5, current_byte, 30, 29, 29);
			r5 = rlwimi(r5, current_byte, 27, 31, 31);
			r5 = rlwimi(r5, current_byte, 27, 30, 30);
			r5 = rlwimi(r5, current_byte, 29, 27, 27);
			r4 = rlwinm(r5, 0, 24, 31);
			break;
		case 6:
			r5 = rlwinm(current_byte, 0, 30, 30);
			r5 = rlwimi(r5, current_byte, 6, 25, 25);
			r5 = rlwimi(r5, current_byte, 30, 31, 31);
			r5 = rlwimi(r5, current_byte, 2, 26, 26);
			r5 = rlwimi(r5, current_byte, 0, 27, 27);
			r5 = rlwimi(r5, current_byte, 2, 24, 24);
			r5 = rlwimi(r5, current_byte, 28, 29, 29);
			r5 = rlwimi(r5, current_byte, 28, 28, 28);
			r4 = rlwinm(r5, 0, 24, 31);
			break;
		}

		// also suspect the signedness of *this* is broken too
		r5 = 0x4ec4ec4f;
		r5 = (int32_t)( ((int64_t)r5*(int64_t)prev_byte) >> 32 );
		r5 = r5 >> 2;
		r6 = rlwinm(r5, 1, 31, 31);
		r5 = r5 + r6;
		r5 = r5 * 13;
		r0 = prev_byte - r5;
		r6 = rlwinm(r0, 2, 0, 29);
		r0 = unk_arr[r6/4]; //load a uint32 from unk_array[r6]
		//printf("(from unk_arr) r0=%08x\n", r0);
		r4 = r4 ^ r0;
		r4 = r4 ^ prev_byte;
		r3 = r4 + 0;

		//printf("(result) r3=%08x\n", r3);
		return r3;
	}
}


uint8_t compress_byte(uint8_t prev_byte, uint8_t current_byte)
{
	uint32_t r0;
	uint32_t r3;
	uint32_t r5;

	//printf("compress_byte(0x%02x, 0x%02x)\n", prev_byte, current_byte);

	r5 = ((int64_t)0x4ec4ec4f * (int64_t)prev_byte) >> 32;
	//printf("r5 = 0x%08x\n", r5);

	if (prev_byte == 0x00) {
		r0 = 0x92492493;
		r0 = (int32_t)( ((int64_t)r0*(int64_t)prev_byte) >> 32 );
	}
	else {
		r0 = ~0x92492493;
		r0 = (int32_t)( ~((int64_t)r0*(int64_t)prev_byte) >> 32 );
	}
	//printf("r0 = 0x%08x\n", r0);

	r3 = r5 >> 2;
	r5 = rlwinm(r3, 1, 31, 31);
	r0 = r0 + prev_byte;
	r3 = r3 + r5;
	r0 = r0 >> 2;
	r5 = r3 * 13;
	r3 = rlwinm(r0, 1, 31, 31);
	r0 = r0 + r3;
	r0 = r0 * 7;
	r5 = prev_byte - r5;
	r0 = prev_byte - r0;
	r5 = rlwinm(r5, 2, 0, 29);

	r5 = unk_arr[r5/4]; //load a uint32 from unk_array[r5]
	//printf("got r5=0x%08x\n from array", r5);

	r3 = prev_byte ^ current_byte;
	r3 = r3 ^ r5;

	// I don't think we ever reach a case where r0 > 6
	if (r0 <= 6){

		r0 = rlwinm(r0, 2, 0, 29);
		switch(r0) {
		case 0x0:
			r0 = rlwinm(r3, 3, 27, 27);
			r0 = rlwimi(r0, r3, 0, 31, 31);
			r0 = rlwimi(r0, r3, 31, 30, 30);
			r0 = rlwimi(r0, r3, 2, 26, 26);
			r0 = rlwimi(r0, r3, 30, 29, 29);
			r0 = rlwimi(r0, r3, 1, 25, 25);
			r0 = rlwimi(r0, r3, 29, 28, 28);
			r0 = rlwimi(r0, r3, 0, 24, 24);
			r3 = rlwinm(r0, 0, 24, 31);
			return r3;
			break;
		case 0x4:
			r0 = rlwinm(r3, 31, 31, 31);
			r0 = rlwimi(r0, r3, 3, 28, 28);
			r0 = rlwimi(r0, r3, 0, 29, 29);
			r0 = rlwimi(r0, r3, 3, 25, 25);
			r0 = rlwimi(r0, r3, 1, 26, 26);
			r0 = rlwimi(r0, r3, 31, 27, 27);
			r0 = rlwimi(r0, r3, 1, 24, 24);
			r0 = rlwimi(r0, r3, 26, 30, 30);
			r3 = rlwinm(r0, 0, 24, 31);
			return r3;
			break;
		case 0x8:
			r0 = rlwinm(r3, 4, 26, 26);
			r0 = rlwimi(r0, r3, 6, 25, 25);
			r0 = rlwimi(r0, r3, 30, 31, 31);
			r0 = rlwimi(r0, r3, 30, 30, 30);
			r0 = rlwimi(r0, r3, 31, 28, 28);
			r0 = rlwimi(r0, r3, 2, 24, 24);
			r0 = rlwimi(r0, r3, 28, 29, 29);
			r0 = rlwimi(r0, r3, 29, 27, 27);
			r3 = rlwinm(r0, 0, 24, 31);
			return r3;
			break;
		case 0xc:
			r0 = rlwinm(r3, 2, 28, 28);
			r0 = rlwimi(r0, r3, 1, 30, 30);
			r0 = rlwimi(r0, r3, 5, 24, 24);
			r0 = rlwimi(r0, r3, 1, 27, 27);
			r0 = rlwimi(r0, r3, 28, 31, 31);
			r0 = rlwimi(r0, r3, 29, 29, 29);
			r0 = rlwimi(r0, r3, 31, 26, 26);
			r0 = rlwimi(r0, r3, 31, 25, 25);
			r3 = rlwinm(r0, 0, 24, 31);
			return r3;
			break;
		case 0x10:
			r0 = rlwinm(r3, 1, 29, 29);
			r0 = rlwimi(r0, r3, 7, 24, 24);
			r0 = rlwimi(r0, r3, 3, 26, 26);
			r0 = rlwimi(r0, r3, 29, 31, 31);
			r0 = rlwimi(r0, r3, 2, 25, 25);
			r0 = rlwimi(r0, r3, 28, 30, 30);
			r0 = rlwimi(r0, r3, 30, 27, 27);
			r0 = rlwimi(r0, r3, 28, 28, 28);
			r3 = rlwinm(r0, 0, 24, 31);
			return r3;
			break;
		case 0x14:
			r0 = rlwinm(r3, 5, 25, 25);
			r0 = rlwimi(r0, r3, 5, 26, 26);
			r0 = rlwimi(r0, r3, 2, 27, 27);
			r0 = rlwimi(r0, r3, 0, 28, 28);
			r0 = rlwimi(r0, r3, 3, 24, 24);
			r0 = rlwimi(r0, r3, 27, 31, 31);
			r0 = rlwimi(r0, r3, 27, 30, 30);
			r0 = rlwimi(r0, r3, 27, 29, 29);
			r3 = rlwinm(r0, 0, 24, 31);
			return r3;
			break;
		case 0x18:
			r0 = rlwinm(r3, 0, 30, 30);
			r0 = rlwimi(r0, r3, 2, 29, 29);
			r0 = rlwimi(r0, r3, 4, 25, 25);
			r0 = rlwimi(r0, r3, 4, 24, 24);
			r0 = rlwimi(r0, r3, 0, 27, 27);
			r0 = rlwimi(r0, r3, 30, 28, 28);
			r0 = rlwimi(r0, r3, 26, 31, 31);
			r0 = rlwimi(r0, r3, 30, 26, 26);
			r3 = rlwinm(r0, 0, 24, 31);
			return r3;
			break;
		}
	}
}

