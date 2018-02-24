from picamera import PiCamera
from envirophat import motion 
from time import sleep
import pantilthat
import touchphat
import math

def track(init_heading, i, motor, prev):
    acc = motion.accelerometer()
    heading = (motion.heading() + i) % 360

    # handle tilt
    tilt = math.floor(90 * acc[0])
    if tilt > 90:
        tilt = 90
    elif tilt < -90:
        tilt = -90

    if prev[0] is None or abs(tilt-prev[0]) > 3:
        motor.tilt(tilt)
    else:
        tilt = prev[0]
    
    # handle pan
    heading = heading - init_heading
    if heading < -90:
        heading = -90
    elif heading > 90:
        heading = 90

    if prev[1] is None or abs(heading - prev[1]) > .5:
        motor.pan(heading)
    else:
        heading = prev[1]
    
    return (tilt, heading)


def main():
    # init motor
    motor = pantilthat.PanTilt()

    # init cam
    cam = PiCamera()
   # cam.start_preview()

    # handle button toggle
    #touchphat.all_off()

    def toggle_tracking(event):
        global tracking_eh
        tracking_eh = not tracking_eh

    touchphat.on_touch("A", toggle_tracking)

    prev = (None, None)
    while True:
        # handle init heading
        if not tracking_eh:
            init_heading = motion.heading()
            i = 0
            if init_heading > 270:
                init_heading -= 90
                i = -90
            elif init_heading < 90:
                init_heading += 90
                i = 90
        else:
            prev = track(init_heading, i, motor, prev)


tracking_eh = False
if __name__ == "__main__":
    main()
