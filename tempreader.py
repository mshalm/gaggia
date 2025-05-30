import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import numpy as np
import time
PGA = 2

BOIL_BUF_LEN = 16
POT_BUF_LEN = 2

V_POT_MIN = 0.0 # [V]
V_POT_MAX = 2.0 # [V]
V_POT_RANGE = V_POT_MAX - V_POT_MIN # [V]

T_POT_MIN = 85.0 # [K]
T_POT_MAX = 100.0 # [K]
T_POT_RES = 0.5 # [K]
T_POT_RANGE = T_POT_MAX - T_POT_MIN # [K]

POT_V2T = T_POT_RANGE / V_POT_RANGE # [K / V]

V_BOILER_OFFSET = 1.2362 # [V]
BOILER_V2T = 1 / .005 # [K / V]

c0 = 0.000000e+00
c1 = 2.508355e+01
c2 = 7.860106e-02
c3 = -2.503131e-01
c4 = 8.315270e-02
c5 = -1.228034e-02
c6 = 9.804036e-04
c7 = -4.413030e-05
c8 = 1.057734e-06
c9 = -1.052755e-08


class RingBuffer(object):
    def __init__(self, size, initval = 0.0, res = None):
        """Initialization"""
        self._index = 0
        self._size = size
        self._data = np.array([initval] * size)
        self._value = initval
        self._res = res

    def __call__(self, a = None):
        """process reading"""
        if a is not None:
            self._data[self._index] = a
            self._index = (self._index + 1) % self._size
            self._value = np.mean(self._data)
            if not self._res is None:
                self._value = round(self._value / self._res) * self._res
        return self._value


class TempReader(object):
    def __init__(self, i2c):
        self.i2c = i2c
        self.ads = ADS.ADS1115(self.i2c)
        self.ads.gain = PGA
    
        self.boiler = AnalogIn(self.ads, ADS.P2)
        boiler_init = self.__readBoilerTemp()
        self.boiler_buffer = RingBuffer(BOIL_BUF_LEN, boiler_init)

        self.command = AnalogIn(self.ads, ADS.P0)
        command_init = self.__readCommandTemp()
        self.command_buffer = RingBuffer(POT_BUF_LEN, command_init, T_POT_RES)

    def __readBoilerTemp(self):
        boiler_volts = self.boiler.voltage
        return (boiler_volts - V_BOILER_OFFSET) * BOILER_V2T

    def __readCommandTemp(self):
        pot_volts = self.command.voltage
         
        temp = T_POT_MIN + (pot_volts - V_POT_MIN) * POT_V2T
        
        # clip to range
        temp = min(T_POT_MAX, max(temp, T_POT_MIN))

        return temp

    def getBoilerTemp(self, nt = None):
        return self.boiler_buffer(nt)

    def getCommandTemp(self, nt = None):
        return self.command_buffer(nt)

    def updateBoilerTemp(self):
        return self.getBoilerTemp(self.__readBoilerTemp())

    def updateCommandTemp(self):
        return self.getCommandTemp(self.__readCommandTemp())

    def getTempError(self):
        return self.getBoilerTemp() - self.getCommandTemp()

    def updateTempError(self):
        return self.updateBoilerTemp() - self.updateCommandTemp()

if __name__ == "__main__":
    L = 10
    IV = 1
    rb = RingBuffer(L, IV)

    print("RingBuffer test")
    for i in range(L):
        print(rb(IV + 1))
        print(rb())

    print("TempReader test")
    tr = TempReader(busio.I2C(board.SCL, board.SDA))
    print(AnalogIn(tr.ads, ADS.P2).voltage)

    while True:
        time.sleep(1)
        print(tr.updateBoilerTemp())
        print(tr.updateCommandTemp())
        print(tr.updateTempError())
    
