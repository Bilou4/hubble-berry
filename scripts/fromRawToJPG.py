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
parser.add_argument("-c", "--compression", type=int, default=85, help="the compression rate of the jpg image (default: 85)")

args = parser.parse_args()

if args.input is None or args.output is None:
    parser.error("To convert your photos, you need to define an input directory and an output directory")
if args.compression < 0 or args.compression > 100:
    parser.error("The compression rate must be between 0 and 100. Higher is the value, better is the quality.")

input_directory = args.input
output_directory = args.output

if os.path.isdir(input_directory) and os.path.isdir(output_directory):
    if input_directory[-1] != '/':
        input_directory = input_directory + '/'
    if output_directory[-1] != '/':
        output_directory = output_directory + '/'
else:
    raise Exception("Either the input or ouput argument is not a directory")

if is_tool("ufraw-batch"):
    l = []
    l = os.listdir(input_directory)
    for raw_path in tqdm(l):
        input_full_path = input_directory + raw_path
        input_full_path = escape_chars(input_full_path)
        os.system("ufraw-batch {} --out-path {} --silent --out-type=jpeg --compression={} --wb=camera"
                .format(input_full_path, output_directory, str(args.compression)))

