# Time Crisis 4 Native

A separate Time Crisis 4 project using the Linux/Vulkan/Nuklear compatibility
foundation developed in [TimeCrisis3-Native](https://github.com/CrownParkComputing/TimeCrisis3-Native).
The current milestone is an authentic **TC4 normal boot into attract mode and the
title screen**. Complete native translation, linked twin screens and Android
playability are unfinished.

![Original Time Crisis 4 title reached by normal boot](docs/screenshots/tc4-title.png)

This is an actual TC4 renderer screenshot from the World TSF1002/A49 package,
captured with the foundation's F8 screenshot command on 24 October 2026.
It demonstrates title-screen boot, not completed gameplay or dual-screen support.

## Build the shared foundation

Target: Linux x86-64 with Vulkan. Build the playable target using the foundation's
README, then point this project's launcher at that checkout. The path is
configurable; no particular sibling directory is required.

```sh
git clone https://github.com/CrownParkComputing/TimeCrisis3-Native.git /path/to/TimeCrisis3-Native
export TC3_NATIVE_ROOT=/path/to/TimeCrisis3-Native
git -C "$TC3_NATIVE_ROOT" checkout 74880d42caa7107dd443ebc993677930b1a1b6d6
# Follow that checkout's build/dependency instructions first.
test -x "$TC3_NATIVE_ROOT/.local/core-build/bin/tc3-native"
```

The tested foundation commit is pinned in [foundation.lock.json](foundation.lock.json).
Build that revision to include the TC4 title, cabinet/test, Sinden and twin-launch gates.

The executable currently retains the `tc3-native` filename. Its in-process
PCSX2-derived core loads TC4's own manifest, firmware, HDD and dongle; this
repository does not pretend that those execution components are already fully
translated native TC4 code. See [STATUS.md](STATUS.md) for the tested scope.

## Prepare your own game files

No game, BIOS, dongle or HDD data is included. Install `unsquashfs` and Python 3.11
or later, then supply the known World TSF1002/A49 assets:

- `Time Crisis 4.squashfs`, containing the HDD CHD, `proverb.elf`, SRAM and manifest.
- Your `256_memcards.zip`, containing `256_memcards/timecrs4-tsf1002-na-a.bin`.
- Your existing `246C.bin`, `246C.nvm` and `246C.mec` BIOS directory.

```sh
python3 tools/prepare_tc4.py \
  --package '/path/to/Time Crisis 4.squashfs' \
  --cards /path/to/256_memcards.zip \
  --bios-dir /path/to/bios
```

Preparation verifies the known asset hashes and creates private storage beneath
`.local/`. Mutable settings, memory cards and SRAM are independent copies and are
preserved when preparation is repeated. HDD storage needs several gigabytes of
free space. Original supplied assets are opened for reading only.

## Run TC4

```sh
python3 tools/run_tc4.py --dry-run
python3 tools/run_tc4.py
# A bounded diagnostic, or a background session:
python3 tools/run_tc4.py --seconds 90
python3 tools/run_tc4.py --background
```

Use `--foundation /path/to/checkout` instead of the environment variable if
preferred. Use `--data-root` to select another prepared private TC4 directory.
The launcher checks for TC4's `NM00032`/Super256/HDD manifest and disables the
TC3-specific cabinet transport environment.

Mouse aiming, left-button trigger, Space pedal, `5` coin and Return start are
configured as the input baseline. **F10** opens the shared Nuklear menu;
arrow keys and Enter navigate it; Escape resumes. **F8** captures the renderer's
own game image. Actual TC4 gun calibration, shot alignment and full gameplay
have not yet been validated.

The shared menu includes **Cabinet / Test** controls for the original game test
menu, directions, Enter/Button 1, service credit and coin. The foundation also
provides Sinden USB detection and an inset white border: Display → Sinden white
border → Auto detect/On. Start the official Sinden Linux driver separately using
[Sinden driver instructions](docs/SINDEN.md). A physical Sinden device and TC4 calibration
have not been tested here.

See [cabinet maintenance controls](docs/CABINET_TEST.md) and [Sinden setup](docs/SINDEN.md).

## Dual screens

**TC4 dual-screen support is not implemented or validated.** There is no working
TC4 twin-screen launch command yet. `--dual-screen` deliberately reports this
status. Do not use TC3's cabinet-pair launcher as a TC4 setup procedure.

[Dual-screen notes](docs/DUAL_SCREEN.md) explain the separate transport work and
acceptance checks. TC3's genuine linked partner view is a milestone of the TC3
project; it is not evidence that TC4 networking works.

## Validation and screenshots

```sh
python3 -m unittest discover -s tests -v
python3 tools/prepare_tc4.py --help
python3 tools/run_tc4.py --help
```

The screenshots in [docs/screenshots](docs/screenshots) are authentic TC4 output.
Private logs, input hashes and raw snapshots remain under `.local/`; they are not
published. The code is GPL-3.0-or-later; see [COPYING](COPYING).
