#!/usr/bin/python
# -*- coding: utf-8 -*-

# this script draw the basic weather infomation on SSD1306 oled display connected via SPI to raspberry pi
# to have renew information, you can add this script to crontab

import urllib.request
import json
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# apikey defined in keys.py
from keys import apikey

url = 'http://api.openweathermap.org/data/2.5/weather?id=3088171&appid={}&units=metric'.format(apikey)

http = urllib.request.urlopen(url)
jsonString = http.read()
weatherInfo = json.loads(jsonString)
 
# Define the Reset Pin
oled_reset = digitalio.DigitalInOut(board.D4)
 
# Change these
# to the right size for your display!
WIDTH = 128
HEIGHT = 64  # Change to 64 if needed
BORDER = 1
 
# Use for I2C.
#i2c = board.I2C()
#oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)
 
# Use for SPI
spi = board.SPI()
oled_cs = digitalio.DigitalInOut(board.D8)    # any GPIO pin of raspberry
oled_dc = digitalio.DigitalInOut(board.D21)   # any GPIO pin of raspberry
oled = adafruit_ssd1306.SSD1306_SPI(WIDTH, HEIGHT, spi, oled_dc, oled_reset, oled_cs)
  
# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new("1", (oled.width, oled.height))
 
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
 
# Draw a white background
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
 
# Draw a smaller inner rectangle
draw.rectangle(
    (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
    outline=0,
    fill=0,
)
 
# Load default font.
font1 = ImageFont.truetype("font.ttf", 25)
font2 = ImageFont.truetype("font.ttf", 12)

# draw an icon
iconPath = "icons/" + weatherInfo['weather'][0]['icon'] + ".png";
im = Image.open(iconPath).convert("RGBA").split()[-1]
im = im.resize((60, 60))
image.paste(im, (2,2))

# draw the temperature
text = str(int(weatherInfo['main']['temp'])) + "°C";
(font_width, font_height) = font1.getsize(text)
draw.text(
    (59, 5),
    text,
    font=font1,
    fill=255,
)    

# draw the preasure 
draw.text(
    (59, 45),
    str(weatherInfo['main']["pressure"]) +"hPa",
    font=font2,
    fill=255,
) 


# Display image
oled.image(image)
oled.show()
