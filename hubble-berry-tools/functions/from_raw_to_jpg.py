#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from tqdm import tqdm
from shutil import which


def is_tool(name: str) -> bool:
    """Check whether `name` is on PATH and marked as executable."""
    return which(name) is not None


def escape_chars(string: str) -> str:
    string = string.replace(" ", "\\ ")
    string = string.replace("(", "\(")
    string = string.replace(")", "\)")
    return string


def convert_raw_to_jpg(input_directory, output_directory, compression):

    if os.path.isdir(input_directory) and os.path.isdir(output_directory):
        if input_directory[-1] != "/":
            input_directory = input_directory + "/"
        if output_directory[-1] != "/":
            output_directory = output_directory + "/"
    else:
        raise Exception("Either the input or ouput argument is not a directory")

    if is_tool("ufraw-batch"):
        l = []
        l = os.listdir(input_directory)
        for raw_path in tqdm(l):
            input_full_path = input_directory + raw_path
            input_full_path = escape_chars(input_full_path)
            os.system(
                "ufraw-batch {} --out-path {} --silent --out-type=jpeg --compression={} --wb=camera".format(
                    input_full_path, output_directory, str(compression)
                )
            )
