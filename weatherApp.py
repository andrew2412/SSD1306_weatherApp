#!/usr/bin/python
# -*- coding: utf-8 -*-

# this script draw the basic weather infomation on SSD1306 oled display connected via SPI to raspberry pi
# to have renew information, you can add this script to crontab

import openweatherAPI
from PIL import Image, ImageDraw, ImageFont, ImageChops
import datetime
#import displays.dummy
#display = displays.dummy.dummy(320, 240)

import displays.ili9341
display = displays.ili9341.ili9341()

# apikey defined in keys.py
from keys import apikey
import SHT30


poznanID = 3088171

weatherInfo = openweatherAPI.getOutsideCondition(apikey, poznanID)
 

#fontName = 'font2.ttf'
fontName = 'resources/arial.ttf'

font1 = ImageFont.truetype(fontName, 30)
font2 = ImageFont.truetype(fontName, 15)
font3 = ImageFont.truetype(fontName, 10)

insideCondition = SHT30.getInsideCondition()

def drawForecast(draw, x, y, item, img):
    global font1
    global font2
    global font3
    date = datetime.datetime.fromtimestamp(item['dt'])
    draw.text(
        (x + 30, y),
        str(date.hour) +":"+ ( "%02d" % (date.minute)),
        font=font3,
        fill=fontColor,
    ) 
    
    draw.text(
        (x + 65, y+20),
        str(int(item['main']['temp'])) + "°C",
        font=font2,
        fill=fontColor,
    ) 

    draw.text(
        (x + 65, y+40),
        str(int(item['main']['feels_like'])) + "°C",
        font=font2,
        fill=fontColor,
    ) 

    iconPath = "resources/icons/" + item['weather'][0]['icon'] + ".png";

    im = Image.open(iconPath).convert("RGBA").split()[-1]


    #im = ImageChops.invert(im)
    im = im.resize((60, 60))
    img.paste(im, (x+3,y+10))



# Change these
# to the right size for your display!
WIDTH = 320
HEIGHT = 240  # Change to 64 if needed
BORDER = 1
 
# Use for I2C.
#i2c = board.I2C()
#oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)
 
# Use for SPI
#spi = board.SPI()
#oled_cs = digitalio.DigitalInOut(board.D8)    # any GPIO pin of raspberry
#oled_dc = digitalio.DigitalInOut(board.D21)   # any GPIO pin of raspberry
#oled = adafruit_ssd1306.SSD1306_SPI(WIDTH, HEIGHT, spi, oled_dc, oled_reset, oled_cs)
  


# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new("RGBA", (WIDTH, HEIGHT))
 
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
 
# Draw a white background

iconList = ["01d", "02n", "04d", "09n", "11d", "13n", "unknown", "01n", "03d", "04n", "10d", "11n", "50d",
"02d", "03n", "09d", "10n", "13d", "50n"]

fontColor = (255,255,255)
backgroundColor = (0,0,0)

draw.rectangle((0, 0, WIDTH, HEIGHT), outline=(255, 255, 255), fill=(255, 255, 255))
# Draw a smaller inner rectangle
draw.rectangle(
    (BORDER, BORDER, WIDTH - BORDER - 1, HEIGHT - BORDER - 1),
    outline=(255, 255, 255),
    fill=backgroundColor,
)


# draw an icon
#weatherInfo['weather'][0]['icon']
iconPath = "resources/icons/" + weatherInfo['current']['weather'][0]['icon'] + ".png";

im = Image.open(iconPath).convert("RGBA").split()[-1]

#r, g, b, a = im.split()

#def invert(image):
#    return image.point(lambda p: 255 - p)

#r, g, b = map(invert, (r, g, b))

#im = Image.merge(im.mode, (r, g, b, a))

#im = ImageChops.invert(im)
im = im.resize((150, 150))
image.paste(im, (1,1), im)
# draw the temperature

draw.text((170, 5), "Inside", font=font2, fill=fontColor) 
draw.text((150, 35), str(int(insideCondition[0])) + "°C", font=font1, fill=fontColor)    

im = Image.open("resources/humidity.png").convert("RGBA").split()[-1]
im = im.resize((20, 20))
image.paste(im, (153,70), im)

# draw the preasure 
draw.text((175, 70), str(int(insideCondition[0])) +" %", font=font2, fill=fontColor) 

im = Image.open("resources/sunrise.png").convert("RGBA").split()[-1]
#im = ImageChops.invert(im)
im = im.resize((25, 25))
image.paste(im, (150,90), im)

im = Image.open("resources/sunset.png").convert("RGBA").split()[-1]
#im = ImageChops.invert(im)
im = im.resize((25, 25))
image.paste(im, (150,115), im)

sunrise = datetime.datetime.fromtimestamp(weatherInfo['current']['sys']['sunrise'])
sunset  = datetime.datetime.fromtimestamp(weatherInfo['current']['sys']['sunset'])

draw.text((185, 92), "%02d:%02d" % (sunrise.hour, sunrise.minute), font=font2, fill=fontColor) 
draw.text((185, 118),"%02d:%02d" % (sunset.hour, sunset.minute), font=font2, fill=fontColor) 

draw.text((250, 5), "Outside", font=font2, fill=fontColor) 

text = str(int(weatherInfo['current']['main']['temp'])) + "°C"
(font_width, font_height) = font1.getsize(text)
draw.text((240, 35),text,font=font1,fill=fontColor)  

draw.text((240, 70),str(int(weatherInfo['current']['main']['feels_like'])) + "°C",font=font2,fill=fontColor)   

im = Image.open("resources/humidity.png").convert("RGBA").split()[-1]
#im = ImageChops.invert(im)
im = im.resize((20, 20))
image.paste(im, (243,90), im)

draw.text((265, 90), str(weatherInfo['current']['main']["humidity"]) +" %", font=font2, fill=fontColor) 


# draw the preasure 
draw.text((240, 115), str(weatherInfo['current']['main']["pressure"]) +" hPa", font=font2, fill=fontColor) 

draw.line((0, 160, 320, 160), fill=fontColor)


drawForecast(draw, 1, 165, weatherInfo['forecast']['list'][0], image)
drawForecast(draw, 101, 165, weatherInfo['forecast']['list'][0], image)
drawForecast(draw, 201, 165, weatherInfo['forecast']['list'][0], image)

# Display image
display.draw(image.convert("RGB"))
#display.show()
