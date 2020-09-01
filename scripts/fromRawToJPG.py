#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import tqdm
from shutil import which


def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""
    return which(name) is not None



parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input", help="the input directory containing photos")
parser.add_argument("-o", "--output", help="the output directory containing tconverted photos")

args = parser.parse_args()

if args.input is None or args.output is None:
    parser.error("To convert your photos, you need to define an input directory and an output directory")
input_directory = args.input
output_directory = args.output
print(input_directory,output_directory)

#os.system("ufraw-batch *.CR2 --silent --out-type=jpeg --compression=95 --wb=camera")
# taux compression + 
# input + list dir + exécuter commande fichier par fichier + tqdm
# 
