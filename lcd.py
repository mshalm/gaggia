import board
import busio
import adafruit_ssd1306

import time

from PIL import Image, ImageDraw, ImageFont

from statemonitor import State, Monitor


UPDATE_MIN_DELAY = 0.1
WIDTH = 128
HEIGHT = 64

PRINT_TEXT = """Temp: {:.1f}\nSet: {:.1f}\nTime: {:.1f}"""

SCL_PIN = board.SCL
SDA_PIN = board.SDA

class LCDScreen(object):
	def __init__(self):
		self.i2c = busio.I2C(SCL_PIN, SDA_PIN)
		self.screen = adafruit_ssd1306.SSD1306_I2C(WIDTH, \
			HEIGHT, i2c, addr=0x3c, reset=None)
		self.boiler_temp = 0.0
		self.command_temp = 0.0
		self.brew_time = 0.0
		self.write_time = time.time()

	def updateText(self, monitor):
		self.boiler_temp = monitor.tempreader.getBoilerTemp()
		self.command_temp = monitor.tempreader.getCommandTemp()
		if monitor.state = State.BREW:
			self.brew_time = time.time() - monitor.switch_time

	def writeText(self):
		if time.time() - self.write_time > UPDATE_MIN_DELAY
			self.write_time = time.time()

			# blank canvas
			self.screen.fill(0)
			font = ImageFont.load_default()
			text = PRINT_TEXT.format(self.boiler_temp, \
				self.command_temp, self.brew_time)