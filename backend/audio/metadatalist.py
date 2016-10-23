#!/usr/bin/env python3
"""
    metadatalist.py
    Author: Samuel Vargas

    This module is responsible for accepting a list of absolute paths to
    audio files and generating a corresponding list of dictionary objects containing
    specific audio metadata (TITLE, ALBUM ARTIST, ARTIST, ALBUM, YEAR, GENRE)
    for each audio file. If that particular metadata is missing from
    the file it will not be present in the dictionary object for that file.
"""

import taglib
from typing import List


def generate_taglist(audio_filepaths: List[str]):
   taglist = []
   for filepath in audio_filepaths:
      tags = taglib.File(filepath).tags
      pruned_tags = {}
      if "TITLE" in tags:
         pruned_tags["title"] = tags["TITLE"]
      if "ARTIST" in tags:
         pruned_tags["artist"] = tags["ARTIST"]
      if "ALBUM ARTIST" in tags:
         pruned_tags["album artist"] = tags["ALBUM ARTIST"]
      if "ALBUM" in tags:
         pruned_tags["album"] = tags["ALBUM"]
      if "YEAR" in tags:
         pruned_tags["year"] = tags["YEAR"]
      if "TRACKNUMBER" in tags:
         pruned_tags["tracknumber"] = tags["TRACKNUMBER"]
      if "GENRE" in tags:
         pruned_tags["genre"] = tags["GENRE"]
      taglist.append(pruned_tags)

   return taglist


if __name__ == '__main__':
   pass
