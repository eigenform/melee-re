/* Setting the entrypoint here seems to be flaky on occasion. I also have 
 * `--section-start=.text=<ENTRYPOINT>` in the LDFLAGS, and this seems to do
 * the trick. I'm afraid to change it. 
 *
 * Good luck, because I have no idea what *your* linker will do with this!
 */

MEMORY
{
	RAM (rwx) : ORIGIN = 0x80000000, LENGTH = 24M
	USER_CODE (rwx) : org = 0x8045d930, l = 55K
}

SECTIONS
{
	.text :
	{
		entry.o
		. += 0x20;
		. = ALIGN(0x40);
		main.o
		. += 0x20;
		. = ALIGN(0x40);
	} >USER_CODE
}
