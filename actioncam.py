## Raspberry ActionCam with one Button and one LED
## Python 3 with gpiozero
##
## ver 0.3 
##
## gpac used for video conversion (sudo apt-get install gpac)
##
## by Willie Beckmann
## 12.2016 - CC-BY-NC
##
## no support, no warranty!
##
## This was my first programming project after a very long time
## and the first in python - so for sure this is no clean code - but it works for me
##
##
## connect LED to GPIO 18 (pin 12) and ground (pin 6)
## connect Button GPIO 17 (pin 11) and ground (pin 9)
## Ports may differ on type of raspberry you use!
## I used a pi-zero.
##
## INSTALL:
##
## copy actioncam.py and videoconvert.sh to home/pi
## make executable 
## make shure, /home/pi/Pitures and /home/pi/Videos do exist
## to run on startup add "python /home/pi/actioncam.py" in /ect/rc.local
##
## MANUAL:
##
## VIDEO
## press short (< 2 s) to start video-record - LED will blink 
## press again to stop recording
##
## STILLS
## press longer (< 5 s) to start timelapse photos - LED will go out an blink every 3 seconds
## press again, release as soon as LED is constantly on to stop recording pictures
##
## SHUTDOWN
## press longer than 5 seconds to shutdown raspi


from picamera import PiCamera
from time import sleep
from time import time
from gpiozero import LED, Button
from signal import pause
from subprocess import check_call
from time import strftime

foto_button = Button(17,pull_up=True)
led = LED(18)

camera = PiCamera()
camera.rotation = 270   ## dependes on how you mount your cam
recordflag = 0          ## global


## timelapse photo
def serie():
    camera.resolution = (2592,1944)     ## 5MP
    #camera.resolution = (3280, 2464)   ## 8MP - no preview 
    camera.start_preview()
    frame = 1
    while True:
        led.off()
        sleep(2)    ## take a photo every 1+x seconds)
        timestr = strftime("%Y%m%d-%H%M%S")
        camera.capture('/home/pi/Pictures/image{}.jpg' .format(timestr))
        led.on()
        frame += 1
        sleep(1)
        if foto_button.is_pressed:
            led.on()
            camera.stop_preview()
            sleep(3)
            break            
      
## video recordstart
def recordstart():
    global recordflag
    camera.resolution = (1280,720) ## HD 1280x720 or FullHD 1920x1080
    ## camera.resolution = (1920,1080)    ## HD 1280x720 or FullHD 1920x1080
    camera.framerate = 30
    camera.video_stabilization = True
    camera.start_preview()
    recordflag = 1
    led.blink()
    timestr = strftime("%Y%m%d-%H%M%S")
    camera.start_recording('/home/pi/Videos/video{}.h264'.format(timestr), quality=0)
    ## to experiment with viedo quality try
    ## quality 10-40 (lower values are better - 20-25 are ok, 0 = default)

## video recordstop  
def recordstop():
    global recordflag
    camera.stop_recording()
    recordflag = 0
    led.on()
    camera.stop_preview()
    ## un/comment the following line for automatic video conversion
    check_call(['/home/pi/videoconvert.sh'])
    camera.framerate = 15


## shutdown raspi
def shutdown():
    camera.stop_preview()
    if recordflag == 1:
        camera.stop_recording()
    check_call(['sudo', 'poweroff'])
    

## MAIN    
led.on()
try:
    while True:
        if foto_button.is_pressed:
            t1=time()
            while foto_button.is_pressed:
                sleep(0.1)
            time_held = time() - t1
            print (time_held)           ## just for debugging
            if time_held < 2:           ## start/stop recording video
                if recordflag == 0:
                    recordstart()
                else: recordstop()
            elif time_held < 5:         ## timelapse
                if recordflag == 0:
                    serie()
            else: shutdown()

except KeyboardInterrupt:        
    camera.stop_preview()
    if recordflag == 1:
        camera.stop_recording()
    led.off()
