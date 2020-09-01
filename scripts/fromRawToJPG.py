#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
from tqdm import tqdm
from shutil import which


def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""
    return which(name) is not None

def escape_chars(string):
    string = string.replace(' ', '\\ ')
    string = string.replace('(', '\(')
    string = string.replace(')', '\)')
    return string

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="the input directory containing photos")
parser.add_argument("-o", "--output", help="the output directory containing tconverted photos")

args = parser.parse_args()

if args.input is None or args.output is None:
    parser.error("To convert your photos, you need to define an input directory and an output directory")
input_directory = args.input
output_directory = args.output

if is_tool("ufraw-batch"):
    l = []
    if os.path.exists(path=input_directory) and os.path.exists(path=output_directory):
        l = os.listdir(input_directory)
        for raw_path in tqdm(l):
            input_full_path = input_directory + raw_path
            input_full_path = escape_chars(input_full_path)
            os.system("ufraw-batch {} --out-path {} --silent --out-type=jpeg --compression=95 --wb=camera".format(input_full_path, output_directory))

# taux compression 