# Memory Map

Collected notes on sorting the DOL layout, in-terms of source object files.
The sections in this Markdown file are based on the sections in the DOL.

The process for working on this is basically:

1. Annotate/analyze disassembly until you are bored
2. Xref symbol names with parent object files from existing map files
3. Find functions at the boundaries of source object files
4. Go back to step 1

Map files are shipped inside some retail titles. This allows us to get a rough
picture of the layout by cross-referencing things. 

The Melee DOL includes strings which hint at the naming convention for certain 
source files. I've tried to integrate these where possible. As we approach a 
complete symbol map, ideally we should be able to provide the atom for some
reproduction of the actual map used when the game was linked up.

Boundaries here are all based on _my_ Dolphin symbol map at the time I was 
looking into them, so some symbol names here may be out-of-sync with the ones
in the map, or with the ones in other maps.

## Text section 0
Seems like low-level utility functions live here. The interrupt table is also 
loaded in here.

```
# -----------------------------------------------------------------------------
# Text section 0: 0x80003100 - 0x80005520, size=0x00002420, offset=0x00000100

# Most/all the following are from the .init sections of the named objects.

__mem.o			80003100 (memset)
mem_TRK.o		80003244 (TRK_memcpy)

# 0x80003298 is the start of the interrupt vector table. This section starts 
# with the string: 
#
#	"Metrowerks Target Resident Kernel for PowerPC"
#
# I think that the .init section from dolphin_trk.o might also be here, from
# looking at other maps. Looks like `__TRK_reset` or something might be placed
# immediately after this, in our case? Not sure about this.
#
__exception.o		80003298 (gTRKInterruptVectorTable)
__start.o		800051ec (__check_pad3)
```

## Data section 0
The actual entrypoint and most of the low-level initialization stuff from 
the Gamecube libraries seems to be in this region.

```
# -----------------------------------------------------------------------------
# Data section 0: 0x80005520 - 0x800056c0, size=0x000001a0, offset=0x003b3e20

# This is the entrypoint for the DOL
__start.o		8000522c (__start)

```

## Data section 1
This region seems to be filled with a bunch of pointers to various functions.
Dolphin never seems to pick up accesses on this region. I don't understand 
what lives here [yet].

```
# -----------------------------------------------------------------------------
# Data section 1: 0x800056c0 - 0x80005940, size=0x00000280, offset=0x003b3fc0

TODO
```


## Text section 1
This is where all of the actual game code and libraries are loaded.
I wouldn't be surprised if there are small data sections scattered about this 
region.

