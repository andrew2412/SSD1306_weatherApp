
import digitalio
import busio
from board import *
from adafruit_rgb_display import color565
import adafruit_rgb_display.ili9341 as ili9341Core

from displays.display import display

class ili9341(display):
    def __init__(self):
        # Change these
        # to the right size for your display!
        self.WIDTH = 320
        self.HEIGHT = 240  # Change to 64 if needed
        
        CS_PIN = D25
        DC_PIN = D24    
        RST_PIN = D23

        spi = busio.SPI(clock=SCK, MOSI=MOSI, MISO=MISO)
        self.display = ili9341Core.ILI9341(spi, 
                                  cs=digitalio.DigitalInOut(CS_PIN),
                                  dc=digitalio.DigitalInOut(DC_PIN), 
                                  rst=digitalio.DigitalInOut(RST_PIN))

    def getSize(self):
        return (self.WIDTH, self.HEIGHT)

    def draw(self, image):
        self.display.image(image, 270)
