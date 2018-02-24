from picamera import PiCamera
from envirophat import motion 
from time import sleep
import pantilthat
import math



def track(init_heading):
    i = 0
    if init_heading > 270:
        init_heading -= 90
        i = -90

    if init_heading < 90:
        init_heading += 90
        i = 90

    while True:
        acc = motion.accelerometer()
        heading = (motion.heading() + i) % 360

        # handle tilt
        tilt = 90 * acc[0]
        tilt = math.floor(tilt) if tilt < 90 else 90
        tilt = math.floor(tilt) if tilt > -90 else -90
        motor.tilt(tilt)

        # handle pan
        
        motor.pan(math.floor(heading - init_heading))
        



motor = pantilthat.PanTilt()
init_heading = motion.heading()
cam = PiCamera()
cam.start_preview()

track(init_heading)
