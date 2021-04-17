#!/usr/bin/python
# -*- coding: utf-8 -*-

# this script draw the basic weather infomation on SSD1306 oled display connected via SPI to raspberry pi
# to have renew information, you can add this script to crontab

import openweatherAPI
import datetime
from PIL import Image

# apikey defined in keys.py
from keys import apikey
import SHT30


poznanID = 3088171
weatherInfo = openweatherAPI.getOutsideCondition(apikey, poznanID)
insideCondition = SHT30.getInsideCondition()

sunrise = datetime.datetime.fromtimestamp(weatherInfo['current']['sys']['sunrise'])
sunset  = datetime.datetime.fromtimestamp(weatherInfo['current']['sys']['sunset'])
   

# Change these
# to the right size for your display!
WIDTH = 320
HEIGHT = 240  

import viewControler

image = viewControler.prepareImage(weatherInfo, insideCondition, (WIDTH, HEIGHT))

nigthColor = (201.255, 72./255, 54./255)
dayColor = (1.0, 1.0, 1.0)

imageColor = dayColor
if datetime.datetime.now() < sunrise:
    imageColor = nigthColor
if datetime.datetime.now() > sunset:
    imageColor = nigthColor


image = image.convert("RGB")
Matrix = (
    imageColor[0], 0, 0., 0,
    0.0, imageColor[1], 0., 0,
    0., 0., imageColor[2], 0)
image = image.convert("RGB", matrix=Matrix)

import displays.ili9341
display = displays.ili9341.ili9341()

#import displays.dummy
#display = displays.dummy.dummy(320, 240)
# Display image
display.draw(image.convert("RGB"))
#display.show()
