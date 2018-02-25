from picamera import PiCamera
from envirophat import motion 
from time import sleep
import pantilthat
import math
import pigpio
import keyboard

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

motor = None

def main():
    # init cam motor
    global motor
    motor = pantilthat.PanTilt()
    #motor.pan(0)

    # init cam
    cam = PiCamera()
    #cam.start_preview()

    # handle button toggle
    touchphat.all_off()

    # set up wheel motors
    ESC = 4
    pi = pigpio.pi()
    pi.set_servo_pulsewidth(ESC, 0)

    max_val = 2000
    min_val = 700

    # arming the motors
    print("Connect the battery and press enter")
    input()
    pi.set_servo_pulsewidth(ESC, 0)
    sleep(1)
    pi.set_servo_pulsewidth(ESC, max_val)
    sleep(1)
    pi.set_servo_pulsewidth(ESC, min_val)
    sleep(1)
    print("Arming done")


    # cam control functions
    def toggle_tracking(_):
        global tracking_eh
        tracking_eh = not tracking_eh

    def move_right(_):
        global motor
        motor.pan((motor.get_servo_one() + 10) if motor.get_servo_one() < 80 else 90)

    def move_left(_):
        global motor
        motor.pan((motor.get_servo_one() - 10) if motor.get_servo_one() > -80 else -90)

    def move_up(_):
        global motor
        motor.tilt((motor.get_servo_two() + 10) if motor.get_servo_two() < 80 else 90)
        
    def move_down(_):
        global motor
        motor.tilt((motor.get_servo_two() - 10) if motor.get_servo_two() > -80 else -90)

    def go_fast(_):
        pi.set_servo_pulsewidth(ESC, max_val)
        
    def so_slow(_):
        pi.set_servo_pulsewidth(ESC, min_val)
        
    def stop_motors(_):
        pi.set_servo_pulsewidth(ESC, 0)

    # cam controls
    keyboard.on_press_key("w", move_up)
    keyboard.on_press_key("s", move_down)
    keyboard.on_press_key("a", move_right)
    keyboard.on_press_key("d", move_left)
    keyboard.on_press_key(" ", toggle_tracking)
    
    # drive controls
    keyboard.on_press_key("up", go_fast)
    keyboard.on_press_key("down", so_slow)
    for key in ["up", "down"]:
        keyboard.on_release_key(key, stop_motors)

    # main bot loop
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
