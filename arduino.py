import time, sys
from fhict_cb_01.CustomPymata4 import CustomPymata4
import requests

BUTTON2PIN = 9
BUTTON1PIN = 8
REDLEDPIN = 4
GREENLEDPIN = 5
BUZZER = 3

def setup():
    global board
    board = CustomPymata4(com_port = "COM4")
    board.set_pin_mode_digital_input_pullup(BUTTON1PIN)
    board.set_pin_mode_digital_input_pullup(BUTTON2PIN)
    board.set_pin_mode_digital_output(REDLEDPIN)
    board.set_pin_mode_pwm_output(BUZZER)
    board.displayOn()

def loop():
    level, time_stamp = board.digital_read(BUTTON1PIN)
    
    if (level == 0):
        requests.get('http://127.0.0.1:5000/oven-started')
        t = 30
        while t:
            board.digital_pin_write(REDLEDPIN, 1)
            board.digital_pin_write(GREENLEDPIN, 0)
            board.pwm_write(BUZZER, 0)
            mins = t // 60
            secs = t % 60
            timer = '{:02d}{:02d}'.format(mins, secs)
            board.displayShow(timer)
            print(timer, end="\r")
            time.sleep(1)
            t -= 1

        board.digital_pin_write(REDLEDPIN, 0)
        board.digital_pin_write(GREENLEDPIN, 1)
        # board.pwm_write(BUZZER, 1000)
        requests.get('http://127.0.0.1:5000/oven-finished')

        time.sleep(0.01)
    elif (level == 0):
        print("press button", end="\r")


        

setup()
while True:
    try:
        loop()
    except KeyboardInterrupt: # crtl+C
        print ('shutdown')
        board.shutdown()
        sys.exit(0)