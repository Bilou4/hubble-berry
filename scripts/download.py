#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
from enum import Enum
from paramiko import SSHClient, RSAKey
from scp import SCPClient
from os import environ, remove, path

class Action(Enum):
    COPY_PICTURES = 1
    COPY_TIMELAPSES = 2
    COPY_VIDEOS = 4
    MOVE_PICTURES = 8
    MOVE_TIMELAPSES = 16
    MOVE_VIDEOS = 32


HOME = environ['HOME']
STORAGE_FOLDER = HOME + '/Images/hubble-berry'
PI_COMMON_FOLDER = '/home/pi/Documents/hubble-berry/appFolder/static/camera'

def cp_pictures(scp):
    """cp_pictures allows to copy pictures from the remote server using scp command.

    Args:
        scp (SCPClient): SCPClient object used to get files from the picture directory.
    """
    try:
        scp.get(PI_COMMON_FOLDER + '/pictures/*', STORAGE_FOLDER + '/pictures/')
        remove(STORAGE_FOLDER + '/pictures/do_not_remove.txt')
    except Exception as e:
        print('[cp_pictures]' + str(e))
    
    
def cp_timelapse(scp):
    """cp_timelapse allows to copy pictures from the remote server using scp command.

    Args:
        scp (SCPClient): SCPClient object used to get files from the timelapse directory.
    """
    try:
        scp.get(PI_COMMON_FOLDER + '/timelapse/*', STORAGE_FOLDER + '/timelapse/')
        remove(STORAGE_FOLDER + '/timelapse/do_not_remove.txt')
    except Exception as e:
        print('[cp_timelapse]' + str(e))

def cp_videos(scp):
    """cp_videos allows to copy videos from the remote server using scp command.

    Args:
        scp (SCPClient): SCPClient object used to get files from the video directory.
    """
    try:
        scp.get(PI_COMMON_FOLDER + '/video/*', STORAGE_FOLDER + '/video/')
        remove(STORAGE_FOLDER + '/video/do_not_remove.txt')
    except Exception as e:
        print('[cp_videos]' + str(e))

def move_pictures(scp, ssh):
    """move_pictures allows to move pictures from the remote server using cp_pictures and an ssh connection.

    Args:
        scp (SCPClient): SCPClient object used to call cp function
        ssh (SSHClient): SSHClient object used to execute a command on the remote server
    """
    cp_pictures(scp)
    stdin, stdout, stderr = ssh.exec_command('cd ' + PI_COMMON_FOLDER + '/pictures && find . -type f -not -name "*.txt" -delete')
    if len(stdout.readlines()) > 0:
        print(stdout.readlines()[0])
    if len(stderr.readlines()) > 0:
        print(stderr.readlines()[0])

def move_timelapse(scp, ssh):
    """move_timelapse allows to move pictures from the remote server using cp_timelapse and an ssh connection.

    Args:
        scp (SCPClient): SCPClient object used to call cp function
        ssh (SSHClient): SSHClient object used to execute a command on the remote server
    """
    cp_timelapse(scp)
    stdin, stdout, stderr = ssh.exec_command('cd ' + PI_COMMON_FOLDER + '/timelapse && find . -type f -not -name "*.txt" -delete')
    if len(stdout.readlines()) > 0:
        print(stdout.readlines()[0])
    if len(stderr.readlines()) > 0:
        print(stderr.readlines()[0])

def move_videos(scp, ssh):
    """move_videos allows to move videos from the remote server using cp_videos and an ssh connection.

    Args:
        scp (SCPClient): SCPClient object used to call cp function
        ssh (SSHClient): SSHClient object used to execute a command on the remote server
    """
    cp_videos(scp)
    stdin, stdout, stderr = ssh.exec_command('cd ' + PI_COMMON_FOLDER + '/video && find . -type f -not -name "*.txt" -delete')
    if len(stdout.readlines()) > 0:
        print(stdout.readlines()[0])
    if len(stderr.readlines()) > 0:
        print(stderr.readlines()[0])


parser = argparse.ArgumentParser()

parser.add_argument("-copy", help="If you want to copy files", action="store_true")
parser.add_argument("-move", help="If you want to move files", action="store_true")

parser.add_argument("-p", "--pictures", help="if your demand concerns pictures", action="store_true")
parser.add_argument("-t", "--timelapse", help="if your demand concerns timelapses", action="store_true")
parser.add_argument("-v", "--video", help="if your demand concerns videos", action="store_true")

args = parser.parse_args()
action_performed = False
action = 0

if not path.isdir(HOME):
    raise Exception('Cannot find ' + HOME)

if not path.isdir(STORAGE_FOLDER):
    raise Exception('Cannot find ' + STORAGE_FOLDER)

if not path.isdir(STORAGE_FOLDER + '/pictures') or not path.isdir(STORAGE_FOLDER + '/timelapse') or not path.isdir(STORAGE_FOLDER + '/video'):
    raise Exception('Cannot find ' + STORAGE_FOLDER + '/pictures or /timelapse or /video')

if args.copy:
    if not args.pictures and not args.timelapse and not args.video:
        parser.error("You need to specify at least one type of files to copy")
    else:
        action_performed = True
        if args.pictures:
            action = action | Action.COPY_PICTURES.value
        if args.timelapse:
            action = action | Action.COPY_TIMELAPSES.value
        if args.video:
            action = action | Action.COPY_VIDEOS.value
elif args.move:
    if not args.pictures and not args.timelapse and not args.video:
        parser.error("You need to specify at least one type of files to move")
    else:
        action_performed = True
        if args.pictures:
            action = action | Action.MOVE_PICTURES.value
        if args.timelapse:
            action = action | Action.MOVE_TIMELAPSES.value
        if args.video:
            action = action | Action.MOVE_VIDEOS.value
        
if not action_performed:
    parser.error("You need to choose an action to perform, either copy or move files.")
else:
    ssh = SSHClient()
    ssh.load_system_host_keys()
    k = RSAKey.from_private_key_file(HOME + '/.ssh/id_rsa')
    
    try:
        ssh.connect(hostname='10.3.141.1', 
            username='pi',
            pkey=k)
        print("[\033[0;32m OK\033[0m ] CONNECTED")

        scp = SCPClient(ssh.get_transport(), sanitize=lambda x: x) # sanitize allows to use wildcards in command line
        if action & Action.COPY_PICTURES.value:
            cp_pictures(scp)
            print('[\033[0;32m OK\033[0m ] pictures copied')
        if action & Action.COPY_TIMELAPSES.value:
            cp_timelapse(scp)
            print('[\033[0;32m OK\033[0m ] timelapse copied')
        if action & Action.COPY_VIDEOS.value:
            cp_videos(scp)
            print('[\033[0;32m OK\033[0m ] videos copied')
        if action & Action.MOVE_PICTURES.value:
            move_pictures(scp, ssh)
            print('[\033[0;32m OK\033[0m ] pictures moved')
        if action & Action.MOVE_TIMELAPSES.value:
            move_timelapse(scp, ssh)
            print('[\033[0;32m OK\033[0m ] timelapse moved')
        if action & Action.MOVE_VIDEOS.value:
            move_videos(scp, ssh)
            print('[\033[0;32m OK\033[0m ] video moved')

    except Exception as e:
        print(e)
    
    finally:
        scp.close()
        ssh.close()
