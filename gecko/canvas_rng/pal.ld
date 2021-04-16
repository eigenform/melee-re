
SECTIONS
{
	/* The future location of this function in memory during runtime. */
	. = 0x80196dd4;

	/* These are just symbols from MexTK headers that we don't need */
	/DISCARD/ :
	{
		*(.sdata)
		*(.sdata.*)
	}
}

GLOBAL_RNG_SEED		= 0x804c71b8;

GLOBAL_TEXTOBJ_PTR	= 0x804017d0;
GLOBAL_STRING_BUF	= 0x80400954;

OSReport		= 0x80345a84;
Text_CreateCanvas	= 0x803a6044;
Text_CreateText		= 0x803a6664;
Text_AddSubtext		= 0x803a6b54;

Text_SetText		= 0x803a7054;

_vsprintf		= 0x80324078;
sprintf			= 0x80323fa4;
