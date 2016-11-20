#!/usr/bin/env python3
#
#   taglist.py
#   Author: Samuel Vargas
#   Date: 10/29/2016
#
#   The taglist module accepts a path to a folder and uses os.walk + Mutagen
#   to dynamically load all of the multimedia files that contain a supported
#   media file extension ('.mp3', '.flac', '.ogg') etc. It then stores those
#   into two instance variables and consists of methods to search them.

#   An instance of this class is then used in the Server module every time the
#   user requests an audio file (to verify that file actually exists) or to
#   search for audio files that contain tags the users are searching for.

#   Finally the self.linear_song_list and self.hierarchy_song_dict attributes
#   can be used to iterate through the entire library or to browse by
#   using a dict with a structure like: {"artist": "album": {"track" : {}}}

#   NOTE: TinyDB / offline saving functionality has been temporarily
#   removed because writing an entire library to a json file is too slow.
#   (I don't know what I expected). I'll be mitigating it to dataset (sqlite3
#   wrapper) in the future. In the mean time this means that your entire music
#   library will be reloaded every time. Mutagen is generally pretty fast
#   though so it should not be much of a problem.

from collections import OrderedDict
from os.path import realpath, join, normpath
from typing import Dict, List, Tuple

import os
import sys
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
    SUPPORTED_EXT = (".mp3", ".ogg", ".flac")
    DESIRED_TAGS = ("title", "artist", "album", "album artist",
                    "year", "tracknumber", "genre")

    def __init__(self, audio_folder: str):
        """
        Create a new instance of a TagList

        :param audio_folder: The music folder to parse audio files from.
        """
        self.linear_song_list = []
        self.hierarchy_song_dict = OrderedDict()
        self.audio_folder = audio_folder

        if not audio_folder:
            raise ValueError("You must specify a folder to parse"
                             "audio files from.\n"
                             "Remember to modify config.ini and add your "
                             "music folder.")

        self.load_from_directory(audio_folder)

    def load_from_directory(self, audio_folder: str):
        """
        Accepts a path to an audio_folder and then constructs a linear
        list of dicts and an OrderedDict in a hierarchy format in
        self.linear and self.hierarchy

        :param audio_folder: An absolute or relative path to a music
                             directory.
        """

        # generate a list of tags
        for filepath in get_files_with_ext(audio_folder, self.SUPPORTED_EXT):
            self.linear_song_list.append({})
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
                        self.linear_song_list[-1][key.lower()] = value
                # record the relative filepath for this audiofile
                self.linear_song_list[-1]["filepath"] = filepath

        for tag in self.linear_song_list:
            artist = tag["artist"][0] if "artist" in tag else None
            album = tag["album"][0] if "album" in tag else None
            title = tag["title"][0] if "title" in tag else None
            tags_to_omit_per_file = ("artist", "album", "title")

            # add {'artist' : {}} if not found yet
            if artist and artist not in self.hierarchy_song_dict:
                self.hierarchy_song_dict[artist] = OrderedDict()

            # add {'artist': {'album': {}}}
            if artist and artist in self.hierarchy_song_dict and \
                    album and album not in self.hierarchy_song_dict[artist]:
                self.hierarchy_song_dict[artist][album] = OrderedDict()

            # add {'artist': {'album': {'track 1': {}}}}
            if artist and artist in self.hierarchy_song_dict and \
                    album and album in self.hierarchy_song_dict[artist] and \
                    title and title not in \
                    self.hierarchy_song_dict[artist][album]:
                self.hierarchy_song_dict[artist][album][title] = \
                    {tag_type: tag_value
                     for tag_type, tag_value in tag.items()
                     if tag_type not in tags_to_omit_per_file}

    def search(self, artist=None, album=None, title=None) -> List[Dict]:
        """
        Searches the taglist for audio files that contain (substring search)
        the specified tags. The type of search performed is a logical AND,
        meaning that if call this function with search(artist="Death", album=
        "Money") it will only return results that match the artist AND album.

        :TODO: Eventually modify this function so that it accepts **kwargs
               so that you can search for any tag and not just the current
               three.

        :param artist: The artist to search for
        :param album: The album to search for
        :param title: The title to search for
        :return: A list containing results, an empty list if no results
                 are found.
        """
        results = []

        hits_needed = 1 if artist is not None else 0
        hits_needed += 1 if album is not None else 0
        hits_needed += 1 if title is not None else 0

        for tag in self.linear_song_list:
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

    def is_song_path_in_taglist(self, song_path: str) -> bool:
        """
        Check to see if a song_path has a corresponding song_path in the
        taglist. Use this function to validate user input when they request
        a song. It will prevent them from downloading any random file in
        the music folder.

        :param song_path: Relative path to an audio file in the music folder
                          to validate.
        :return: True if the song_path corresponds to a valid audio file,
                 False otherwise.
        """
        for song in self.linear_song_list:
            if 'filepath' in song and song['filepath'] == normpath(song_path):
                return True
        return False
