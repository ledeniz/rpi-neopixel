#!/usr/bin/env python
#
# WS2812B control script by Deniz Erdogan (dev@ledeniz.de)
# 
# Based on the great work of Tony DiCola (tony@tonydicola.com)
#                        and Jeremy Garff (jer@jers.net)
#
import argparse
import pickle
import os

from pathlib import Path
from neopixel import *

# LED strip configuration:
LED_COUNT      = 24      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).

LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest

LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

LOCK  = "/tmp/led.lock"  # This script will do nothing if that file exists
STATE = "/tmp/led.state" # Informations about the current state (last color & if the lights are on)

colors = {
    "none":   Color(0, 0, 0),
    "bright": Color(128, 255, 64),
    "dim":    Color(32, 64, 16),
    "violet": Color(0, 150, 255),
    "orange": Color(64, 255, 32),
    "red":    Color(1, 255, 1),
    "blue":   Color(155, 155, 255)
}

colors["default"] = colors["dim"]

def fill(strip, color):
    for i in range(0, strip.numPixels(), 1):
        strip.setPixelColor(i, color)
        strip.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', help='on|off|toggle|done|attention|fail|error')
    args = parser.parse_args()

    if os.path.isfile(LOCK) and args.mode != 'unlock':
        print("locked: " + LOCK)
        exit()
    else:
        Path(LOCK).touch()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    if os.path.isfile(STATE):
        with open(STATE, 'rb') as file:
            state = pickle.load(file)
    else:
        state = {"color": False, "active": False}

    color = colors["default"]
    active = True

    if args.mode == 'off':
        color = colors["none"]
        active = False

    elif args.mode == 'unlock':
        os.remove(LOCK)
        exit()

    elif args.mode == 'on':
        color = colors["default"] 

    elif args.mode == 'bright':
        color = colors["bright"]

    elif args.mode == 'dim':
        color = colors["dim"]

    elif args.mode == 'done':
        color = colors["violet"]

    elif args.mode == 'attention':
        color = colors["blue"]

    elif args.mode == 'fail':
        color = colors["orange"]

    elif args.mode == 'error':
        color = colors["red"]

    elif args.mode == 'toggle' or args.mode == '':
        active = not state["active"]
        
        if active:
            color = state["color"]
        else:
            color = colors["none"]
    else:
        print("invalid argument: '" + str(args.mode) + "'")
        os.remove(LOCK)
        exit()

    fill(strip, color)

    state["active"] = active

    if color != colors["none"]:
        state["color"] = color

    # save current state
    with open(STATE, 'wb') as file:
        pickle.dump(state, file, pickle.HIGHEST_PROTOCOL)

    os.remove(LOCK)
    exit()
