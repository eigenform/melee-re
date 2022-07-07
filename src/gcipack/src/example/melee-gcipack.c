#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <inttypes.h>

#include "ssbm_pack.h"
#include "ssbm_format.h"
#include "util.h"

enum { UNPACK_MODE = 1, PACK_MODE = 2, CHECKSUM_MODE = 3, };
enum { READ_ONLY = 0, WRITE_BACK = 1, };

/* Print a 0x10-byte checksum to stdout */
void print_checksum(void *buf)
{
	for (int i=0; i < 0x10; i++)
		printf("%02X", *(unsigned char*)(buf + i));
	printf("\n");
}

/* Read a GCI into a `struct gci` and return a pointer to it */
struct gci* read_gci(char *filename)
{
	FILE *f;
	long input_size;
	struct gci *new_gci;

	//printf("[*] Input filename: %s\n", filename);
	f = fopen(filename, "rb");
	if (f == NULL) {
		printf("[!] Couldn't open %s\n", filename);
		return NULL;
	}

	fseek(f, 0, SEEK_END);
	input_size = ftell(f);
	fseek(f, 0, SEEK_SET);
	if (input_size != sizeof(*new_gci)) {
		printf("[!] Input GCI must be 0x%x bytes\n", sizeof(*new_gci));
		fclose(f);
		return NULL;
	}

	//printf("[*] Reading 0x%x bytes ..\n", input_size);

	new_gci = malloc(sizeof(*new_gci));
	memset(new_gci, 0x00, sizeof(*new_gci));
	fread(new_gci, 1, sizeof(*new_gci), f);
	fclose(f);

	return new_gci;
}

/* Compute the checksum over the specified number of bytes in `count` on the
 * buffer specified by `base`, using the buffer `checksum` to store output. 
 * The `checksum` buffer is 0x10 bytes and must be pre-seeded with a certain
 * hard-coded value. */
void do_checksum(void* base, uint32_t count, unsigned char *checksum)
{
	uint32_t bytes_read = 0;
	unsigned char cur = 0;
	unsigned char cur_arr = 0;
	uint8_t arr_pos = 0;

	//uint32_t ctr = (count - 8) / 8;
	uint32_t ctr = (count) / 8;

	unsigned char x = 0;
	unsigned char y = 0;

	while (ctr > 0)
	{
		for (int i = 0; i < 8; i++)
		{
			cur = *(unsigned char*)(base + i);
			cur_arr = *(checksum + (arr_pos & 0xf));
			*(checksum + (arr_pos & 0xf)) = (char)(cur + cur_arr);
			arr_pos++;
		}
		ctr--;
		base += 8;
		bytes_read += 8;
	}

	for (int i = 1; i < 0xf; i++) {
		x = *(checksum + (i-1));
		y = *(checksum + i);
		if (x == y) {
			x = y ^ 0x00FF;
			*(checksum + i) = x;
		}
	}
}

/* Compute checksums over relevant regions of data. 
 *
 * Note that the checksums stored in the GCI at some given time are always a 
 * representation of the *de-obfuscated* data contents! Comparing checksums 
 * against obfuscated contents will always result in a mis-match! */
