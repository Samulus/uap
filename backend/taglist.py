#!/usr/bin/env python3
"""
    taglist.py
    Author: Samuel Vargas
    Date: 10/29/2016
"""

import taglib
from typing import List, Tuple
from os import walk
from os.path import isabs, join


class TagList:
    SUPPORTED_EXT = (".mp3", ".ogg", ".flac")
    DESIRED_TAGS = ("title", "artist", "album", "album artist", "year", "tracknumber", "genre")

    def __init__(self, audio_directory: str, supported_ext=SUPPORTED_EXT, desired_tags=DESIRED_TAGS):
        self.tags = []

        for file_path in self.__get_audio_files(audio_directory, supported_ext):
            self.tags.append({})
            for tag_type, tag_value in taglib.File(file_path).tags.items():
                for desired in desired_tags:
                    if tag_type.lower() == desired:
                        self.tags[-1][tag_type.lower()] = tag_value

    def search(self, artist=None, album=None, title=None) -> List[str]:
        results = []

        hits_needed = 1 if artist is not None else 0
        hits_needed += 1 if album is not None else 0
        hits_needed += 1 if title is not None else 0

        for tag in self.tags:
            hits = 0
            for tag_key, tag_value in tag.items():
                if artist is not None and tag_key == "artist" and artist in tag_value[0]:
                    hits += 1
                if album is not None and tag_key == "album" and album in tag_value[0]:
                    hits += 1
                if title is not None and tag_key == "title" and title in tag_value[0]:
                    hits += 1
            if hits == hits_needed:
                results.append(tag)
        return results

    @staticmethod
    def __get_audio_files(audio_directory: str, supported_ext: Tuple) -> List[str]:
        audio_files = []

        if not isabs(audio_directory):
            raise ValueError("'{0}' is not an absolute path to an audio_directory".format(audio_directory))

        for dir_name, _, file_list in walk(audio_directory):
            for file_path in file_list:
                if file_path.lower().endswith(supported_ext):
                    audio_files.append(join(dir_name, file_path))
        return audio_files
