# Time Crisis 4 dual-screen status

A genuine second cabinet view must show the other camera and stay synchronized
with player one, including when only player one has joined. Two unrelated game
windows or a mirrored first view do not satisfy that requirement.

TC4 has not reached that milestone. The supplied TC4 dongle includes `USBLINK`,
`INET`, `INETCTL`, `AN986`, `LIBNET` and related modules; the TC3 dongle instead
provides the `ILINK`/`ILSOCK`/`ILDRV` path used by TC3's implemented adapter.
The presence of these modules is static inventory evidence, not a completed TC4
transport implementation or a runtime proof of the precise protocol.

The TC4 launcher removes `TC3_CABINET_ROLE` and `TC3_CABINET_DIR`. Its
`--dual-screen` option returns an explicit unavailable error. The shared menu's
TC3 twin-cabinet action must stay disabled for the `NM00032` game ID.

Before publishing TC4 twin-screen instructions, implementation and testing must
cover:

1. Trace TC4's actual link setup, peer identity, send/receive and timing contracts.
2. Run isolated left/right storage and execution state with that transport.
3. Observe the original game recognizing its link, with actual packet exchange.
4. Start only player one and capture two genuine, synchronized camera views.
5. Verify per-view aiming, shared pause/quit, rendering settings and Sinden borders.
6. Validate full stage transitions, audio, stable real game rate and clean shutdown.

Until those checks pass there is no TC4 dual-screen command to recommend. Use
single-cabinet `tools/run_tc4.py` for the currently documented boot diagnostic.
