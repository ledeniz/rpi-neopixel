# rpi-neopixel
WS281x ("Neopixel") LED strip control on a Raspberry Pi

This script helps me to control a WS2812B LED strip when my 3D printer does something.

## Usage
`sudo python ./control.py on|off|toggle|dim|bright|done|attention|fail|error|unlock`

### Available Arguments
- toggle
- on (default color; dim)
- off
- dim
- bright
- done (violet)
- attention (blue)
- fail (orange)
- error (red)
- unlock (removes lock file)

## How does it work?
The script itself uses the [rpi-ws281x-python](https://github.com/rpi-ws281x/rpi-ws281x-python) library to control the LED strip.

In order to react to events triggered by my 3D printer I set up the following on the RPi:
- OctoPrint (with the Webhooks plugin) calls several API routes for different events (e.g. "Print done")
- Node-RED provides some API endpoints for the different commands & watches a GPIO pin (push button)

**Beware!**
You have to use root privileges in order to use PWM on the Raspberry Pi.
I made a new entry for this in my sudoers file (use visudo)

`pi      ALL=NOPASSWD:/home/pi/rpi-neopixel/control.py`

## Customization
You can set your default color and your own colors in the control.py script itself.

## Credits

A huge THANK YOU to the contributors of [rpi-ws281x-python](https://github.com/rpi-ws281x/rpi-ws281x-python)

Special thanks to [Tony DiCola](https://github.com/tdicola) (tony@tonydicola.com) & [Jeremy Garff](https://github.com/jgarff) (jer@jers.net)

This repository and all it's containing files are licensed under the BSD-2-Clause license.
