#!/bin/bash

for file in /home/pi/Videos/*.h264 ; do
	fname=$(basename "$file")
        name=${fname%.h264}
	MP4Box -add "/home/pi/Videos/"$name.h264 "/home/pi/Videos/"$name.mp4
	rm "/home/pi/Videos/"$name.h264

done
