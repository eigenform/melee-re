#include <stdint.h>


// This is the initial seed for each checksum
static unsigned char checksum_seed[] = {
	0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF,
	0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54, 0x32, 0x10
};

// Helper functions
uint32_t mask(uint32_t mb, uint32_t me);
uint32_t rotl(uint32_t rx, uint32_t sh);
uint32_t rlwinm(uint32_t rs, uint32_t sh, uint32_t mb, uint32_t me);
uint32_t rlwimi(uint32_t ra, uint32_t rs, uint32_t sh, uint32_t mb, uint32_t me);

// Library functions
uint8_t decompress_byte(uint8_t prev_byte, uint8_t current_byte);
uint8_t compress_byte(uint8_t prev_byte, uint8_t current_byte);
