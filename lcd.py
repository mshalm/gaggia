import board
import busio
import adafruit_ssd1306

import time

from PIL import Image, ImageDraw, ImageFont

from statemonitor import State, Monitor


UPDATE_MIN_DELAY = 0.5
WIDTH = 128
HEIGHT = 64

TITLE = "G\nA\nG\nG\nI\nA"
TITLE_HEIGHT = 14
LINE_HEIGHT = 16

TEMP_TEXT = "Temp:"
SET_TEXT  = "Set:"

TEMP_STYLE = "{:.1f}C"
TIME_STYLE = "{:.f1}s"
TEXT_X = 15

SCL_PIN = board.SCL
SDA_PIN = board.SDA

class LCDScreen(object):
    def __init__(self, i2c):
        self.i2c = i2c
        self.screen = adafruit_ssd1306.SSD1306_I2C(WIDTH, \
            HEIGHT, self.i2c, addr=0x3c)
        self.boiler_temp = 0.0
        self.command_temp = 0.0
        self.brew_time = 0.0
        self.write_time = 0.0
        self.title_font = ImageFont.truetype("FreeMono.ttf", size=16) 
        self.font = ImageFont.truetype("FreeMono.ttf", size=16)
        (title_width, title_height) = self.font.getsize(TITLE)
        print(title_width, title_height)
        self.title_pos = (3, 4 + WIDTH // 2 - title_width // 2)
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
            # print("display activate")
            self.write_time = time.time()

            # blank canvas
            self.screen.fill(0)


            # construct text draw
            image = Image.new("1", (self.screen.height, self.screen.width))
            draw = ImageDraw.Draw(image)

            # draw headline background
            draw.rectangle((0, 0, TITLE_HEIGHT, self.screen.width), outline=255, fill=255)

            # draw headline
            draw.text(self.title_pos, TITLE, font=self.title_font, \
                fill=0)

            
            draw.text((TEXT_X, 0), TEMP_TEXT, font=self.font, \
                fill=255)

            draw.text((TEXT_X, 1 * LINE_HEIGHT), \
                TEMP_STYLE.format(self.boiler_temp), \
                font=self.font, fill=255)
            
            draw.text((TEXT_X, 3 * LINE_HEIGHT), SET_TEXT, \
                font=self.font, fill=255)

            draw.text((TEXT_X, 4 * LINE_HEIGHT), \
                TEMP_STYLE.format(self.command_temp), \
                font=self.font, fill=255)

            # draw image
            self.screen.image(image.rotate(270, expand=True))
            self.screen.show()

if __name__ == "__main__":
    lcd = LCDScreen(busio.I2C(SCL_PIN, SDA_PIN))
    while True:
        lcd.writeText()
        print(lcd.printText())
        time.sleep(UPDATE_MIN_DELAY)
