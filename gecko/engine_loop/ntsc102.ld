
SECTIONS
{
	/* The future location of this function in memory during runtime. */
	. = 0x8019628c;

	.text : 
	{
		*(.text);
	}

	.data : 
	{
		*(.rodata);
		*(.data.*);
	}


	/* These are just symbols from MexTK headers that we don't need */
	/DISCARD/ :
	{
		*(.sdata)
		*(.sdata.*)
		*(.comment)
	}
}

GLOBAL_TEXTOBJ_PTR		= 0x80400930;
GLOBAL_STRING_BUF		= 0x80400954;
MINORSCENE_CHANGE_REQUEST = 0x80479d64;
PAD_RESET_REQUEST		= 0x8046b0f4;

Text_CreateCanvas		= 0x803a611c;
Text_CreateText			= 0x803a6754;
Text_AddSubtext			= 0x803a6b98;
Text_SetText			= 0x803a70a0;

_vsprintf				= 0x80323dc8;
sprintf					= 0x80323cf4;

OSGetTime				= 0x8034c3f0;
OSReport				= 0x803456a8;

HSD_StartRender			= 0x80375538;
HSD_VICopyXFBASync		= 0x803761c0;
HSD_VISetXFBDrawDone	= 0x8037639c;
HSD_PadGetRawQueueCount = 0x8037699c;
HSD_PadFlushQueue		= 0x80376d04;
HSD_PadGetResetSwitch	= 0x803769d8;

GetEngineSteps			= 0x80019894;
Do_PadRenewMasterStatus = 0x800198e0;
SFX_ProcessVolume		= 0x80027df8;
GObj_RunProcs			= 0x80390cfc;
GXInvalidateVtxCache	= 0x8033c898;
GXInvalidateTexAll		= 0x8033f270;
CameraTaskScheduler		= 0x80390fc0;
CheckRenderStepIs3		= 0x803755a8;
RunDiscCheck			= 0x800195d0;
ClearEngineFlags		= 0x801677c0;

