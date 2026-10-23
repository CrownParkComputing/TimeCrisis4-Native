#!/usr/bin/env python3
"""Prepare private TC4 World TSF1002/A49 assets; game data is never distributed.

Requires the user's own SquashFS package, dongle archive and 246C BIOS files.
Existing mutable SRAM, memory-card data and settings are preserved on rerun.
"""
import argparse
import configparser
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
CARD_ENTRY = '256_memcards/timecrs4-tsf1002-na-a.bin'
PINS = {
    'proverb.elf': '06c2e31d9a133291be11156b2b2c8074a9278d7ec7a0a5bacbf6f939e03492a0',
    'sram.bin': 'b33a1c338e8ef128bf3c664bea7135024c5214ad19ec13d38f4e60dbb289713b',
    'NM00032 TSF1-HA (HDD).chd': '2538a37bc48cf8e83f29781d152b956ca28535278ee081b46e7832bae9c5c82c',
    'Time Crisis 4.acgame': 'ad162389c679e3131d9a7dff625a99b6ffdf2cba7cfab5291ab9ac0f65dd9034',
}
CARD_HASH = 'f4f555d91118a5c65426eb9ef1acb2a5e4b68cdcd6e6ffb9de64d4149d0ad824'
BIOS_HASH = '8eb8f4d963dde4659de4fbb6eca870077f9af59a9100e8eecd59ec836ff79fae'


def sha(path):
    with path.open('rb') as source:
        return hashlib.file_digest(source, 'sha256').hexdigest()


def require_hash(path, expected):
    if path.is_symlink() or not path.is_file() or sha(path) != expected:
        raise ValueError('Unexpected private asset or SHA-256 mismatch: ' + str(path))


def safe_private(path, inspect_children=True):
    if '..' in path.parts:
        raise ValueError('Private destination must not contain parent traversal')
    path = path.absolute()
    if not path.is_relative_to((ROOT / '.local').absolute()):
        raise ValueError('Private destination must be inside this project .local directory')
    for parent in [path, *path.parents]:
        if parent.is_symlink():
            raise ValueError('Private destination contains a symlink: ' + str(parent))
    if inspect_children and path.exists():
        for child in path.rglob('*'):
            if child.is_symlink():
                raise ValueError('Unexpected symlink in mutable private storage: ' + str(child))
    return path


def copy_new(source, destination):
    if destination.exists():
        if destination.is_symlink() or not destination.is_file() or os.path.samefile(source, destination):
            raise ValueError('Mutable target is not an independent private file: ' + str(destination))
        return False
    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix='.tc4-prepare-', dir=destination.parent)
    os.close(descriptor)
    try:
        shutil.copyfile(source, temporary)
        os.chmod(temporary, 0o600)
        try:
            # Atomic exclusive publication: a concurrent preparation must never
            # replace mutable data created by the first preparer or the game.
            os.link(temporary, destination)
        except FileExistsError:
            if destination.is_symlink() or not destination.is_file() or os.path.samefile(source, destination):
                raise ValueError('Concurrent private target is not an independent file: ' + str(destination))
            return False
    finally:
        Path(temporary).unlink(missing_ok=True)
    return True


def settings():
    values = {
        'UI': {'SettingsVersion': '1', 'SetupWizardIncomplete': 'false', 'PauseOnFocusLoss': 'false'},
        'Filenames': {'BIOS': '246C.bin'},
        'EmuCore': {'EnableFastBoot': 'true', 'EnablePatches': 'false', 'EnableCheats': 'false',
                    'EnableWideScreenPatches': 'false', 'EnableNoInterlacingPatches': 'false',
                    'SaveStateOnShutdown': 'false'},
        'EmuCore/CPU/Recompiler': {'EnableEE': 'true', 'EnableIOP': 'true', 'EnableVU0': 'true',
                                 'EnableVU1': 'true', 'EnableFastmem': 'true'},
        'EmuCore/Speedhacks': {'EECycleRate': '0', 'EECycleSkip': '0', 'vuThread': 'true'},
        'EmuCore/GS': {'Renderer': '14', 'upscale_multiplier': '1', 'AspectRatio': '4:3',
                       'OsdMessagesPos': '0', 'OsdPerformancePos': '0', 'fxaa': 'false',
                       'CASMode': '0', 'CASSharpness': '50', 'VsyncEnable': 'false', 'VsyncQueueSize': '2'},
        'InputSources': {'SDL': 'false', 'Evdev': 'false'},
        'MemoryCards': {'Slot1_Filename': 'NM00032.ps2', 'Slot2_Filename': ''},
        'USB1': {'Type': 'guncon2', 'guncon2_Pointer': 'Pointer-0',
                 'guncon2_Trigger': 'Pointer-0/LeftButton', 'guncon2_A': 'Keyboard/Space',
                 'guncon2_Start': 'Keyboard/Return'},
        'JVS': {'LightgunLinkAs2P': 'false', 'ToggleTestMode': 'Keyboard/F9', 'Coin1': 'Keyboard/5',
                'P1_Start': 'Keyboard/Return', 'P1_Service': 'Keyboard/9', 'P1_Up': 'Keyboard/Up',
                'P1_Down': 'Keyboard/Down', 'P1_Button1': 'Keyboard/E'},
    }
    config = configparser.ConfigParser(interpolation=None)
    config.optionxform = str
    config.read_dict(values)
    return config


