# Original cabinet test controls

Press **F10 → Cabinet / Test**. The shared Nuklear menu offers:

| Action | Original board control |
| --- | --- |
| Toggle original test menu | JVS test DIP switch, also available as F9 |
| Up / Down / Left / Right | Original JVS directions |
| Enter / Button 1 | Original JVS Button 1 |
| Service credit | Original service switch |
| Insert coin | Original coin input |

Selecting a control resumes the game and closes Nuklear so the original cabinet can process it. Press F10 again for the next control. Momentary direction, Enter and Service inputs release after six guest video fields; the test switch stays toggled until toggled again or the original configuration changes.

Use TC4's own on-screen instructions for I/O, gun, sound and game settings. Finish its original exit/save procedure normally. The frontend does not bypass those screens or write arbitrary values into game storage. F9, Up/Down, E, 9 and 5 remain keyboard alternatives outside Nuklear.

A live TC4 software check verified original test-switch dispatch and guest resume. Full calibration and maintenance workflows with an actual gun still need validation. TC4's unimplemented twin-cabinet transport stays disabled; see [dual-screen status](DUAL_SCREEN.md).
