#!/usr/bin/env python3
"""
    taglist.py
    Author: Samuel Vargas
    Date: 10/29/2016

    TODO: taglib.File(file_path).tag.items() is extremely slow,
    it takes about 10-15 seconds on my 26GB library. We should
    either accept this and cache the database or write a faster
    solution loading all of the DESIRED_TAGS from the music
    library.
"""

import taglib
from src import util
from typing import List
import json


class TagList:
    SUPPORTED_EXT = (".mp3", ".ogg", ".flac")
    DESIRED_TAGS = ("title", "artist", "album", "album artist", "year", "tracknumber", "genre")

    def __init__(self, audio_directory="", supported_ext=SUPPORTED_EXT, desired_tags=DESIRED_TAGS):

        self.tags = []

        if audio_directory is None:
            return

        for file_path in util.get_audio_files(audio_directory, supported_ext):
            self.tags.append({})
            for tag_type, tag_value in taglib.File(file_path).tags.items():
                for desired in desired_tags:
                    if tag_type.lower() == desired:
                        self.tags[-1][tag_type.lower()] = tag_value
                self.tags[-1]["filepath"] = file_path

    def load_from_json(self, json_path: str) -> None:
        with open(json_path, "r") as db:
            self.tags = json.loads(db.read())

    def save_as_json(self, save_path: str) -> None:
        with open(save_path, "w") as db:
            db.write(json.dumps(self.tags))

    def get_tags(self):
        return self.tags

    def as_json_str(self):
        return json.dumps(self.tags)

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


if __name__ == '__main__':
    print(TagList("/home/sam/music").search())
