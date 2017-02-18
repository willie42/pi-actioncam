# pi-actioncam
code to make a rasperrypi with connected cam act as an actioncam

This was my first programming project after a very long time
and the first in python - so for sure this is no clean code - but it works for me

onnect LED to GPIO 18 (pin 12) and ground (pin 6)
connect Button GPIO 17 (pin 11) and ground (pin 9)
Ports may differ on type of raspberry you use!
I used a pi-zero.

INSTALL:

copy actioncam.py and videoconvert.sh to home/pi
make executable 
make shure, /home/pi/Pitures and /home/pi/Videos do exist
to run on startup add "python /home/pi/actioncam.py" in /ect/rc.local


MANUAL:

** VIDEO

press short (< 2 s) to start video-record - LED will blink 
press again to stop recording

** STILLS

press longer (< 5 s) to start timelapse photos - LED will go out an blink every 3 seconds
press again, release as soon as LED is constantly on to stop recording pictures

** SHUTDOWN

press longer than 5 seconds to shutdown raspi
