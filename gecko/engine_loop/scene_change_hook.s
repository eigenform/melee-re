.include "../macro.asm"

# Replace the `bl EngineUpdate` at 0x801a40f0 with `bl EngineTemplate`.

_start:
	bl EngineTemplate
