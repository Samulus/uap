#!/usr/bin/env python3
"""
    metadatalist.py
    Author: Samuel Vargas

    Given a list of known audio files this module will generate a list of
    dictionary objects containing tag information computed by taglib +
    the path it was found in.
"""

import taglib

def generate_taglist(audio_filepaths):
    taglist = []
    for filepath in audio_filepaths:
        taglist.append(taglib.File(filepath).tags)
        taglist[-1]["FILEPATH"] = filepath

    return taglist

if __name__ == '__main__':
    from backend.audio.scanner import get_audiofile_list
    from backend.audio.pruner import prune_invalid_audio_files
    audio_files = generate_taglist(prune_invalid_audio_files(get_audiofile_list("/home/sam/music/")))