def prepare(package, cards, bios, destination):
    local = safe_private(ROOT / '.local', inspect_children=False)
    destination = safe_private(destination)
    # The CHD lives in owned private storage, never in the Git source tree.
    if not destination.is_relative_to(local):
        raise ValueError('Private playtest must remain inside .local')
    bios = bios.resolve()
    require_hash(bios / '246C.bin', BIOS_HASH)
    for name in ('246C.nvm', '246C.mec'):
        if not (bios / name).is_file():
            raise ValueError('Supply the existing BIOS companion file: ' + str(bios / name))
    local.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(cards) as archive:
        info = archive.getinfo(CARD_ENTRY)
        if info.file_size != 8650752:
            raise ValueError('Unexpected raw PS2 dongle size')
        card = archive.read(info)
    if hashlib.sha256(card).hexdigest() != CARD_HASH or not card.startswith(b'Sony PS2 Memory Card Format '):
        raise ValueError('TC4 raw memory-card identity mismatch')
    hashes = {}
    with tempfile.TemporaryDirectory(prefix='tc4-extract-', dir=local) as temporary:
        unpacked = Path(temporary) / 'package'
        subprocess.run(['unsquashfs', '-no-progress', '-processors', '2', '-d', str(unpacked),
                        str(package.resolve()), *PINS], check=True, stdout=subprocess.DEVNULL)
        for name, expected in PINS.items():
            require_hash(unpacked / name, expected)
            hashes[name] = expected
        asset = local / 'assets'
        safe_private(asset)
        asset.mkdir(parents=True, exist_ok=True)
        original_card = Path(temporary) / 'NM00032.ps2'
        original_card.write_bytes(card)
        for source, target, expected in [
            (original_card, asset / 'NM00032-original.ps2', CARD_HASH),
            (unpacked / 'NM00032 TSF1-HA (HDD).chd', asset / 'NM00032.chd', PINS['NM00032 TSF1-HA (HDD).chd']),
        ]:
            if target.exists():
                require_hash(target, expected)
            else:
                copy_new(source, target)
        games = destination / 'games'
        games.mkdir(parents=True, exist_ok=True)
        # Immutable HDD is independent of the source package and original media.
        media = games / 'NM00032.chd'
        if media.exists():
            require_hash(media, PINS['NM00032 TSF1-HA (HDD).chd'])
        else:
            copy_new(asset / 'NM00032.chd', media)
        for source, target in [
            (unpacked / 'proverb.elf', games / 'proverb.elf'),
            (unpacked / 'sram.bin', games / 'sram.bin'),
            (asset / 'NM00032-original.ps2', destination / 'PCSX2x6/memcards/NM00032.ps2'),
            *[(bios / name, destination / 'PCSX2x6/bios' / name) for name in ('246C.bin', '246C.nvm', '246C.mec')],
        ]:
            copy_new(source, target)
        require_hash(games / 'proverb.elf', PINS['proverb.elf'])
        require_hash(destination / 'PCSX2x6/bios/246C.bin', BIOS_HASH)
    ini = destination / 'PCSX2x6/inis/PCSX2.ini'
    ini.parent.mkdir(parents=True, exist_ok=True)
    if not ini.exists():
        with ini.open('x') as output:
            settings().write(output)
    manifest = games / 'NM00032.acgame'
    if not manifest.exists():
        config = configparser.ConfigParser(interpolation=None)
        config.read_dict({'game': {'name': 'Time Crisis 4 [World, TSF1002 Ver. A49]',
                                  'gameid': 'NM00032', 'platform': 'super256'},
                          'data': {'subdir': '', 'elf': 'proverb.elf', 'dongle': 'NM00032.ps2',
                                   'mediasrc': 'NM00032.chd', 'media': 'HDD', 'sram': 'sram.bin',
                                   'jvsmode': 'lightgun'}})
        with manifest.open('x') as output:
            config.write(output)
    for directory in ('logs', 'cache', 'snaps', 'sstates'):
        (destination / 'PCSX2x6' / directory).mkdir(parents=True, exist_ok=True)
    report = {'schema_version': 1, 'game': 'NM00032', 'variant': 'World TSF1002/A49',
              'data_root': str(destination), 'manifest': str(manifest),
              'private_asset_sha256': {**hashes, 'dongle': CARD_HASH, 'bios': BIOS_HASH},
              'mutable_files': 'Independent private copies; existing files preserved',
              'dual_screen': 'Not implemented or validated for TC4; TC3 link adapter must stay disabled'}
    (destination / 'preparation.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package', required=True, type=Path, help='User-owned Time Crisis 4.squashfs')
    parser.add_argument('--cards', required=True, type=Path, help='User-owned 256_memcards.zip')
    parser.add_argument('--bios-dir', required=True, type=Path, help='Directory with 246C.bin/.nvm/.mec')
    parser.add_argument('--data-root', type=Path, default=ROOT / '.local/playtest')
    args = parser.parse_args()
    try:
        print(json.dumps(prepare(args.package, args.cards, args.bios_dir, args.data_root), indent=2))
    except (OSError, ValueError, KeyError, zipfile.BadZipFile, subprocess.CalledProcessError) as error:
        parser.exit(1, f'TC4 preparation failed: {error}\n')


if __name__ == '__main__':
    main()
