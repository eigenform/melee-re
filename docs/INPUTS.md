# Input Polling
There are basically two or three interlocking loops that are relevant to
input handling in Melee. Interestingly, the period of the alarm configured 
for input polling is also directly related to the speed of the game engine. 

## 1. The Serial Interface (fetching data from controller hardware)
The GC/Wii exposes controller data to the CPU via the serial interface (SI)
registers (`0xcc006400 - 0xcc006500`). Gamecube controllers communicate using
Nintendo's _Joybus protocol._ 

Melee configures the serial interface to automatically send status requests 
to controllers by configuring the `SIPOLL` register. This allows the serial
interface to poll controllers at some interval determined by bits in `SIPOLL`,
which automatically updates the actual registers that hold responses from
some controller/s (`SI{0..3}INBUF`). The polling interval is configured as 
some fraction of the vertical blanking period (i.e. the time it takes to 
draw a frame).


## 2. The Input Polling Alarm (fetching data from serial interface registers) 
Melee uses the decrementer register (DEC, or SPR22) to schedule some aspects
of input polling. When set, the decrementer monotonically decreases at 
one-fourth the speed of the bus clock and causes an interrupt when the timer
runs out. For Gamecube games, the bus clock is set to 162MHz (0x09a7ec80, 
or 162000000).

In Melee, the default input polling interval used by the decrementer is
hard-coded to `0xa4cb8`: every `0xa4cb8` ticks of the decrementer, an interrupt
called "the input polling alarm" is fired. 

The period of the interrupt in milliseconds is `0xa4cb8 / ((0x09a7ec80 / 4) / 1000)`,
which is 16.6666.. ms (corresponding roughly to the time it takes to draw a frame).

Gamecube games call a library function named `PADRead()` in order to consume 
inputs off `SI{0..3}INBUF` on the serial interface registers. In Melee's case, 
input handling with the Gamecube libraries is also wrapped by HAL's "HSD" library.

In Melee, the decrementer exception handler calls a function named 
`HSD_PadRenewRawStatus()`, which is a wrapper around `PADRead()`. Data from `PADRead()` 
is put on a queue to be consumed by the game engine later in the process.


...
