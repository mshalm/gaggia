import board
import busio

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

i2c = busio.I2C(SCL_PIN, SDA_PIN)
print("initialize temp reader")
tempreader = TempReader(i2c)

print("initialize LCD")
lcd = LCDScreen(i2c)

# do this last
print("initialize LCD")
pid = PID(KP, KI, KD, setpoint=0.0)

print("initialize Monitor")
monitor = Monitor(tempreader, pid, lcd)

print("Set SIGINT handler")
signal.signal(signal.SIGINT, signal_handler)


interrupted = False

print("stepping")
while not interrupted:
    #print("stepping")
    monitor.step()
    time.sleep(0.01)

monitor.cleanup()
print("Process interrupted.")
