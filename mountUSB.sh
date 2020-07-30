#!/bin/bash

if [[ $# -ne 1 ]]; then
	echo "Illegal number of parameters"
	exit 2
fi
if [[ $1 = "mount" ]]; then
	sudo mount /dev/sda1 /media/pi/HUBBLE_SAVE/ -o uid=pi,gid=pi
	echo "mounted"
else
	if [[ $1 = "umount" ]]; then
		sudo umount /media/pi/HUBBLE_SAVE/
		echo "unmounted"
	else
		echo "only available options are mount or umount"
	fi
fi
