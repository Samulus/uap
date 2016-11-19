#!/usr/bin/env python3
#
#   taglist.py
#   Author: Samuel Vargas
#   Date: 10/29/2016
#
#   The taglist module accepts a path to a folder and uses os.walk + Mutagen
#   to dynamically load all of the multimedia files that contain a supported
#   media file extension ('.mp3', '.flac', '.ogg') etc.

#   Note that the TinyDB / offline saving functionality has been temporarily
#   removed because writing an entire library to a json file is too slow.
#   (I don't know what I expected). I'll be mitigating it to dataset (sqlite3
#   wrapper) in the future.

from collections import OrderedDict
from os.path import realpath, join
from typing import List, Tuple
import os
import mutagen


def get_files_with_ext(audio_folder: str, supported_ext: Tuple) -> List[str]:
    """
    Returns a list of relative paths to files in a given audio_directory
    that end with one of the extensions in the supported_ext tuple.

    :param audio_folder: The root folder to begin searching for files.
                            Can be relative or absolute.
    :param supported_ext:   A tuple containing desired file extensions
                            e.g. ('.mp3', '.ogg', '.mp4', '.tar.xz').
                            Ensure that you include the leading dot when
                            specifying the extension type.

    :return: A list of relative paths to files that have this extension.

    """
    audio_files = []
    audio_folder = os.path.normpath(audio_folder)
    for dir_name, _, file_list in os.walk(audio_folder):
        for file_path in file_list:
            if file_path.lower().endswith(supported_ext):
                audio_files.append(
                    os.path.relpath(os.path.join(dir_name, file_path),
                                    audio_folder))
    return audio_files


class TagList:
    DB_PATH = realpath(join(__file__, "..", "database/taglist.json"))
    SUPPORTED_EXT = (".mp3", ".ogg", ".flac")
    DESIRED_TAGS = ("title", "artist", "album", "album artist",
                    "year", "tracknumber", "genre")

    def __init__(self, audio_folder: str, ram_db=False):
        self.linear = []
        self.hierarchy = OrderedDict()
        self.audio_folder = audio_folder

        if not audio_folder:
            raise ValueError("You must specify a directory to parse"
                             "audio files from.")

        if ram_db:
            self.__database = TinyDB(storage=MemoryStorage)
        else:
            self.__database = TinyDB(TagList.DB_PATH)

        self.load_from_directory(audio_folder)

    def load_from_directory(self, audio_folder: str):
        """
        Accepts a path to an audio_folder and then constructs a linear
        list of dicts and an OrderedDict in a hierarchy format in
        self.linear and self.hierarchy

        :param audio_folder: An absolute or relative path to a music
                             directory.
        """

        # ghetto: purge the table before reloading the database
        # back into the memory object.
        self.__database.purge_table('_default')

        # generate a list of tags
        for filepath in get_files_with_ext(audio_folder, self.SUPPORTED_EXT):
            self.linear.append({})
            audiofile = None
            try:
                audiofile = mutagen.File(os.path.join(audio_folder, filepath),
                                         easy=True)
            except mutagen.mp3.HeaderNotFoundError:
                audiofile = None

            if audiofile is None:
                continue

            for key, value in audiofile.items():
                # copy all of the desired tags from the file into the tag
                for desired in TagList.DESIRED_TAGS:
                    if key.lower() == desired:
                        self.linear[-1][key.lower()] = value
                # record the relative filepath for this audiofile
                self.linear[-1]["filepath"] = filepath

        for tag in self.linear:
            artist = tag["artist"][0] if "artist" in tag else None
            album = tag["album"][0] if "album" in tag else None
            title = tag["title"][0] if "title" in tag else None
            tags_to_omit_per_file = ("artist", "album", "title")

            # add {'artist' : {}} if not found yet
            if artist and artist not in self.hierarchy:
                self.hierarchy[artist] = OrderedDict()

            # add {'artist': {'album': {}}}
            if artist and artist in self.hierarchy and \
               album and album not in self.hierarchy[artist]:
                self.hierarchy[artist][album] = OrderedDict()

            # add {'artist': {'album': {'track 1': {}}}}
            if artist and artist in self.hierarchy and \
               album and album in self.hierarchy[artist] and \
               title and title not in self.hierarchy[artist][album]:
                    self.hierarchy[artist][album][title] = \
                        {tag_type: tag_value
                         for tag_type, tag_value in tag.items()
                         if tag_type not in tags_to_omit_per_file}

    def search(self, artist=None, album=None, title=None) -> List[str]:
        results = []

        hits_needed = 1 if artist is not None else 0
        hits_needed += 1 if album is not None else 0
        hits_needed += 1 if title is not None else 0

        for tag in self.linear:
            hits = 0
            for tag_key, tag_value in tag.items():
                if artist is not None and tag_key == "artist" and \
                   artist.lower() in tag_value[0].lower():
                    hits += 1
                if album is not None and tag_key == "album" and \
                   album.lower() in tag_value[0].lower():
                    hits += 1
                if title is not None and tag_key == "title" and \
                   title.lower() in tag_value[0].lower():
                    hits += 1
            if hits == hits_needed:
                results.append(tag)

        return results

    def get_absolute_song_path(self, song_path):
        results = self.__database.search(Query().filepath == song_path)
        assert len(results) < 2, \
            "Two songs should not have the same filepath."
        if len(results) == 1:
            return join(self.audio_folder, results[0]['filepath'])
        return None
