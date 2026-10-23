import configparser
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]

def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'tools' / (name + '.py'))
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value

PREP = module('prepare_tc4')
RUN = module('run_tc4')

class PreparationTests(unittest.TestCase):
    def test_mutable_copy_is_independent_and_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, target = root / 'source', root / 'private/card'
            source.write_bytes(b'original card')
            self.assertTrue(PREP.copy_new(source, target))
            target.write_bytes(b'game-modified card')
            self.assertFalse(PREP.copy_new(source, target))
            self.assertEqual(target.read_bytes(), b'game-modified card')
            self.assertEqual(source.read_bytes(), b'original card')
            self.assertNotEqual(source.stat().st_ino, target.stat().st_ino)

    def test_private_destination_rejects_symlink_ancestor(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            local = root / '.local'; local.mkdir()
            actual = local / 'actual'; actual.mkdir()
            (local / 'alias').symlink_to(actual, target_is_directory=True)
            with patch.object(PREP, 'ROOT', root):
                with self.assertRaises(ValueError):
                    PREP.safe_private(local / 'alias/playtest')
                with self.assertRaises(ValueError):
                    PREP.safe_private(root / 'outside')
                with self.assertRaises(ValueError):
                    PREP.safe_private(local / '../outside')

    def test_settings_select_tc4_dongle_and_disable_patches(self):
        config = PREP.settings()
        self.assertEqual(config.get('MemoryCards', 'Slot1_Filename'), 'NM00032.ps2')
        self.assertFalse(config.getboolean('EmuCore', 'EnablePatches'))
        self.assertFalse(config.getboolean('EmuCore', 'EnableCheats'))
        self.assertEqual(config.get('EmuCore/GS', 'Renderer'), '14')
        self.assertFalse(config.getboolean('InputSources', 'SDL'))

class LaunchTests(unittest.TestCase):
    def test_tc3_cabinet_adapter_is_removed(self):
        with patch.dict(os.environ, {'TC3_CABINET_ROLE': 'right', 'TC3_CABINET_DIR': '/private/session'}):
            env = RUN.environment()
            self.assertNotIn('TC3_CABINET_ROLE', env)
            self.assertNotIn('TC3_CABINET_DIR', env)

    def test_wrong_game_manifest_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            data = Path(directory)
            (data / 'games').mkdir(); (data / 'PCSX2x6/inis').mkdir(parents=True)
            (data / 'PCSX2x6/inis/PCSX2.ini').write_text('[Filenames]\nBIOS=246C.bin\n')
            manifest = data / 'games/NM00032.acgame'
            manifest.write_text('[game]\ngameid=NM00012\nplatform=246\n[data]\nmedia=DVD\n')
            with self.assertRaises(ValueError):
                RUN.command_for(Path('/foundation/tc3-native'), data)
            manifest.write_text('[game]\ngameid=NM00032\nplatform=super256\n[data]\nmedia=HDD\n')
            command = RUN.command_for(Path('/foundation/tc3-native'), data, 90)
            self.assertEqual(command[-2:], ['--seconds', '90'])
            self.assertIn(str(manifest), command)

    def test_foundation_path_is_explicit_and_configurable(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                RUN.foundation_path(None)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            binary = root / '.local/core-build/bin/tc3-native'
            binary.parent.mkdir(parents=True); binary.write_text('#!/bin/sh\n'); binary.chmod(0o700)
            self.assertEqual(RUN.foundation_path(root), (root, binary))
            with patch.dict(os.environ, {'TC3_NATIVE_ROOT': str(root)}):
                self.assertEqual(RUN.foundation_path(None), (root, binary))

if __name__ == '__main__':
    unittest.main()
