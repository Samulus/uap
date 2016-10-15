#!/usr/bin/env python3
"""
    pruner.py
    Author: Samuel Vargas
    Date: 10/12/2016

    This module is responsible for accepting a list of files that are
    suspected to be audio files (i.e. end with a audio extension) and checks the
    header of each file for the presence of known magic byte audio data
    to ensure that these are actually audio files before attempting to extract
    any tag metadata from them.
"""

from typing import Tuple
from unittest import TestCase
from tempfile import mkdtemp
from os.path import join
from os import remove, rmdir


def prune_invalid_audio_files(absolute_audiopath: Tuple[str]) -> Tuple[str]:
    pruned_files = []
    for path in absolute_audiopath:
        with open(path, "rb") as audio_file:
            header_bytes = audio_file.read(4)
            if _is_valid_mp3(header_bytes) or _is_valid_ogg(header_bytes) or _is_valid_flac(header_bytes):
                pruned_files.append(path)

    return tuple(pruned_files)


def _is_valid_mp3(header_bytes: bytes) -> bool:
    return (header_bytes is not None and len(header_bytes) >= 3 and
            (
            header_bytes.startswith(b'ID3') or header_bytes.startswith(b'TAG') or header_bytes.startswith(b'\xff\xfb')))


def _is_valid_ogg(header_bytes: bytes) -> bool:
    return header_bytes is not None and len(header_bytes) >= 4 and header_bytes.startswith(b'Oggs')


def _is_valid_flac(header_bytes: bytes) -> bool:
    return header_bytes is not None and len(header_bytes) >= 4 and header_bytes.startswith(b'fLaC')


"""
    Unittest: AudioFilePrunerTest
    Author: Samuel Vargas

    Creates a temporary directory and populates it with several files
    that contain valid mp3 / flac / ogg file signatures and some that don't.
    The contents of the directory is passed to the function as a tuple and the
    resulting tuple is checked to ensure that only valid media files were included
    in the result.
"""


class AudioFilePrunerTest(TestCase):
    def setUp(self):
        valid_files = ["valid_ID3.mp3", "valid_TAG.mp3", "valid_TAGLESS.mp3", "valid.ogg", "valid.flac"]
        valid_signatures = [b'ID3abcefg', b'TAGaslfa', b'\xff\xfbfoofoo', b'Oggscatdog', b'fLaCPotato']
        invalid_files = ["bad.mp3", "bad.ogg", "bad.flac"]
        invalid_signatures = [b'badID3', b'badOggs', b'badfLaC']

        self.test_files = valid_files + invalid_files
        self.test_signatures = valid_signatures + invalid_signatures
        self.tmp_folder = mkdtemp()
        self.test_files = [join(self.tmp_folder, s) for s in self.test_files]

        for filepath, signature in zip(self.test_files, self.test_signatures):
            with open(filepath, "wb") as temp_file:
                temp_file.write(bytes(signature))

    def test_only_return_valid_audio_files(self):
        valid_audio_files = prune_invalid_audio_files(tuple(self.test_files))
        for filepath in valid_audio_files:
            assert "valid" in filepath

    def tearDown(self):
        for filepath in self.test_files:
            remove(filepath)
        rmdir(self.tmp_folder)


if __name__ == '__main__':
    import unittest

    unittest.main()
