#
#   util.py
#   Author: Samuel Vargas
#   Date: 10/30/2016
#

import os
from typing import Tuple, List


def get_files_with_ext(audio_directory: str, supported_ext: Tuple) -> List[str]:

    """
    Returns a list of relative paths to files in a given audio_directory that end
    with one of the extensions in the supported_ext tuple.

    :param audio_directory: The root folder to begin searching for files. Can be relative or absolute.
    :param supported_ext: A tuple containing desired file extensions e.g. ('.mp3', '.ogg', '.mp4', '.tar.xz').
                          Ensure that you include the leading dot.
    :return: A list of relative paths to files that have the required extension.

    TODO: test this with relative paths
    """
    audio_files = []
    audio_directory = os.path.normpath(audio_directory)
    for dir_name, _, file_list in os.walk(audio_directory):
        for file_path in file_list:
            if file_path.lower().endswith(supported_ext):
                audio_files.append(os.path.relpath(os.path.join(dir_name, file_path), audio_directory))
    return audio_files


def sanitize_input(input: str) -> str:
    pass