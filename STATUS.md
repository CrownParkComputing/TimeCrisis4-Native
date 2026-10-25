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

## Linked cabinet pair (verified)

- `tools/run_tc4.py --dual-screen` launches two linked workers through the
  shared twin supervisor — one machine, two adjacent fullscreen views.
- A native bridge in the compatibility layer replaces TC4's AN986 USB-Ethernet
  path: it stubs the game's low-level INET/LIBNET worker entries, asserts the
  connected link-state flags, drains `0x440`-byte MD5-authenticated frames from
  the game's TX-ready packet queue and injects peer frames into its RX-ready
  queue over local Unix datagram sockets (`tc4link-left/right.sock`).
- Live logs showed the handshake completing (`LINK : ON`,
  `LINK AS : 1 (LEFT)` / `2 (RIGHT)`), sustained 60 Hz packet exchange on both
  workers, and the test menu reached with no `LINK MALFUNCTION`.
- `Cabinet / Service` edits the original options directly — player's life,
  difficulty, hit color, free play, game cost, continue cost and attract sound —
  and **Save & Reset Machine** writes the `TSF100-2-NA` EEPROM block with the
  exact TC4 CRC16 (table recovered from `TC4LOAD`) and triggers the game's own
  soft-reset on both workers via the shared reset sequence. Verified live: both
  cabinets logged `synchronized cabinet reset` after a save.
- One worker is muted so the pair produces a single sound source; closing
  either side closes the pair; F9 test mode is synchronized across both.
- Per-cabinet `LINK AS` is forced from the worker role so INI sync cannot flip
  the right cabinet back to 1P.

## Not yet established

Full native game translation, complete stage progression, camera parity during
play, exact gun alignment/calibration, audio equivalence, long-run stability and
linked **gameplay** beyond packet/test-menu exchange remain unverified or
unfinished. Title-screen boot does not establish those outcomes.

The current foundation is PCSX2-derived and executes the original game CPU/VU
programs. This repository supplies the TC4 project boundary and preparation/run
workflow while game-specific translation progresses. The shared renderer/menu
contains working generic controls, but temporal DLSS/FSR/frame generation is not
validated TC4 functionality.

## Native vs emulated split

| Layer | Split |
| --- | --- |
| Host, UI, input & cabinet layer | ~100% native C++/Python |
| Arcade I/O & link hardware (JVS, SRAM, HDD reader, AN986/UDP bridge) | ~100% native HLE |
| GPU presentation (GS → Vulkan) | Hybrid: native backend, emulated GS stream |
| Game code & audio (TC4LOAD EE/VU/IOP, SPU2) | Emulated via x86-64 JIT; ~0% statically recompiled |

Approximate subsystem weight: **~45% native host/arcade infrastructure, ~55%
emulated core**; **0% of TC4LOAD is statically translated today**. Next steps
toward 100% native: static EE/VU recompilation, native IOP module contracts, a
native GS renderer against the game's draw stream, a native SPU2-class mixer,
then matched-replay validation.

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
