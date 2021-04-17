
from displays.display import display

import board
import digitalio
import adafruit_ssd1306

class ssd_1306(display):
    def __init__(self): 
        self.width = 128
        self.height = 64
        spi = board.SPI()
        oled_cs = digitalio.DigitalInOut(board.D8)    # any GPIO pin of raspberry
        oled_dc = digitalio.DigitalInOut(board.D21)   # any GPIO pin of raspberry
        oled_rst = digitalio.DigitalInOut(board.D4)  # not used at all
        self.display = adafruit_ssd1306.SSD1306_SPI(self.width, self.height, spi, oled_dc, oled_reset, oled_cs)        

    def getSize():
        return (self.width, self.height)

    def draw(self, image):
        oled.image(image)
        oled.show()