```
# -----------------------------------------------------------------------------
# Text section 1: 0x80005940 - 0x803b7240, size=0x003b1900, offset=0x00002520

# Static player block setters/getters seem to start around here.
			800322c0


# Some subaction event functions live here
			80071028


# This is the first instance of one of the `AnimInterrupt` functions from the
# "global" array of animation function tables (non-character specific).
			8008a494




# Character OnLoad functions start here. Character-specific functions in the 
# animation tables (for special moves?) appear to live inside these regions.

			800e0960 (onload_Mario)

 			800e2aec (onload_CaptFalcon)

 			800e57ac (onload_Fox)

 			800eae44 (onload_Link)

 			800ee680 (onload_Kirby)

 			8010d9ac (onload_DonkeyKong)

 			801100ec (onload_Shiek)

 			8011480c (onload_Ness)

 			8011b628 (onload_Peach)

 			8011ef3c (onload_Popo)

 			80122edc (onload_Nana)

 			801243e4 (onload_Pikachu)

 			8012837c (onload_Samus)

 			8012b99c (onload_Yoshi)

 			80132abc (onload_Bowser)

 			801364ac (onload_Marth)

 			80139334 (onload_Zelda)

 			8013c67c (onload_Jigglypuff)

 			80142324 (onload_Luigi)

 			80144e48 (onload_Mewtwo)

 			80148ce4 (onload_YoungLink)

 			801494e4 (onload_DrMario)
 			80149cc4 (onload_Falco)
 			80149e34 (onload_Pichu)

 			8014a37c (onload_GameAndWatch)

 			8014ee1c (onload_Ganon)

 			8014f124 (onload_Roy)
 			8014f3dc (onload_BoyWireframe)
 			8014f440 (onload_GirlWireframe)
 			8014f6b8 (onload_GigaBowser)
 			8014f9d0 (onload_Sandbag)
 			8014fc6c (onload_MasterHand)
 			80155e1c (onload_CrazyHand)



# Functions from the minor scene shared function tables are around here.
# Functions related to "InGame" scenes? 
			8016d32c
# Functions related to "ResultScreen" scenes?
			80177368
# Classic/AllStar/Adventure Mode Splash screen scene functions?
			80186dfc
# Tournament mode scene functions?
			8019628c
# Functions related to "ResultScreen" scenes seem to live around here
			80177368


# Functions from the minor scene tables start here, arranged in blocks related
# to the associated major scene, starting with MainDebugMenu functions
			801b099c

# ClassicMode scene functions?
			801b2d54

# <other scenes>
			...

# Miscellaneous scene functions
			801bf728

# First occurence of functions dealing with the static StaticInfo struct
			801bffb0

# There's a block of stage StaticInfo setters and getters around here
			801c3880

# Stage-specific functions live around here, starting with Fountain:
			801cbb84
# Castle
			801cd338
# Pokemon Stadium
			801d1018
# Kongo Jungle
			801d5238

# <other stages>
			...

# Final Destination
			8021a620

# Target test stages (starting with Mario's)
			8021f840

# Ganon's target test (last in the chunk of target test functions)
			802246d8

# Start of generic stage/camera functions.
			80224a54

# Start of a block of functions relevant to the develop mode 
			802254b8

# Menu relevant functions here-ish
			8022c304

# SSS and CSS scene functions seem to be around here
			80259ed8

# High-level item/entity functions?
			80267978

# Start of regular item functions (from tables), starting with "Capsule," etc.
			8027cf00

# Character projectile item functions seem to start here, with Mario's
			8029b868

# Pokemon [projectile] functions, starting with Goldeen's.
			802c8f4c

# Seems like the start of functions relevant to CPU enemies/monsters
			802d73f0

# Start of another block of functions related to debug menu?
			802ffea4

# Adventure Mode cutscene functions from minor scene shared function tables
			8031cd94

# I believe the Metrowerks libraries start here. Think there are also some
# others mixed in here. K7 map has a list of these. Probably very close to 
# Melee's layout.

__va_arg.o		80322620 (__va_arg)

mem.o			803238c8 (memcmp)
printf.o		80323cf4 (sprintf)

mainloop.o		80326714 (TRKHandleRequestEvent)
nubevent.o		8032687c (TRKInitializeEventQueue?)
nubinit.o		80326ad8 (TRKInitializeNub)
serpoll.o		803274dc (TRKTestForPacket)
dispatch.o		803276a8 (TRKInitializeDispatcher)
msghndlr.o		80327740 (TRKMessageIntoReply)

dolphin_trk.o		8032a628 (InitMetroTRK)
mpc_7xx_603e.o		8032a868 (TRKSaveExtended1Block)
main_TRK.o		8032abe0 (TRK_main)

dolphin_trk_glue.o	8032add4 (TRKInitializeIntDrivenUART)
targcont.o		8032af80 (TRKTargetContinue)


# I think this is the start of [mostly] regular-old SDK libraries
# Pretty straightforward.

hio.o			8032ba6c (ExtHandler)
mcc.o			8032c74c (callbackEventStream)
fio.o			8032ea84 (fioMccChannelEvent)

THPDec.o		8032f630 (__THPPrepBitStream)
jpeg-dec.o		8032f8d4 (JPEGGetFileInfo)

PPCArch.o		80335e5c (PPCMfmsr)
db.o			80335ec0 (DBInit)
dsp.o			80335fc8 (DSPCheckMailToDSP?)
dsp_debug.o		8033620c (__DSP_debug_printf)
dsp_task.o		8033625c (__DSPHandler)
dvdlow.o		80336ae0 (__DVDInitWA)
dvdqueue.o		8033a150 (__DVDClearWaitingQueue)
dvderror.o		8033a348 (__DVDStoreErrorCode)
fstload.o		8033a4a0 (cb)
GXInit.o		8033a6e0 (__GXDefaultTexRegionCallback)
GXFifo.o		8033b788 (GXCPInterruptHandler)

mtxvec.o		80342690 (PSMTXQuat)
mtxvec.o		80342aa8 (PSMTXMUltiVec / C_MTXMultVec)
os.o			80342e94 (OSGetConsoleType)
OSAlloc.o		80343e44 (DLInsert)
OSArena.o		803444c8 (OSGetArenaHi)
OSAudioSystem.o		80344534 (__OSInitAudioSystem)
OSCache.o		803447c8 (DCEnable)
OSContext.o		80344e30 (OSLoadFPUContext)
OSError.o		803456a8 (OSReport)
EXIBios.o		80345a70 (SetExiInterruptMask)
OSFont.o		8034730c (OSGetFontEncode)
OSInterrupt.o		80347364 (OSDisableInterrupts)
OSLink.o		80347bcc (__OSModuleInit)
OSContext.o		80347be4 (OSGetCurrentContext)
OSMemory.o		80347bfc (OSOnReset)
OSMutex.o		80347edc (__OSUnlockAllMutex)
OSReboot.o		80348144 (__OSReboot)
OSReset.o		80348310 (OSRegisterResetFunction)
OSResetSW.o		803486e4 (__OSResetSWInterruptHandler)
OSRtc.o			80348a90 (WriteSramCallback)
SIBios.o		803494bc (SIBusy)
OSSync.o		8034ab80 (SystemCallVector)
OSThread.o		8034ac04 (__OSThreadInit)
OSTime.o		8034c3f0 (OSGetTime)
EXIUart.o		8034c86c (InitializeUART)
EXIAd????.o		8034c8bc (unknown)
__ppc_eabi_init.o	8034cabc (__init_user?)
Padclamp.o		8034cb50 (ClampStick)
Pad.o			8034cd88 (UpdateOrigin)
SISamplingRate.o	8034ddac (SISetSamplingRate)
Pad.o			8034debc (PADControlMotor)
vi.o			8034e964 (__VIRetraceHandler)
ai.o			803503e4 (AIRegisterDMACallback)
ar.o			80350cd0 (ARStartDMA)
arq.o			80351edc (__ARQServiceQueueLo)
CARDBios.o		80352270 (__CARDDefaultApiCallback)
CARDUnlock.o		8035350c (bitrev)
CARDRdwr.o		80354720 (BlockReadCallback)
CARDBlock.o		803549b8 (__CARDGetFatBlock)
CARDDir.o		80354dbc (__CARDGetDirBlock)
CARDCheck.o		80355020 (__CARDCheckSum)
CARDMount.o		80355f5c (CARDProbe)
CARDFormat.o		80356970 (FormatCallback)
CARDOpen.o		80357154 (__CARDCompareFileName)
CARDCreate.o		80357708 (CreateCallbackFat)
CARDRead.o		80357a58 (__CARDSeek)
CARDWrite.o		80357ed0 (WriteCallback)
CARDDelete.o		8035824c (DeleteCallback)
CARDStat.o		80358400 (UpdateIconOffsets)
CARDRename.o		80358898 (CARDRenameAsync)
AX.o			80358a94 (AXInitEx)
AXAlloc.o		80358ac8 (__AXGetStackHead)
AXAux.o			80358f90 (__AXAuxInit)
AXCL.o			803592b4 (__AXGetCommandListCycles)
AXOut.o			80359724 (__AXOutNewFrame)
AXSPB.o			80359d8c (__AXGetStudio?)
AXVPB.o			8035a250 (__AXGetNumVoices)
AXProf.o		8035b678 (__AXGetCurrentProfile)
reverb_hi.o		8035b6c0 (ReverbHICreate)
reverb_std.o		8035c504 (ReverbSTDCreate)
chorus.o		8035cea8 (do_src1)
delay.o			8035d890 (AXFXDelayCallback)
axfx.o			8035dd3c (__AXFXAllocFunction)

# This seems like the start of HAL's sysdolphin libraries according to the map
# that Achilles produced - apparently corresponding to some Killer7 maps.

dobj.o			8035dda0 (HSD_DobjGetFlags)
tobj.o			8035e560 (HSD_TObjRemoveAnimAll)
state.o			803615d0 (HSD_SetupChannelMode)
tev.o			80362024 (HSD_RenderInitAllocData)

# Boundary/function not clear - might be incorrect.
# The function above looks suspiciously like `_HSD_AObjForgetMemory`.
mobj.o			80362d30 (HSD_MObjSetCurrent)

aobj.o			80363fc8 (HSD_AObjInitAllocData)
lobj.o			8036539c (HSD_LObjGetFlags)
cobj.o			803676f8 (HSD_CObjEraseScreen)

# Again, unclear function/boundary. Dunno if this is a cobj or fobj function.
fobj.o			8036a938 (HSD_FObjGetAllocData?)

pobj.o			8036b8d0 (HSD_PObjGetFlags)
jobj.o			8036ec10 (HSD_JObjCheckDepend)
displayfunc.o		803738a0 (HSD_ZListInitAllocData)
initialize.o		80374e48 (HSD_InitComponent)
video.o			8037588c (HSD_VISearchXFBByStatus)
controller.o		8037699c (HSD_PadGetRawQueueCount)
rumble.o		80378090 (HSD_PadRumbleOn)
spline.o		80378a34 (splGetHelmite)
mtx.o			80379598 (HSD_MtxInverseConcat)
util.o			8037a780 (HSD_MulColor)
objalloc.o		8037a94c (HSD_ObjSetHeap)
robj.o			8037ae34 (HSD_RObjInitAllocData)
id.o			8037cd80 (HSD_IDGetAllocData)
wobj.o			8037d050 (HSD_WObjRemoveAnim)
fog.o			8037d970 (HSD_FogSet)
perf.o			8037e1bc (HSD_PerfInitStat)
list.o			8037e3fc (HSD_ListInitAllocData)

# Weird that this is the only function included here from object.o? 
# Perhaps some motion in HSD libs between Melee and K7.
object.o		8037e6c4 (HSD_ObjInfoInit)

quatlib.o		8037e708 (MatToQuat)
memory.o		8037f1b0 (HSD_Free)
shadow.o		8037f250 (HSD_ShadowInitAllocData)
random.o		803804f8 (HSD_Rand)
bytecode.o		803805dc (HSD_ByteCodeEval)

# It's either ClassInfoInit here, or the boundary is the function after this.
class.o			80381be4 (ClassInfoInit?)

# The boundary might be on one of the two functions above `HSD_HashSearch`
hash.o			80382b40 (HSD_HashSearch)
texp.o			80382c00 (HSD_TExpGetType)

# After texp.o, there are a lot of un-named functions that Achilles didn't 
# get to. I'd probably need a copy of K7 to begin looking at it?
texpdiag.o		80385798 (assign_reg)

# Game functions for dealing with savedata start around here, I think.
			803a949c

```


