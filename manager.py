import board
import busio
from adafruit_extended_bus import ExtendedI2C

from tempreader import TempReader
from simple_pid import PID
from statemonitor import Monitor
from lcd import LCDScreen

import signal
import time


SCL_PIN = board.SCL
SDA_PIN = board.SDA


KP = 5.0
KI = 0.05
KD = 1.0

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

i2c_1 = busio.I2C(SCL_PIN, SDA_PIN)
#i2c_4 = ExtendedI2C(4, frequency=200000)
print("initialize temp reader")
tempreader = TempReader(i2c_1)

print("initialize LCD")
lcd = LCDScreen()

# do this last
print("initialize LCD")
pid = PID(KP, KI, KD, setpoint=0.0)

print("initialize Monitor")
monitor = Monitor(tempreader, pid, lcd)

print("Set SIGINT handler")
signal.signal(signal.SIGINT, signal_handler)


interrupted = False

print("stepping")
l_t = time.time()
# try:
while not interrupted:
    c_t = time.time()
    #print(c_t-l_t)
    l_t = c_t
    #print("stepping")
    monitor.step()
    time.sleep(0.001)
#except:
#    print("exception encountered")

monitor.cleanup()
print("Process interrupted.")
