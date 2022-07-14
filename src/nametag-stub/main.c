#include <stdint.h>
#include "ssbm_ntsc_usa_12.h"

static unsigned char *info_string = "hello, world!";
void loader_main(void) 
{
	OSReport("%s\n", info_string);
	OSReport("Entering loader ...");

	// Do things here
	// ...

	OSReport("Exiting loader ...");
}
