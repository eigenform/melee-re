# Debug Menu functionality

| Debug Level| Name          |
| ---------- | ------------- |
| 0          | Master        |
| 1          | No-Debug-Rom  |
| 2          | Debug-Develop |
| 3          | Debug-Rom     |
| 4          | Develop       |


| When/Where/How | Inputs  | Description |
| ---------- | ------- | ----------- |
| On Boot, if `debug.ini` is present  | Hold **Y** | Elevate debug level |
| On Boot, if `debug.ini` is present  | Hold **R** | Invoke EXI2USB setup |
| Main Menu, if debug level is 3 | Press **Y** | Invoke the debug menu |
| Main Menu, if debug level is 3 | Press **X** | Invoke the sound-test menu |
| Anywhere, if debug level is 3  | **X + Pad-Up** for pause, **Z** for frame-advance | Pause all animation, frame-advance |
| On a Crash, if debug level is 3 (?) | Input the following button combos in this order: **(Z + R + L)**, **(Y + Pad-Up)**, **(A + Pad-Down)**, **(B + Pad-Left)**, **(X + Pad Right)**. | Invoke the exception-handler menu |
| Anywhere, if debug level is 3 | **X + Right** | Draw CPU/memory stats at bottom screen; invokes `OSReport` diagnostic messages about heap/stack usage, `sysdolphin` object allocations | 
| When menu pop-ups occur, if debug level is 3 | Hold **L + R** and press **A** | Allows you to cycle through the list of potential display messages by pressing **L** or **R**. |


## Additional Notes

- At boot-time, the function at `0x8015fda4` calls `DVDConvertPathToEntrynum` in an attempt
  to find a `debug.ini` on-disc (typically, only `usa.ini` is on-disc). If present, the 
  user can hold 'Y' during boot to elevate into debug mode. I think holding 'X' will
  move the level downwards.

- Holding 'R' during boot (where debug level > 3?) will invoke EXI2USB setup (some day 
  I'll implement one of these in Dolphin and play around with this)

- The verbosity of Melee's exception handler is controlled by the debug level.
  During a crash, inputting a secret button combinations in succession
  will write OSReport output and stack dump information to the framebuffer (I think this
  functionality is also in _Kirby Air Ride_, another HAL release on the Gamecube).
  For certain debug levels (I think 3?), the exception handler also includes
  an interactive way to inspect memory.

* According to UP, holding **L** and entering the Gallery will allow you to debug the model 
  viewer. Holding **R** seems to invoke a menu used to unlock trophies?
