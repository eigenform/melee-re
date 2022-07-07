#include <stdint.h>

// Checksums live at the 0x2000-byte boundaries
#define BLOCK_SIZE		0x2000
#define BLOCK_DATA_SIZE		0x1ff0
#define CHECKSUM_SIZE		0x0010

#define DENTRY_SIZE		0x0040

// Assume all gamedata GCIs are 11 blocks
#define GCI_SIZE		((BLOCK_SIZE * 11) + DENTRY_SIZE)


// Dentry structure (common to all GC games)
struct dentry {
	uint8_t gamecode[4];
	uint8_t makercode[2];
	uint8_t unused_a;
	uint8_t bi_flags;
	char filename[0x20];
	uint8_t modtime[4];
	uint8_t image_offset[4];
	uint8_t icon_fmt[2];
	uint8_t anim_speed[2];
	uint8_t permissions;
	uint8_t copy_counter;
	uint8_t first_block[2];
	uint16_t block_count;
	uint8_t unused_b[2];
	uint32_t comments_addr;
} __attribute__((__packed__));


struct block_data {
	// This is some metadata about the block I think
	unsigned char unk_0[0x10];

	// This part is stitched up with others into a contiguous region
	unsigned char data[0x1f2c];

	// Don't know what this is yet
	unsigned char unk_1[0xb4];
} __attribute__((__packed__));

struct block {
	unsigned char checksum[CHECKSUM_SIZE];
	union
	{
		unsigned char data[BLOCK_DATA_SIZE];
		struct block_data block_data;
	};
} __attribute__((__packed__));


/* Currently, I've only dealt with two types of savefile. `struct gci` is the
 * regular gamedata savefile, and `struct snapshot` is a savefile with some
 * snapshot data (from using Camera Mode).
 */

struct gci {
	struct dentry dentry;

	// De-obfuscated region with a checksum
	unsigned char region_0[0x1e40];
	unsigned char checksum_0[CHECKSUM_SIZE];

	// Maybe padding
	unsigned char unk_0[0x30];

	// Obfuscated region - don't know what this is
	unsigned char unk_1[0x180];

	// There are ten blocks of gamedata stored in the file
	struct block block[10];
} __attribute__((__packed__));

struct snapshot {
	struct dentry dentry;

	// De-obfuscated region with a checksum
	unsigned char region_0[0x1e40];
	unsigned char checksum_0[CHECKSUM_SIZE];

	// Seems like padding?
	unsigned char unk_0[0x20];

	// At offset 0x1eb0
	unsigned char checksum_1[CHECKSUM_SIZE];
	unsigned char data_header[0x180];

	// At offset 0x2040
	unsigned char checksum_2[CHECKSUM_SIZE];
	unsigned char data[0x1ff0];
} __attribute__((__packed__));
