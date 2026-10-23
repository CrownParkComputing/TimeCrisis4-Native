# Sinden setup for TC4

The shared Linux frontend provides **F10 → Display → Sinden white border** with **Auto detect**, **On** and **Off**, plus 1–5% border width. Auto checks physical USB descriptors roughly once a second. The device count reports hardware presence, not camera-driver health. Force On for setup or an unrecognized device.

Install and start the manufacturer's Linux driver separately. The [official Sinden driver page](https://sindenlightgun.com/drivers/) currently lists the v2.08b archive; its Linux folder is labelled v2.05. The bundled PC driver is `LightgunMono.exe`, uses Mono, and has its own SDL/native-library and USB/camera/serial permission requirements. Use mouse mode for the current frontend. The driver must keep running while you play. No driver or firmware is bundled or installed here.

The foundation's [full Linux driver guide](https://github.com/CrownParkComputing/TimeCrisis3-Native/blob/main/docs/SINDEN.md) documents the exact archive folders, calibration/start commands, official USB identifiers and current restrictions. Download proprietary driver software from Sinden and follow its version-specific instructions.

A white rectangle and black inner gap surround each displayed game view; the game image and its authoritative aim rectangle are inset together. Settings are saved in TC4's own private data root. TC4 currently has one diagnostic view. A border option does not implement the missing TC4 cabinet networking or twin screens.

Calibrate the driver, then use **Cabinet / Test** to check the original game's gun calibration and center/corner hits. Keep all four border edges visible and disable compositor dimming/translucency/rounded clipping on the game window. Do not add a conflicting desktop-wide border over the application border.

A live software integration check on TC4 verified border mode/width, unchanged guest fields during paused edits, the same original GS rectangle for display and aiming, saved/restored preferences and original test-DIP toggle/resume. **No physical Sinden gun, recoil, camera tracking, shot alignment or independent two-gun routing has been validated.** The current input path uses the driver's mouse output in the focused game window.
