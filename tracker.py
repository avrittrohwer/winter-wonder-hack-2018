import touchphat
import pantilthat
import motion from envirophat
import time
import math

def get_pan_angle(pos):
    """
    Calculates the pan angle the camera should be at.

    pos: (x, y, z)
    """
    x, y, z = pos

    return 90 - math.degrees(math.atan(z / x))

def get_tilt_angle(pos):
    """
    Calculates the tilt angle the camera should be at.

    pos: (x, y, z)
    """
    x, y, z = pos

    return 90 - math.degrees(math.atan(z / y))

def g_to_pos(g, pos, time):
    """
    Converts a gs vector to a position based on time.

    g:   (x, y, z) in g's
    pos: (x, y, z) in m
    """
    g_x, g_y, g_z = g
    p_x, p_y, p_z = pos
    return (
        p_x + (g_x * time**2 * 9.81),
        p_y + (g_y * time**2 * 9.81),
        p_z + (g_z * time**2 * 9.81),
    )

def main():
    # initialize motor controller
    controller = pantilthat.PanTilt()

    cur_pos = (0, 0, 1)

    start = time.time()
    while True:
        acc = motion.accelerometer() # (x, y, z)
        delta_t = (time.time() - start)
        new_pos = g_to_pos(acc, cur_pos, delta_t)

        # adjust the camera
        controller.pan(get_pan_angle(new_pos))
        controller.tilt(get_tilt_angle(new_pos))

        start = time.time()

if __name__ == "main":
    main()