int checksum_gci(struct gci *gci, int mode, int verb)
{
	int res = 0;
	unsigned char *current;
	unsigned char computed[0x10];

	// Compute the checksum for region_0
	current = gci->checksum_0;
	memcpy(&computed, &checksum_seed, 0x10);
	do_checksum(&gci->region_0, sizeof(gci->region_0), computed);

	if ( memcmp(current, computed, 0x10) == 0) {
		if (verb)
			printf("[*] region_0 checksum is valid\n");
	}
	else {
		res++;
		if (verb) {
			printf("[!] region_0 checksum mismatch!\n");
			printf("[!] Current region_0 checksum:\t"); 
			print_checksum(current);
			printf("[!] Computed region_0 checksum:\t");
			print_checksum(computed);
		}

		if (mode == WRITE_BACK) {
			if (verb)
				printf("[*] Fixing region_0 checksum ...\n");
			memcpy(&gci->checksum_0, &computed, 0x10);
		}
	}

	// Compute the checksum for each data block
	for (int blknum = 0; blknum < 10; blknum++)
	{
		memcpy(&computed, &checksum_seed, 0x10);
		current = &gci->block[blknum].checksum[0];
		do_checksum(&gci->block[blknum].data, 
			    sizeof(gci->block[blknum].data),
			    computed);

		if ( memcmp(current, computed, 0x10) == 0){
			if (verb)
				printf("[*] Block %d checksum is valid\n", blknum);
		}
		else {
			res++;
			if (verb) {
				printf("[!] Block %d checksum mismatch!\n", blknum);
				printf("[!] Current block %d checksum:\t", blknum); 
				print_checksum(current);
				printf("[!] Computed block %d checksum:\t", blknum); 
				print_checksum(computed);
			}

			if (mode == WRITE_BACK) {
				if (verb)
					printf("[*] Fixing block %d checksum ...\n", blknum);
				memcpy(&gci->block[blknum].checksum, &computed, 0x10);
			}
		}
	}

	return res;
}



/* Deobfuscate all relevant regions of the GCI */
void decompress_gci(struct gci *gci)
{
	uint8_t cursor, prev, res;

	// Is the previous byte always 0x00 here? 
	prev = 0x00;

	// For the unk_1 region in the GCI
	for (int i = 0; i < sizeof(gci->unk_1); i++)
	{
		cursor = gci->unk_1[i];
		res = decompress_byte(prev, cursor);
		gci->unk_1[i] = res;
		prev = cursor;
	}

	// For each data block in the GCI
	for (int blknum = 0; blknum < 10; blknum++)
	{
		prev = gci->block[blknum].checksum[0xf];
		for (int i = 0; i < sizeof(gci->block[blknum].data); i++)
		{
			cursor = gci->block[blknum].data[i];
			res = decompress_byte(prev, cursor);
			gci->block[blknum].data[i] = res;
			prev = cursor;
		}
	}
}


/* Obfuscate all relevant regions in the given GCI */
void compress_gci(struct gci *gci)
{
	uint8_t cursor, prev, res;

	// Is the previous byte always 0x00?
	prev = 0x00;

	// For the unk_1 region in the GCI
	for (int i = 0; i < sizeof(gci->unk_1); i++)
	{
		cursor = gci->unk_1[i];
		res = compress_byte(prev, cursor);
		gci->unk_1[i] = res;
		prev = res;
	}

	// For each data block in the GCI
	for (int blknum = 0; blknum < 10; blknum++)
	{
		prev = gci->block[blknum].checksum[0xf];
		for (int i = 0; i < sizeof(gci->block[blknum].data); i++)
		{
			cursor = gci->block[blknum].data[i];
			res = compress_byte(prev, cursor);
			gci->block[blknum].data[i] = res;
			prev = res;
		}
	}
}

/* If this function returns 0, it *must* mean that: 
 *
 *	a. the GCI is already packed!
 *	b. the checksum on unpacked contents is valid!
 *
 * This function returns the number of checksums that need to be fixed. */
int validate_gci(char *filename)
{
	struct gci *scratch = NULL;
	int res = 0;

	scratch = read_gci(filename);
	decompress_gci(scratch);
	res = checksum_gci(scratch, READ_ONLY, 0);
	free(scratch);
	return res;
}

/* Print command-line usage to stdout */
void print_usage(char *name)
{
	printf(
		"WARNING! THIS TOOL IS EXPERIMENTAL - TAKE CARE NOT TO CORRUPT YOUR DATA!\n"
		"THE --pack AND --unpack FLAGS WILL MODIFY THE FILE THAT YOU POINT IT AT!\n"
		"\n"
		"usage:\n"
		"  %s [--unpack | --pack | --checksum] <input GCI>\n"
		"options:\n"
		"  --checksum:\t\"Check and print the checksum values of the input GCI\"\n"
		"  --pack:\t\"Re-obfuscate and save contents of the input GCI\"\n"
		"  --unpack:\t\"De-obfuscate and save contents of the input GCI\"\n"
		,name
	);
}


