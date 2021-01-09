from tempreader import TempReader
from simple_pid import PID
from statemonitor import Monitor
from lcd import LCDScreen

import signal

KP = 4.5
KI = 0.125
KD = 0.2

def signal_handler(signal, frame):
    global interrupted
    interrupted = True


tempreader = TempReader()

lcd = LCDScreen()

# do this last
pid = PID(KP, KI, KD, setpoint=0.0)

monitor = Monitor(tempreader, pid, lcd)

signal.signal(signal.SIGINT, signal_handler)


interrupted = False


while not interrupted:
    monitor.step()

print("Process interrupted.")