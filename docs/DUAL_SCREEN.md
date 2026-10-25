# Time Crisis 4 dual-screen status

`python3 tools/run_tc4.py --dual-screen` launches the linked left/right cabinet
pair through the shared twin supervisor: one machine, two adjacent views, one
sound source, shared pause/quit/test state and synchronized service resets.

## How the link works

TC4 does not use TC3's `ILINK`/`ILSOCK`/`ILDRV` path. The supplied TC4 dongle
provides `USBLINK`, `INET`, `INETCTL`, `AN986` and `LIBNET`: `TC4LOAD` treats the
pair as `192.168.0.1:8020` (master, 1P left) and `192.168.0.2:8020` (slave, 2P
right) exchanging `0x440`-byte MD5-authenticated UDP frames through
doubly-linked packet-node pools in EE RAM.

The compatibility layer implements a native bridge for that protocol. It stubs
the low-level `AN986`/`LIBNET` worker entry points before the game spawns them,
asserts the connected link-state flags, drains each worker's TX-ready node queue
and injects peer frames into its RX-ready queue over local Unix datagram
sockets (`<session>/tc4link-left.sock` / `tc4link-right.sock`) at 60 Hz. The
game's own packet builders, sequence numbers, MD5 checks and link-command
dispatch run unmodified — the bridge only replaces the wire.

Each worker's `LINK AS` side switch is forced from `TC3_CABINET_ROLE`, so the
left machine is always `1 (LEFT)` and the right always `2 (RIGHT)` even when INI
files are synced between workers.

## Verified live

- Handshake completes; both workers log the `0x7`/`0xf` flag sequence and
  sustain 60 Hz TX/RX frames in lockstep.
- Test menu reports `LINK : ON` with `LINK AS : 1 (LEFT)` / `2 (RIGHT)` and no
  `LINK MALFUNCTION`.
- `Cabinet / Service → Save & Reset Machine` writes the EEPROM with a valid TC4
  CRC16 and both workers log `synchronized cabinet reset`.

## Still required before claiming linked gameplay

1. Start only player one and capture two genuine, synchronized camera views
   through a stage transition.
2. Verify per-view aiming, gun calibration and hit registration on both views.
3. Validate full stage transitions, audio, stable real game rate and clean
   shutdown over long runs.
4. Confirm disconnect/loss recovery behavior matches the original hardware.