FILE *out = NULL;
struct gci *input = NULL;
int main(int argc, char* argv[])
{
	int mode = 0;
	int to_fix = 0;
	int unpacked = 0;
	int valid = 0;

	if (argc < 2) {
		print_usage(argv[0]);
		return -1;
	}

	if (strcmp(argv[1], "--unpack") == 0){
		if (argc < 3) {
			print_usage(argv[0]);
			return -1;
		}
		mode = UNPACK_MODE;
	}
	if (strcmp(argv[1], "--pack") == 0){
		if (argc < 3) {
			print_usage(argv[0]);
			return -1;
		}
		mode = PACK_MODE;
	}
	if (strcmp(argv[1], "--checksum") == 0){
		if (argc < 3) {
			print_usage(argv[0]);
			return -1;
		}
		mode = CHECKSUM_MODE;
	}

	switch(mode) {
	case UNPACK_MODE:
		input = read_gci(argv[2]);

		/* First, validate checksums without unpacking anything. 
		 * If all checksums are valid, this means the file is already
		 * unpacked and has not been changed by the user in any way
		 */

		to_fix = checksum_gci(input, READ_ONLY, 0);
		if (to_fix == 0) {
			printf(
			"[!] Detected an unpacked and valid GCI file, refusing to write an unpacked file!\n"
			"    There's no reason to unpack this file because it seems like you:\n"
			"        - Provided a file which is already in an unpacked state\n"
			"        - Provided a file where all checksums are valid\n"
			);
			free(input);
			return -1;
		}

		/* Just refuse to unpack invalid GCIs for now - should prevent
		 * users from totally corrupting the state of files they're 
		 * working on (hopefully?). Note that this doesn't catch cases
		 * where the user gives us an *unpacked AND unchanged* GCI.
		 */

		to_fix = validate_gci(argv[2]);
		if (to_fix != 0) {
			printf(
			"[!] Detected %d invalid checksum[s], refusing to write an unpacked file!\n"
			"    There's no reason to unpack this file because it seems like you may have:\n"
			"        (a) Provided an unpacked GCI with changes to it?\n"
			"        (b) Provided a packed GCI that is somehow corrupted?\n"
			, to_fix);
			return -1;
		}

		printf("[*] Unpacking GCI ...\n");
		decompress_gci(input);
		out = fopen(argv[2], "wb");
		if (out == NULL)
			return -1;
		fwrite(input, sizeof(*input), 1, out);
		fclose(out);
		free(input);

		printf("[!] Wrote unpacked GCI to %s\n", argv[2]);
		break;

	case PACK_MODE:
		to_fix = validate_gci(argv[2]);
		if (to_fix == 0) {
			printf("[!] This GCI is already packed and valid, refusing to write a packed file!\n");
			return 0;
		}

		printf("[*] Packing GCI ...\n");
		input = read_gci(argv[2]);
		to_fix = checksum_gci(input, WRITE_BACK, 0);
		printf("[*] Fixed %d checksum values\n", to_fix);
		compress_gci(input);

		out = fopen(argv[2], "wb");
		if (out == NULL)
			return -1;
		fwrite(input, sizeof(*input), 1, out);
		fclose(out);
		free(input);
		
		printf("[!] Wrote changes to %s\n", argv[2]);
		break;

	case CHECKSUM_MODE:
		printf("[*] Current checksum state:\n");
		input = read_gci(argv[2]);
		decompress_gci(input);
		checksum_gci(input, READ_ONLY, 1);
		break;

	default:
		print_usage(argv[0]);
		return -1;
		break;
	}
}
