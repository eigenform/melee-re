#include "text.h"
#include "ntsc102.h"
#include <stdarg.h>

extern u32 MINORSCENE_CHANGE_REQUEST;
extern u32 PAD_RESET_REQUEST;

static const char *text = "Entered engine loop\n";

void EngineUpdate(void (*minor_onframe_func)()) {
	int steps_todo = 0;
	int steps_done = 0;

	OSReport("%s", text);

	ClearEngineFlags((void*)0x80479d68);
	MINORSCENE_CHANGE_REQUEST = 0;
	HSD_PadFlushQueue(2);

	while (true) {

		if (MINORSCENE_CHANGE_REQUEST != 0) { break; }

		while (true) {
			steps_todo = GetEngineSteps();
			if (steps_todo != 0) { break; }
		}

		if (HSD_PadGetResetSwitch() != 0) {
			PAD_RESET_REQUEST = 1;
			break;
		}
		
		while (steps_done < steps_todo) {
			Do_PadRenewMasterStatus();
			if (minor_onframe_func != 0) { minor_onframe_func(); }
			SFX_ProcessVolume();
			GObj_RunProcs();

			if (MINORSCENE_CHANGE_REQUEST != 0) { break; }
			steps_done = steps_done + 1;
		}
		if (MINORSCENE_CHANGE_REQUEST == 2) { break; }

		GXInvalidateVtxCache();
		GXInvalidateTexAll();
		HSD_StartRender(0);
		CameraTaskScheduler();
		CheckRenderStepIs3();
		HSD_VICopyXFBASync(0);
	}

	HSD_VISetXFBDrawDone();
	return;
}
