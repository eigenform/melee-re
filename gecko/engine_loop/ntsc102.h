
extern int sprintf(char *str, const char *fmt, ...);
extern void OSReport(char *, ...);

extern void ClearEngineFlags(void *ptr);
extern void RunDiscCheck(void);
extern void Do_PadRenewMasterStatus(void);
extern void SFX_ProcessVolume(void);
extern void GObj_RunProcs(void);
extern void GXInvalidateVtxCache(void);
extern void GXInvalidateTexAll(void);
extern void CameraTaskScheduler(void);
extern void CheckRenderStepIs3(void);
extern u8	GetEngineSteps(void);

extern int  HSD_PadGetResetSwitch(void);
extern u8   HSD_PadGetRawQueueCount(void);
extern void HSD_StartRender(int stage);
extern void HSD_VICopyXFBASync(int pass);
extern void HSD_VISetXFBDrawDone(void);
extern void HSD_PadFlushQueue(int q);


