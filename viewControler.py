
from PIL import Image, ImageDraw, ImageFont, ImageChops
import os
import datetime


#__fontName = 'font2.ttf'
__fontName = 'resources/arial.ttf'
__fonts = { 30 : ImageFont.truetype(__fontName, 30),
            20 : ImageFont.truetype(__fontName, 20),
            15 : ImageFont.truetype(__fontName, 15),
            10 : ImageFont.truetype(__fontName, 10)}

__icons = ["01d", "02n", "04d", "09n", "11d", "13n", "unknown", "01n", "03d", "04n", "10d", "11n", "50d",
"02d", "03n", "09d", "10n", "13d", "50n"]

white = (255,255,255)
black = (0,0,0)
fontColor = white

def prepareImage(weatherInfo, insideCondition, size):
    if size == (320, 240):
        return __prepare320x240(weatherInfo, insideCondition)
    elif size == (128, 64):
        return __prepare128x64(weatherInfo, insideCondition)
    else:
        raise "Not implemented size"

def __prepare320x240(weatherInfo, insideCondition):
    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    WIDTH = 320
    HEIGHT = 240
    BORDER = 1
    image = Image.new("RGBA", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    fontColor = white
    backgroundColor = black

    draw.rectangle((0, 0, WIDTH, HEIGHT), outline=white, fill=white)
    # Draw a smaller inner rectangle
    draw.rectangle(
        (BORDER, BORDER, WIDTH - BORDER - 1, HEIGHT - BORDER - 1),
        outline = white,
        fill = backgroundColor)

    # draw an icon
    iconPath = os.path.join("resources/icons/", weatherInfo['current']['weather'][0]['icon'] + ".png")

    im = Image.open(iconPath).convert("RGBA").split()[-1]
    im = im.resize((150, 150))
    image.paste(im, (1,1), im)
    # draw the temperature

    draw.text((160, 5), "Inside", font=__fonts[20], fill=fontColor) 
    draw.text((240, 5), "Outside", font=__fonts[20], fill=fontColor) 
 
    draw.text((150, 35), str(int(insideCondition[0])) + "°C", font=__fonts[30], fill=fontColor)    

    text = str(int(weatherInfo['current']['main']['temp'])) + "°C"
    draw.text((240, 35),text,font=__fonts[30],fill=fontColor) 

    sunrise = datetime.datetime.fromtimestamp(weatherInfo['current']['sys']['sunrise'])
    sunset  = datetime.datetime.fromtimestamp(weatherInfo['current']['sys']['sunset'])
   
    draw.text((240, 70),str(int(weatherInfo['current']['main']['feels_like'])) + "°C",font=__fonts[15],fill=fontColor)   

    __putLineOnImage(image, draw, (150, 70), "humidity.png", int(insideCondition[1]), " %")
    __putLineOnImage(image, draw, (243, 90), "humidity.png", int(weatherInfo['current']['main']["humidity"]), " %")
    __putLineOnImage(image, draw, (150, 90), "sunrise.png", "%02d:%02d" % (sunrise.hour, sunrise.minute), "")
    __putLineOnImage(image, draw, (150, 115), "sunrise.png", "%02d:%02d" % (sunset.hour, sunset.minute), "")

    # draw the preasure 
    draw.text((240, 115), str(weatherInfo['current']['main']["pressure"]) +" hPa", font=__fonts[15], fill=fontColor) 


    draw.line((0, 160, 320, 160), fill=fontColor)
    __drawForecast(draw, 1, 165, weatherInfo['forecast']['list'][0], image)
    __drawForecast(draw, 101, 165, weatherInfo['forecast']['list'][1], image)
    __drawForecast(draw, 201, 165, weatherInfo['forecast']['list'][2], image)
    return image


def __prepare128x64(weatherInfo, insideCondition):
    return null


def __putLineOnImage(image, draw, pos, icon, value, unit):
    global __fonts
    im = Image.open(os.path.join("resources", icon)).convert("RGBA").split()[-1]
    #im = ImageChops.invert(im) 
    im = im.resize((20, 20))
    image.paste(im, pos, im)
    draw.text((pos[0]+22, pos[1]), str(value)+unit, font=__fonts[15], fill=white) 
    
def __drawForecast(draw, x, y, item, img):
    global __fonts
    date = datetime.datetime.fromtimestamp(item['dt'])
    draw.text(
        (x + 30, y),
        str(date.hour) +":"+ ( "%02d" % (date.minute)),
        font= __fonts[10],
        fill=fontColor,
    ) 
    
    draw.text(
        (x + 65, y+20),
        str(int(item['main']['temp'])) + "°C",
        font=__fonts[15],
        fill=fontColor,
    ) 

    draw.text(
        (x + 65, y+40),
        str(int(item['main']['feels_like'])) + "°C",
        font=__fonts[15],
        fill=fontColor,
    ) 

    iconPath = "resources/icons/" + item['weather'][0]['icon'] + ".png";

    im = Image.open(iconPath).convert("RGBA").split()[-1]


    #im = ImageChops.invert(im)
    im = im.resize((60, 60))
    img.paste(im, (x+3,y+10))

