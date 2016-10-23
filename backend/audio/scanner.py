#!/usr/bin/env python3
"""
    scanner.py
    Author: Samuel Vargas
    Date: 10/12/2016

    The audio.scanner module provides the get_audiofile_list method
    which iterates over a provided directory and returns a list
    of all files that end in a known audio extension (VALID_MEDIA_EXTENSIONS)
"""

from typing import Tuple
from os import walk

# unittest
from tempfile import mkdtemp
from os.path import join, isabs
from os import remove, rmdir
from unittest import TestCase

try:
    from backend.config.constant import VALID_MEDIA_EXTENSIONS
except ImportError:
    VALID_MEDIA_EXTENSIONS = (
        ".mp3", ".ogg", ".flac"
    )


def get_audiofile_list(directory_path: str) -> Tuple[str]:
    if (not isabs(directory_path)):
        raise ValueError
    results = []
    for dirName, _, fileList in walk(directory_path):
        for filepath in fileList:
            if filepath.lower().endswith(VALID_MEDIA_EXTENSIONS):
                results.append(join(dirName, filepath))
    return tuple(results)


"""
    Unittest: LibraryScannerTest
    Author: Samuel Vargas

    Creates a temporary folder and populates it with various empty files,
    some of which have VALID_MEDIA_EXTENSIONS and others that have random
    extensions. It ensures that get_audiofile_list only returns a list of the
    files with those VALID_MEDIA_EXTENSIONS and excludes non audio files.
"""


class LibraryScannerTest(TestCase):
    tmp_folder = None
    test_extensions = None
    tmp_filename = None

    @classmethod
    def setUpClass(cls):
        cls.tmp_folder = mkdtemp()
        cls.tmp_filename = "__uap_libraryscannertest"
        cls.test_extensions = [".odt", ".pdf", ".zip", ".virus", ""]
        cls.test_extensions.extend(list(VALID_MEDIA_EXTENSIONS))
        for ext in cls.test_extensions:
            with open(join(cls.tmp_folder, cls.tmp_filename + ext.upper()), "w") as tmp_file:
                tmp_file.close()

    def test_find_suspected_audio_files(self):
        suspected_media_files = get_audiofile_list(self.tmp_folder)
        for suspect in suspected_media_files:
            assert suspect.lower().endswith(VALID_MEDIA_EXTENSIONS)

    def test_fails_on_relative_path(self):
        with self.assertRaises(ValueError) as _:
            get_audiofile_list(".")

    @classmethod
    def tearDownClass(cls):
        for ext in cls.test_extensions:
            remove(join(cls.tmp_folder, cls.tmp_filename + ext.upper()))
        rmdir(cls.tmp_folder)


if __name__ == '__main__':
    import unittest

    unittest.main()
