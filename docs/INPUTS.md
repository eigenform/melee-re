# Context
In order for us to reason about things precisely, it's useful to have some
background knowledge about how some elements of Gamecube hardware/software
typically work.

## Standard Libraries
During the lifetime of the Gamecube, Nintendo developed and maintained a
set of libraries used to perform common low-level tasks like memory management,
interrupt-handling, scheduling, and I/O (i.e. with memory cards, controllers,
etc). These are typically referred to as the "Dolphin SDK libraries" or
"standard libraries". These offer an interface to aspects of the Gamecube 
hardware, and when developing retail titles for the Gamecube, allow developers
to simply link against them and use them instead of having to understand 
low-level details about the platform. 

## Timing and Clocks
Games have access to various hardware timers that can be used to synchronize
certain events in software. These timers are typically tied to the speed of
the main bus clock on the Gamecube. By default, the Gamecube's bus clock speed 
is set to 162Mhz (`0x09a7ec80`, or 162000000).

Many Gamecube games use the decrementer register (DEC, or SPR #22) to schedule
user-configurable interrupts. When set, the decrementer register monotonically
decreases at one-fourth the speed of the bus clock, causing an interrupt when
the timer overflows at zero.

## The Video Interface
Additionally, all Gamecube games are [necessarily] implemented as a loop based 
around the time it takes for a video frame/field to scan out on the screen. 
NTSC-{U,J} titles typically runs at 60Hz, meaning that there are 16.6666... 
milliseconds between "the first horizontal line in a frame" and "the last 
horizontal line in a frame." 

It's also important to know that the time in-between "the last line in a frame"
and "the first line in the next frame" is called the vertical blanking period 
(or "vsync", "vblank," "vertical retrace," etc). In order to synchronize 
software to the tempo of video output, the Gamecube's video interface (VI) is 
typically configured to fire an interrupt when the vertical blanking period 
occurs. 

## The Serial Interface
The Gamecube exposes controller data to the CPU via the 
[serial interface](https://www.gc-forever.com/yagcd/chap5.html#sec5.8) (SI)
registers. Gamecube controllers communicate with the serial interface using Nintendo's 
[Joybus](https://github.com/ExtremsCorner/gba-as-controller/blob/gc/controller/source/main.arm.c)
protocol.

Some Gamecube games opt to manually send/recieve commands/responses from the
serial interface. However, there are various ways to query controllers for 
data. The serial interface can also be configured to automatically send and
recieve commands to/from controllers by configuring the SIPOLL register.

This allows the serial interface to poll controllers at some interval 
determined by various bits in SIPOLL. The polling interval is configured as 
some fraction of the vertical blanking period (i.e. the time it takes to draw 
a frame), and can be used to query controllers very quickly (multiple times
per frame). When a poll is completed, the `SI{0..3}INBUF{H,L}` registers used to
hold the actual responses from some controllers are updated automatically.

# Melee's Engine loop
Here's some pseudo-code representing Melee's in-game main engine loop:

```c
void EngineLoop()
{
  // The period of this loop is one frame/field
  while (true)
  {

    // Dynamically adjust the number of game-engine steps we perform depending 
    // on the number of pending entries in the "raw input queue"

    int steps_todo = GetEngineSteps();

    // Do some number of game-engine steps
    while (steps_done < steps_todo)
    {
      // Consume one entry off "raw input queue," copy to the "master buffer."
      HSD_PadRenewMasterStatus();

      // Copy from "master buffer" to the "copy buffer." Presumably these 
      // percolate into the various functions used to compute actual game state.
      Do_MasterPadToCopyPad();

      // Dispatch all scene-specific code
      TaskScheduler();

      steps_done++;
    }
    ...
    HSD_VICopyXFBASync(0);
  }
}
```

## "Engine Steps"
Note that it's possible for the game engine to compute game state more than one time
per video frame. This depends directly on the number of inputs in the "raw queue."
This is how "Lightning Mode" and similar features are implemented. If the pace of input
polling is sped up, the game engine compensates by computing more than one "game engine step"
per video frame.

## Filling the "raw queue"
Melee uses the decrementer register to schedule the low-level aspect of input polling.
In Melee, the default input polling interval used by the decrementer is hard-coded 
to `0xa4cb8`, meaning: every `0xa4cb8` ticks of the decrementer, an interrupt called 
"the input polling alarm" is fired. The period of this interrupt in milliseconds 
is `0xa4cb8 / ((0x09a7ec80 / 4) / 1000)`, which comes out to 16.6666... milliseconds 
(corresponding _roughly_ to the time it takes to draw a frame).

**FUN FACT!:** _Since NTSC-{U,J} Melee technically runs at 59.94Hz, this means that 
the input polling interval is slightly desynced from the video loop. This means that,
every ~1000th frame, the polling interval will fall totally out-of-sync and drop
a frame of input. Great!_

Typically, Gamecube games use a function in the libraries called `PADRead()` in order
to consume raw inputs off of `SI{0..3}INBUF{H,L}` on the serial interface registers.
In Melee's case, HAL had been simultaneously working on their own set of libraries 
called HSD (**H**AL **S**ys**D**olphin) which are used to wrap up the Gamecube's 
standard libraries in various useful ways.

In Melee, the decrementer exception handler calls a function named `HSD_PadRenewRawStatus()`, 
which is a wrapper around `PADRead()`. Data from `PADRead()` is put on a "raw queue" to be 
consumed when the game engine does a step.
