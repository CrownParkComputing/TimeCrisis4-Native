# TC4 status

## Observed

- The supplied package identifies **Time Crisis 4 [World, TSF1002 Ver. A49]**,
  `NM00032`, Super256, HDD.
- The raw PS2 dongle is 8,650,752 bytes with ECC spare areas and contains
  `TC4LOAD`/`TC4GAME`. Original media and firmware remain private.
- A normal boot through the shared Linux/Vulkan foundation reached TC4's original
  attract movie and title screen. Bounded diagnostics exited cleanly.
- Retained screenshots were requested through the actual GS renderer with F8.
  Their pixel origin is the TC4 process, independent of overlapping desktop apps.
- Existing code enables a configurable foundation path, pinned input validation,
  isolated private preparation and a TC4-only launch manifest.

## Not yet established

Full native game translation, complete stage progression, camera parity during
play, exact gun alignment/calibration, audio equivalence, long-run stability,
TC4 cabinet networking and genuine dual-screen gameplay remain unverified or
unfinished. Title-screen boot does not establish those outcomes.

The current foundation is PCSX2-derived and executes the original game CPU/VU
programs. This repository supplies the TC4 project boundary and preparation/run
workflow while game-specific translation progresses. The shared renderer/menu
contains working generic controls, but temporal DLSS/FSR/frame generation is not
validated TC4 functionality.

Sinden detection and white borders come from the shared foundation. Their
availability does not prove a physical gun, driver, calibration or shot hit test
has passed for TC4. Follow the original cabinet's gun test before assessing aim.

Android touchscreen shooting remains a requested future target. The present
shared execution core has no complete working ARM64 CPU recompiler path; no
playable Android APK is claimed.

## Dependency and evidence

The public dependency is
[TimeCrisis3-Native](https://github.com/CrownParkComputing/TimeCrisis3-Native).
The parent project records its pinned PCSX2 source and shared-layer provenance.
The tested foundation revision is recorded in `foundation.lock.json`. Local diagnostic
binary hashes, complete asset hashes and original native snapshots are retained
privately in `.local/`.

## Shared frontend integration

The live TC4 software check passes Sinden border mode/width and persisted
restoration, unchanged paused guest fields, matching GS display/aim rectangles,
and original cabinet test-DIP toggle/resume. The shared menu blocks TC3 twin
launch for this game ID. This does not establish physical gun tracking or full
maintenance/calibration workflows.
