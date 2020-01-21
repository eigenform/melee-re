#include <stdio.h>
#include <stdlib.h>
#include <gccore.h>
#include <ogcsys.h>
#include <unistd.h>
#include <fat.h>

#include "clamp.h"

static void *xfb = NULL;
static GXRModeObj *rmode = NULL;

// Initial setup for video, controllers
void initialize(void)
{
	VIDEO_Init();
	PAD_Init();

	rmode = VIDEO_GetPreferredMode(NULL);
	xfb = MEM_K0_TO_K1(SYS_AllocateFramebuffer(rmode));
	console_init(xfb, 20, 20, rmode->fbWidth, rmode->xfbHeight,
			rmode->fbWidth * VI_DISPLAY_PIX_SZ);

	VIDEO_Configure(rmode);
	VIDEO_SetNextFramebuffer(xfb);
	VIDEO_SetBlack(FALSE);
	VIDEO_Flush();
	VIDEO_WaitVSync();

	if(rmode->viTVMode & VI_NON_INTERLACE) 
		VIDEO_WaitVSync();

	if (!fatInitDefault())
		exit(0);
}

u8 x_s = 0;
u8 y_s = 0;
u8 last_x_s = 0;
u8 last_y_s = 0;

double last_x_f = 0;
double last_y_f = 0;
double x_f = 0;
double y_f = 0;
u32 pad_x = 0;
u32 pad_y = 0;

int main(int argc, char **argv)
{
	initialize();

	FILE *fp = fopen("test.txt", "w");

	// For each possible PADRead x value
	pad_x = 0;
	while (pad_x <= 0xff)
	{
		// For each possible PADRead y value
		pad_y = 0;
		while (pad_y <= 0xff)
		{
			// Clamp the x and y analog values
			x_s = (u8)pad_x;
			y_s = (u8)pad_y;
			clamptest(&x_s, &y_s, 0x01, 0x00, 0x50);

			// Convert to float representation
			__convert_to_float(x_s, &x_f);
			__convert_to_float(y_s, &y_f);

			printf("x=%02x,y=%02x x=%02x,y=%02x x=%f,y=%f\n",
				pad_x, pad_y, x_s, y_s, x_f, y_f);
			fprintf(fp, "0x%02x,0x%02x 0x%02x,0x%02x %f,%f\n",
				pad_x, pad_y, x_s, y_s, x_f, y_f);


			last_x_f = x_f;
			last_y_f = y_f;
			last_x_s = x_s;
			last_y_s = y_s;
			x_s = 0; y_s = 0; x_f = 0; y_f = 0; pad_y++;
		}

		pad_x++;
	}

	fclose(fp);

	printf("[*] Press START to exit\n");
	while(1) 
	{
		PAD_ScanPads();
		u32 pressed = PAD_ButtonsDown(0);
		if ( pressed & PAD_BUTTON_START ) exit(0);
		VIDEO_WaitVSync();
	}
	return 0;
}
