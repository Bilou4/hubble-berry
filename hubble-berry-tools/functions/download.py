#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flags import Flags
from paramiko import SSHClient, RSAKey
from scp import SCPClient
from os import environ, remove
from pathlib import Path


class Action(Flags):
    DO_NOTHING = 0
    COPY_PICTURES = 1
    COPY_TIMELAPSES = 2
    COPY_VIDEOS = 4
    MOVE_PICTURES = 8
    MOVE_TIMELAPSES = 16
    MOVE_VIDEOS = 32


HOME = Path(environ["HOME"])
STORAGE_FOLDER = HOME / Path("Images/hubble-berry")
PI_COMMON_FOLDER = Path(
    "/home/pi/Documents/production/hubble-berry/appFolder/static/camera"
)


def copy_move_pictures_videos_timelapses(
    action: int, pictures: bool, timelapses: bool, videos: bool
):
    if not HOME.is_dir():
        raise Exception(f"Cannot find {HOME}")

    if not STORAGE_FOLDER.is_dir():
        raise Exception(f"Cannot find  {STORAGE_FOLDER}")

    if (
        not (STORAGE_FOLDER / "pictures").is_dir()
        or not (STORAGE_FOLDER / "timelapse").is_dir()
        or not (STORAGE_FOLDER / "video").is_dir()
    ):
        raise Exception(
            f"Cannot find {STORAGE_FOLDER} /pictures or /timelapse or /video"
        )

    ssh = SSHClient()
    ssh.load_system_host_keys()
    k = RSAKey.from_private_key_file(str(HOME / ".ssh/id_rsa"))

    try:
        ssh.connect(hostname="10.3.141.1", username="pi", pkey=k)
        print("CONNECTED")

        scp = SCPClient(
            ssh.get_transport(), sanitize=lambda x: x
        )  # sanitize allows to use wildcards in command line
        if action & Action.COPY_PICTURES:
            cp_pictures(scp)
            print("pictures copied")
        if action & Action.COPY_TIMELAPSES:
            cp_timelapse(scp)
            print("timelapse copied")
        if action & Action.COPY_VIDEOS:
            cp_videos(scp)
            print("videos copied")
        if action & Action.MOVE_PICTURES:
            move_pictures(scp, ssh)
            print("pictures moved")
        if action & Action.MOVE_TIMELAPSES:
            move_timelapse(scp, ssh)
            print("timelapse moved")
        if action & Action.MOVE_VIDEOS:
            move_videos(scp, ssh)
            print("video moved")

    except Exception as e:
        print(e)

    finally:
        scp.close()
        ssh.close()


def cp_pictures(scp: SCPClient) -> None:
    """cp_pictures allows to copy pictures from the remote server using scp command.

    Args:
        scp (SCPClient): SCPClient object used to get files from the picture directory.
    """
    try:
        scp.get(PI_COMMON_FOLDER / "pictures/*", STORAGE_FOLDER / "pictures/")
        remove(STORAGE_FOLDER / "pictures/do_not_remove.txt")
    except Exception as e:
        print("[cp_pictures]" + str(e))


def cp_timelapse(scp: SCPClient) -> None:
    """cp_timelapse allows to copy pictures from the remote server using scp command.

    Args:
        scp (SCPClient): SCPClient object used to get files from the timelapse directory.
    """
    try:
        scp.get(PI_COMMON_FOLDER / "timelapse", STORAGE_FOLDER)
        remove(STORAGE_FOLDER / "timelapse/do_not_remove.txt")
    except Exception as e:
        print("[cp_timelapse]" + str(e))


def cp_videos(scp: SCPClient) -> None:
    """cp_videos allows to copy videos from the remote server using scp command.

    Args:
        scp (SCPClient): SCPClient object used to get files from the video directory.
    """
    try:
        scp.get(PI_COMMON_FOLDER / "video", STORAGE_FOLDER)
        remove(STORAGE_FOLDER / "video/do_not_remove.txt")
    except Exception as e:
        print("[cp_videos]" + str(e))


def move_pictures(scp: SCPClient, ssh: SSHClient) -> None:
    """move_pictures allows to move pictures from the remote server using cp_pictures and an ssh connection.

    Args:
        scp (SCPClient): SCPClient object used to call cp function
        ssh (SSHClient): SSHClient object used to execute a command on the remote server
    """
    cp_pictures(scp)
    stdin, stdout, stderr = ssh.exec_command(
        "cd "
        + str(PI_COMMON_FOLDER / "pictures")
        + " && find . -type f -not -name '*.txt' -delete"
    )
    if len(stdout.readlines()) > 0:
        print(stdout.readlines()[0])
    if len(stderr.readlines()) > 0:
        print(stderr.readlines()[0])


def move_timelapse(scp: SCPClient, ssh: SSHClient) -> None:
    """move_timelapse allows to move pictures from the remote server using cp_timelapse and an ssh connection.

    Args:
        scp (SCPClient): SCPClient object used to call cp function
        ssh (SSHClient): SSHClient object used to execute a command on the remote server
    """
    cp_timelapse(scp)
    stdin, stdout, stderr = ssh.exec_command(
        "cd "
        + str(PI_COMMON_FOLDER / "timelapse")
        + " && find . -type f -not -name '*.txt' -delete"
    )
    if len(stdout.readlines()) > 0:
        print(stdout.readlines()[0])
    if len(stderr.readlines()) > 0:
        print(stderr.readlines()[0])


def move_videos(scp: SCPClient, ssh: SSHClient) -> None:
    """move_videos allows to move videos from the remote server using cp_videos and an ssh connection.

    Args:
        scp (SCPClient): SCPClient object used to call cp function
        ssh (SSHClient): SSHClient object used to execute a command on the remote server
    """
    cp_videos(scp)
    stdin, stdout, stderr = ssh.exec_command(
        "cd "
        + str(PI_COMMON_FOLDER / "video")
        + " && find . -type f -not -name '*.txt' -delete"
    )
    if len(stdout.readlines()) > 0:
        print(stdout.readlines()[0])
    if len(stderr.readlines()) > 0:
        print(stderr.readlines()[0])
