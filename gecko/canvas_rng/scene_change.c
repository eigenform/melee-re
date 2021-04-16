#include "text.h"
#include <stdarg.h>

extern int sprintf(char *str, const char *fmt, ...);
extern u32 *GLOBAL_RNG_SEED;
extern Text *GLOBAL_TEXTOBJ_PTR;
extern char GLOBAL_STRING_BUF[0x10];
extern void OSReport(char *, ...);

void OnSceneChange(void) {
	int canvas = Text_CreateCanvas(10, 0, 9, 13, 0, 14, 0, 19);

	GLOBAL_TEXTOBJ_PTR = Text_CreateText(10, canvas);
	GLOBAL_TEXTOBJ_PTR->align = 2;
	GLOBAL_TEXTOBJ_PTR->kerning = 1;
	GLOBAL_TEXTOBJ_PTR->scale.X = 0.5;
	GLOBAL_TEXTOBJ_PTR->scale.Y = 0.5;
	GLOBAL_TEXTOBJ_PTR->trans.X = 615;
	GLOBAL_TEXTOBJ_PTR->trans.Y = 455;

	sprintf(GLOBAL_STRING_BUF, "%08X\n", GLOBAL_RNG_SEED);
	Text_AddSubtext(GLOBAL_TEXTOBJ_PTR, 0, 0, GLOBAL_STRING_BUF);
	return;
}

void PerFrame(void) {
	sprintf(GLOBAL_STRING_BUF, "%08X\n", GLOBAL_RNG_SEED);

	// The subtext id will always be 0 here
	Text_SetText(GLOBAL_TEXTOBJ_PTR, 0, GLOBAL_STRING_BUF);
}
