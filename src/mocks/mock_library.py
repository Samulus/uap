#!/usr/bin/env python3
#
#   mock_library.py
#   Author: Samuel Vargas
#   Date: 11/08/2016

#   This module works by taking a sample audio file (mp3 / ogg) + a List of
#   dictionaries containing keys / values

import shutil
import taglib
from tempfile import mkdtemp, NamedTemporaryFile
from typing import List, Dict


class MockLibrary:
    def __init__(self, mock_files: List[Dict[str, str]]):
        self.mock_files = mock_files
        self.path = mkdtemp() or None
        self.__enter__()

    def cleanup(self):
        if self.path is not None:
            shutil.rmtree(self.path)

    def __enter__(self):
        for entry in self.mock_files:
            # create dummy mp3 file for taglib
            tmp_file = NamedTemporaryFile(suffix=".mp3", delete=False, dir=self.path)
            tmp_file.write(b'ID3')
            tmp_file.close()

            # open them up in taglib and write the requested tags to each file
            dummy_audio = taglib.File(tmp_file.name)
            for tag_key, tag_value in entry.items():
                dummy_audio.tags[tag_key.upper()] = tag_value
            dummy_audio.save()
            dummy_audio.close()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

