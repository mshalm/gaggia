import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

ads = None
temp_chan = None
pot_chan = None

def init():
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    
    temp_chan = AnalogIn(ads, ADS.P2)
    pot_chan = AnalogIn(ads, ADS.P1)
    
def read_temp():
    pass