## Data section 2

```
# -----------------------------------------------------------------------------
# Data section 2: 0x803b7240 - 0x803b7260, size=0x00000020, offset=0x003b4240

TODO
```

## Data section 3

```
# -----------------------------------------------------------------------------
# Data section 3: 0x803b7260 - 0x803b7280, size=0x00000020, offset=0x003b4260

TODO
```

## Data section 4

```
# -----------------------------------------------------------------------------
# Data section 4: 0x803b7280 - 0x803b9840, size=0x000025c0, offset=0x003b4280

TODO
```

## Data section 5

Lots of important structures are loaded from the DOL into this region.

```
# -----------------------------------------------------------------------------
# Data section 5: 0x803b9840 - 0x804316c0, size=0x00077e80, offset=0x003b6840

# Array of pointers to character-specific action state function tables
			803c12e0

# Start of action state function tables for special B moves
			803c13e8 

# Start of shared action state function table
			803c2800 

# Character-specific action state function tables live here
			803c7120 (as_table_mario)
			803c7260 (as_table_gigabowser)
			803c72b8 (as_table_captfalcon)
			803c7788 (as_table_fox)
			803c7e18 (as_table_link)

			803c8368 (as_table_kirby)

			803ca04c (as_table_sandbag)
			803cb838 (as_table_dk)
			803cc060 (as_table_sheik)
			803cc650 (as_table_ness)
			803cccb8 (as_table_peach)
			803cd2d0 (as_table_popo)
			803cd838 (as_table_nana)
			803cdd78 (as_table_pikachu)
			803ce2d0 (as_table_samus)
			803ce6d0 (as_table_yoshi)
			803cedc0 (as_table_bowser)
			803cf420 (as_table_marth)
			803cfa58 (as_table_zelda)
			803cfef0 (as_table_puff)
			803d0628 (as_table_luigi)
			803d0b00 (as_table_mewtwo)
			803d0fa0 (as_table_ylink)
			803d1498 (as_table_drmario)
			803d1848 (as_table_falco)
			803d1ea8 (as_table_pichu)
			803d23e8 (as_table_gamenwatch)
			803d29f8 (as_table_ganon)
			803d2e80 (as_table_roy)
			803d3a30 (as_table_masterhand)
			803d35e8 (as_table_wireframe_male)
			803d3998 (as_table_wireframe_female)
			803d41f8 (as_table_crazyhand)


# Array of pointers to stage-specific function tables
			803dfedc

# Start of stage-specific function tables
			803e0e5c (stage_ft_fountain)
			803e11a4 (stage_ft_castle)
			803e1334 (stage_ft_stadium)
			803e1800 (stage_ft_kongo)
			803e1b2c (stage_ft_brinstar)
			803e1f08 (stage_ft_adventurecorneria)
			803e274c (stage_ft_yoshistory)
			803e2858 (stage_ft_onett)
			803e2d20 (stage_ft_bigblue)
			803e33dc (stage_ft_mutecity)
			803e3d94 (stage_ft_fourside)
			803e3f6c (stage_ft_greatbay)
			803e4800 (stage_ft_icemt)
			803e4950 (stage_ft_mk1)
			803e4c00 (stage_ft_mk2)
			803e4d0c (stage_ft_depths)
			803e4ecc (stage_ft_cruise)
			803e5130 (stage_ft_temple)
			803e51cc (stage_ft_yoshisland)
			803e52e0 (stage_ft_jungle)
			803e54cc (stage_ft_venom)
			803e5764 (stage_ft_test)
			803e584c (stage_ft_adventuremk)
			803e5988 (stage_ft_adventurehyrule)
			803e5e0c (stage_ft_adventurebrinstar)
			803e617c (stage_ft_adventurefzero)
			803e62c0 (stage_ft_trophy1)
			803e6370 (stage_ft_trophy2)
			803e6420 (stage_ft_trophy3)
			803e650c (stage_ft_yi64)
			803e65e8 (stage_ft_dkj64)
			803e6748 (stage_ft_dreamland)
			803e6a3c (stage_ft_pokefloats)
			803e76d0 (stage_ft_greens)
			803e7a00 (stage_ft_flatzone)
			803e7b10 (stage_ft_racetofinish)
			803e7d34 (stage_ft_snagtrophies)
			803e7e38 (stage_ft_battlefield)
			803e7f90 (stage_ft_finaldest)
			803e821c (stage_ft_homerun)
			803e84c4 (stage_ft_allstarrest)
			803e85a4 (stage_ft_targetmario)
			803e8664 (stage_ft_targetfalcon)
			803e872c (stage_ft_targetylink)
			803e87ec (stage_ft_targetdk)
			803e88ac (stage_ft_targetdrmario)
			803e8974 (stage_ft_targetfalco)
			803e8a34 (stage_ft_targetfox)
			803e8af4 (stage_ft_targetics)
			803e8c0c (stage_ft_targetkirby)
			803e8ccc (stage_ft_targetbowser)
			803e8d8c (stage_ft_targetlink)
			803e8e4c (stage_ft_targetluigi)
			803e8f0c (stage_ft_targetmarth)
			803e8fcc (stage_ft_targetmewtwo)
			803e908c (stage_ft_targetness)
			803e914c (stage_ft_targetpeach)
			803e920c (stage_ft_targetpichu)
			803e92cc (stage_ft_targetpika)
			803e9394 (stage_ft_targetpuff)
			803e9454 (stage_ft_targetsamus)
			803e9514 (stage_ft_targetsheik)
			803e95d4 (stage_ft_targetyoshi)
			803e9694 (stage_ft_targetzelda)
			803e9754 (stage_ft_targetgnw)
			803e981c (stage_ft_targetroy)
			803e98dc (stage_ft_targetganon)
```

## Data section 6

```
# -----------------------------------------------------------------------------
# Data section 6: 0x804d36a0 - 0x804d63a0, size=0x00002d00, offset=0x0042e6c0

TODO
```

## Data section 7

```
# -----------------------------------------------------------------------------
# Data section 7: 0x804d79e0 - 0x804dec00, size=0x00007220, offset=0x004313c0

TODO
```


After this, the stack region starts at `0x804dec00`.
After the stack should mostly be space for dynamically-allocated memory.
