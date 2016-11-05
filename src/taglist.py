#!/usr/bin/env python3
#
#   taglist.py
#   Author: Samuel Vargas
#   Date: 10/29/2016
#
#   TODO: taglib.File(file_path).tag.items() is extremely slow,
#   it takes about 10-15 seconds on my 26GB library. We should
#   either accept this and cache the database or write a faster
#   solution loading all of the DESIRED_TAGS from the music
#   library.
#
#   TODO: The module is including the absolute path that the music file
#   was found at as part of the "filepath" key but this is a security risk
#   and extraneous information that can be recalculated server side anyway.
#   Modify the __construct_tag_list method to only include relative paths
#   in its output.


import json
import taglib
from collections import OrderedDict
from typing import List

from src import util


class TagList:
    SUPPORTED_EXT = (".mp3", ".ogg", ".flac")
    DESIRED_TAGS = ("title", "artist", "album", "album artist",
                    "year", "tracknumber", "genre")

    def __init__(self, audio_directory=None, use_json_path=None):
        self.tag_list = []
        self.tag_hierarchy = OrderedDict()

        # raise exception if parameters are used incorrectly
        if (audio_directory is None and use_json_path is None or
                        audio_directory is not None and use_json_path is not None):
            raise ValueError("taglist.py: Specify an audio directory OR a json tag file")

        # use path to offline json file instead of reloading audio files from directory
        if use_json_path is not None:
            with open(use_json_path, "r") as json_file:
                self.tag_list = json.loads(json_file.read())
                self.__construct_tag_hierarchy()
                return

        # build tag_list + tag_hierarchy for search and library api requests respectively
        self.__construct_tag_list(audio_directory)
        self.__construct_tag_hierarchy()

    def __construct_tag_list(self, audio_directory) -> None:
        for file_path in util.get_audio_files(audio_directory, TagList.SUPPORTED_EXT):
            self.tag_list.append({})
            for tag_type, tag_value in taglib.File(file_path).tags.items():
                for desired in TagList.DESIRED_TAGS:
                    if tag_type.lower() == desired:
                        self.tag_list[-1][tag_type.lower()] = tag_value
                self.tag_list[-1]["filepath"] = file_path

    # TODO: this function does not support audio files missing an (artist, album, title)
    def __construct_tag_hierarchy(self) -> None:
        for tag in self.tag_list:
            artist = tag["artist"][0] if "artist" in tag else None
            album = tag["album"][0] if "album" in tag else None
            title = tag["title"][0] if "title" in tag else None
            tags_to_omit_per_file = ("artist", "album", "title")

            # add root level artist tag to hierarchy
            if artist not in self.tag_hierarchy:
                self.tag_hierarchy[artist] = OrderedDict()

            # add album tag to existing artist
            if artist in self.tag_hierarchy and album not in self.tag_hierarchy[artist]:
                self.tag_hierarchy[artist][album] = OrderedDict()

            # add title tag to existing album
            if artist in self.tag_hierarchy and album in self.tag_hierarchy[artist] and title not in \
                    self.tag_hierarchy[artist][album]:
                self.tag_hierarchy[artist][album][title] = {tag_type: tag_value for tag_type, tag_value in tag.items()
                                                            if tag_type not in tags_to_omit_per_file}

    def search(self, artist=None, album=None, title=None) -> List[str]:
        results = []

        hits_needed = 1 if artist is not None else 0
        hits_needed += 1 if album is not None else 0
        hits_needed += 1 if title is not None else 0

        for tag in self.tag_list:
            hits = 0
            for tag_key, tag_value in tag.items():
                if artist is not None and tag_key == "artist" and artist.lower() in tag_value[0].lower():
                    hits += 1
                if album is not None and tag_key == "album" and album.lower() in tag_value[0].lower():
                    hits += 1
                if title is not None and tag_key == "title" and title.lower() in tag_value[0].lower():
                    hits += 1
            if hits == hits_needed:
                results.append(tag)

        return results
