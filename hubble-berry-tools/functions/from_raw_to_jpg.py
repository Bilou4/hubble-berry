#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from pathlib import Path
from tqdm import tqdm
from shutil import which


def is_tool(name: str) -> bool:
    """Check whether `name` is on PATH and marked as executable."""
    return which(name) is not None


def escape_chars(string: str) -> str:
    string = string.replace(" ", "\\ ")
    string = string.replace("(", "(")
    string = string.replace(")", ")")
    return string


def convert_raw_to_jpg(input_directory: Path, output_directory: Path, compression: int):

    if is_tool("ufraw-batch"):
        files_list = []
        files_list = os.listdir(input_directory)
        for raw_path in tqdm(files_list):
            input_full_path = input_directory + raw_path
            input_full_path = escape_chars(input_full_path)
            os.system(
                "ufraw-batch {} --out-path {} --silent --out-type=jpeg --compression={} --wb=camera".format(
                    input_full_path, output_directory, str(compression)
                )
            )
