import board
import busio
import adafruit_ssd1306

import time

from PIL import Image, ImageDraw, ImageFont

from statemonitor import State, Monitor


UPDATE_MIN_DELAY = 0.1
WIDTH = 128
HEIGHT = 64
TITLE = "GAGGIA"

PRINT_TEXT = """Temp: {:.1f}\nSet: {:.1f}\nTime: {:.1f}"""
TEXT_POS = (0, 16)

SCL_PIN = board.SCL
SDA_PIN = board.SDA

class LCDScreen(object):
    def __init__(self):
        self.i2c = busio.I2C(SCL_PIN, SDA_PIN)
        self.screen = adafruit_ssd1306.SSD1306_I2C(WIDTH, \
            HEIGHT, self.i2c, addr=0x3c, reset=None)
        self.boiler_temp = 0.0
        self.command_temp = 0.0
        self.brew_time = 0.0
        self.write_time = 0.0
        self.font = ImageFont.truetype("FreeMono.ttf", size=16)
        (title_width, title_height) = self.font.getsize(TITLE)
        self.title_pos = \
            (self.screen.width // 2 - title_width // 2, 0)
        self.writeText()

    def updateText(self, monitor):
        self.boiler_temp = monitor.tempreader.getBoilerTemp()
        self.command_temp = monitor.tempreader.getCommandTemp()
        if monitor.state == State.BREW:
            self.brew_time = time.time() - monitor.switch_time

    def printText(self):
        return PRINT_TEXT.format(self.boiler_temp, \
            self.command_temp, self.brew_time)

    def writeText(self):
        if time.time() - self.write_time > UPDATE_MIN_DELAY:
            self.write_time = time.time()

            # blank canvas
            self.screen.fill(0)


            # construct text draw
            image = Image.new("1", (oled.width, oled.height))
            draw = ImageDraw.Draw(image)

            
            # draw headline
            draw.text(self.title_pos, TITLE, font=self.font, \
                fill=255)
            draw.text(TEXT_POS, self.printText(), font=self.font, \
                fill=255)

            # draw image
            self.screen.image(image)

if __name__ == "__main__":
    lcd = LCDScreen()
    lcd.writeText()