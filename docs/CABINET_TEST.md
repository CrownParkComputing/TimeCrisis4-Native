# Original cabinet test controls

Press **F10 → Cabinet / Service**. The shared Nuklear menu offers two layers:

## Direct service settings (recommended)

Player's life, difficulty, hit color, free play, game cost, continue cost and
attract sound are edited directly in the menu — the original test menu is not
needed for ordinary changes. **Save & Reset Machine** writes the EEPROM block
with a valid TC4 CRC16 checksum and reboots both linked cabinets together so
they always run identical settings.

| Action | Original board control |
| --- | --- |
| Service credit | Original service switch |
| Insert coin | Original coin input |

## Original test menu (diagnostics)

**F9** toggles the original JVS test DIP on both linked screens. The native
help overlay lists the mapped keys: arrows move and adjust, **E** selects,
**Return** starts, **9** service credit, **5** coin. Use the game's own I/O,
gun and sound test pages for calibration and deep diagnostics; finish its
original exit/save procedure normally.

A live TC4 software check verified original test-switch dispatch and guest
resume. Full calibration and maintenance workflows with an actual gun still
need validation. The linked cabinet pair is documented in
[dual-screen status](DUAL_SCREEN.md).
