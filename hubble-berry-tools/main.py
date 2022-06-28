import functools
import sys
from typing import Callable
import click
from functions.timelapse import make_timelapse
from functions.star_trail import make_star_trail_avg, make_star_trail_max
from functions.download import (
    Action,
    copy_move_pictures_videos_timelapses,
)
from functions.extract_image_from_videos import extract_image_from_video
from functions.from_raw_to_jpg import convert_raw_to_jpg


def input_output(f: Callable):
    options = [
        click.option("-i", "--input", help="the input directory containing photos"),
        click.option(
            "-o", "--output", help="the output directory containing converted photos"
        ),
    ]

    return functools.reduce(lambda x, opt: opt(x), options, f)


def directory_to_retrieve(f: Callable):
    options = [
        click.option(
            "-p",
            "--pictures",
            help="if your demand concerns pictures",
            action="store_true",
        ),
        click.option(
            "-t",
            "--timelapse",
            help="if your demand concerns timelapses",
            action="store_true",
        ),
        click.option(
            "-v", "--video", help="if your demand concerns videos", action="store_true"
        ),
    ]
    return functools.reduce(lambda x, opt: opt(x), options, f)


@click.group()
def cli():
    click.secho("Hello")


@cli.command()
@input_output
@click.option(
    "--avg",
    is_flag=True,
    help="method used to create the star trail (default: max)",
)
def star_trail(input, output, avg: bool):
    if avg:
        click.secho("avg set")
        make_star_trail_avg(input, output)
    else:
        make_star_trail_max(input, output)
    click.secho("star trail")


@cli.command()
@input_output
@click.option(
    "-t",
    "--time",
    help="time for the duration of a frame in the final video",
    type=float,
)
@click.option(
    "--mp4",
    is_flag=True,
    help="The format you want for the video (default: avi)",
)
def timelapse(input, output, time, mp4):
    format = "mp4" if mp4 else "avi"
    time_one_im = time
    fps = 1 / time_one_im  # may need a cast to int
    make_timelapse(input, output, fps, format)

    click.secho("timelapse")


@cli.command()
@click.option("-p", "--pictures", is_flag=True, help="if your demand concerns pictures")
@click.option(
    "-t", "--timelapses", is_flag=True, help="if your demand concerns timelapses"
)
@click.option("-v", "--videos", is_flag=True, help="if your demand concerns videos")
def copy_images(pictures: bool, timelapses: bool, videos: bool):
    """If you want to copy files"""
    click.secho("copy_images")

    if not pictures and not timelapses and not videos:
        print("You need to specify at least one type of files to copy")
        sys.exit(1)
    else:
        if pictures:
            action = action | Action.COPY_PICTURES.value
        if timelapses:
            action = action | Action.COPY_TIMELAPSES.value
        if videos:
            action = action | Action.COPY_VIDEOS.value
    copy_move_pictures_videos_timelapses(pictures, timelapses, videos)


@cli.command()
@click.option("-p", "--pictures", is_flag=True, help="if your demand concerns pictures")
@click.option(
    "-t", "--timelapses", is_flag=True, help="if your demand concerns timelapses"
)
@click.option("-v", "--videos", is_flag=True, help="if your demand concerns videos")
def move_images(pictures: bool, timelapses: bool, videos: bool):
    """If you want to move files"""
    click.secho("move_images")
    if not pictures and not timelapses and not videos:
        print("You need to specify at least one type of files to copy")
        sys.exit(1)
    else:
        if pictures:
            action = action | Action.MOVE_PICTURES.value
        if timelapses:
            action = action | Action.MOVE_TIMELAPSES.value
        if videos:
            action = action | Action.MOVE_VIDEOS.value
    copy_move_pictures_videos_timelapses(pictures, timelapses, videos)


@cli.command()
@input_output
@click.option(
    "-c",
    "--compression",
    type=click.IntRange(0, 100),
    default=85,
    help="the compression rate of the jpg image. The compression rate must be between 0 and 100. Higher is the value, better is the quality.",
    show_default=True,
)
def raw_to_jpg(input, output, compression: int):

    if input is None or output is None:
        print(
            "To convert your photos, you need to define an input directory and an output directory"
        )
    convert_raw_to_jpg(input, output, compression)
    click.secho("raw_to_jpg")


@cli.command()
@click.option("-i", "--input", help="the input video")
@click.option("-o", "--output", help="the output directory containing extracted photos")
def extract_video_frames(input, output):
    click.secho("extract_video_frames")
    extract_image_from_video(input, output)
