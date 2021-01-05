import board
import busio
import time

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

ads = None
ads_pga = 2
temp_chan = None
pot_chan = None

temp_offset = 1.2362

def init():
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    
    ads.gain = ads_pga

    temp_chan = AnalogIn(ads, ADS.P2)
    pot_chan = AnalogIn(ads, ADS.P1)
    
    return (temp_chan, pot_chan)

def read_temp(temp):
    volts = temp.voltage
    
    return (volts - temp_offset) / .005 

def read_pot(p):
    return p.voltage

if __name__ == "__main__":
    t, p = init()
    t_init = time.time()
    N = 10
    for i in range(N):
        read_temp(t)
        read_pot(p)
    print(read_temp(t),read_pot(p))
    print((time.time() - t_init)/(N*2))

