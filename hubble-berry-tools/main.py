import functools
import sys

from typing import Callable
import click
from pathlib import Path
from functions.timelapse import make_timelapse
from functions.star_trail import make_star_trail_avg, make_star_trail_max
from functions.download import (
    Action,
    copy_move_pictures_videos_timelapses,
)
from functions.extract_image_from_videos import extract_image_from_video
from functions.from_raw_to_jpg import convert_raw_to_jpg


def input_directory(function: Callable):
    function = click.option(
        "-i",
        "--input",
        type=click.Path(exists=True, dir_okay=True, file_okay=False),
        help="the input directory containing photos",
    )(function)
    return function


def output_directory(function: Callable):
    function = click.option(
        "-o",
        "--output",
        type=click.Path(exists=True, dir_okay=True, file_okay=False),
        help="the output directory containing converted photos",
    )(function)
    return function


def directory_to_retrieve(f: Callable):
    options = [
        click.option(
            "-p",
            "--pictures",
            help="if your demand concerns pictures",
            is_flag=True,
        ),
        click.option(
            "-t",
            "--timelapses",
            help="if your demand concerns timelapses",
            is_flag=True,
        ),
        click.option(
            "-v", "--videos", is_flag=True, help="if your demand concerns videos"
        ),
    ]
    return functools.reduce(lambda x, opt: opt(x), options, f)


@click.group()
def cli():
    """Hubble-Berry will help you interact with your images and your berry-box."""
    pass


@cli.command()
@input_directory
@output_directory
@click.option(
    "--avg",
    is_flag=True,
    help="Method used to create the star trail (default: max).",
)
def star_trail(input: Path, output: Path, avg: bool):
    """Create a Star Trail by averaging or maximizing stars on the final image."""
    if avg:
        make_star_trail_avg(input, output)
    else:
        make_star_trail_max(input, output)


@cli.command()
@input_directory
@output_directory
@click.option(
    "-t",
    "--time",
    help="Time for the duration of a frame in the final video.",
    type=float,
)
@click.option(
    "--mp4",
    is_flag=True,
    help="The format you want for the video (default: avi)",
)
def timelapse(input: Path, output: Path, time: float, mp4: bool):
    """Create a timelapse by merging all images from an input directory."""
    format = "mp4" if mp4 else "avi"
    time_one_im = time
    fps = int(1 / time_one_im)
    make_timelapse(input, output, fps, format)


@cli.command()
@directory_to_retrieve
def copy_images(pictures: bool, timelapses: bool, videos: bool):
    """Retrieve images from your berry-box by copying them."""

    action = Action(0)

    if not pictures and not timelapses and not videos:
        print("You need to specify at least one type of files to copy")
        sys.exit(1)
    else:
        if pictures:
            action = action | Action.COPY_PICTURES
        if timelapses:
            action = action | Action.COPY_TIMELAPSES
        if videos:
            action = action | Action.COPY_VIDEOS
    copy_move_pictures_videos_timelapses(action, pictures, timelapses, videos)


@cli.command()
@directory_to_retrieve
def move_images(pictures: bool, timelapses: bool, videos: bool):
    """Retrieve images from your berry-box by moving them."""

    action = Action(0)

    if not pictures and not timelapses and not videos:
        print("You need to specify at least one type of files to copy")
        sys.exit(1)
    else:
        if pictures:
            action = action | Action.MOVE_PICTURES
        if timelapses:
            action = action | Action.MOVE_TIMELAPSES
        if videos:
            action = action | Action.MOVE_VIDEOS
    copy_move_pictures_videos_timelapses(action, pictures, timelapses, videos)


@cli.command()
@input_directory
@output_directory
@click.option(
    "-c",
    "--compression",
    type=click.IntRange(0, 100),
    default=85,
    help="The compression rate of the jpg image. The compression rate must be between 0 and 100. Higher is the value, better is the quality.",
    show_default=True,
)
def raw_to_jpg(input: Path, output: Path, compression: int):
    """Tool to convert RAW images to JPG."""
    convert_raw_to_jpg(input, output, compression)


@cli.command()
@click.option(
    "-i",
    "--input",
    type=click.Path(dir_okay=False, exists=True, file_okay=True),
    help="the input video",
)
@output_directory
def extract_video_frames(input: Path, output: Path):
    """Extract all images from a video."""
    extract_image_from_video(input, output)


# TODO: linters: bandit-
# TODO: logger for tools
# TODO: test it still works..
