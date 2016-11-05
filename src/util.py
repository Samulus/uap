#
#   util.py
#   Author: Samuel Vargas
#   Date: 10/30/2016
#

import os
from typing import Tuple, List


def get_audio_files(audio_directory: str, supported_ext: Tuple) -> List[str]:
    audio_files = []

    if not os.path.isabs(audio_directory):
        raise ValueError("'{0}' is not an absolute path to an audio_directory".format(audio_directory))

    for dir_name, _, file_list in os.walk(audio_directory):
        for file_path in file_list:
            if file_path.lower().endswith(supported_ext):
                audio_files.append(os.path.join(dir_name, file_path))
    return audio_files
