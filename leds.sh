#!/bin/bash

DIR="/home/pi/leds"

cd "$DIR"

sudo python ./control.py "$*"


