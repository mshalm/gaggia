import time
import board
import digitalio
from enum import Enum
import numpy as np

BREW_PIN = board.D4
SSR_PIN = board.D5
SWITCH_DELAY = 0.01 # [s]
WINDOW_SIZE = 5.0 # [s]
TIMEOUT_TIME = 3.0 * 60.0 * 60.0 # [s]

class State(Enum):
    IDLE = 1
    BREW = 2
    TIMEOUT = 3

class Monitor(object):
    def __init__(self, tempreader, pid, lcd):
        self.tempreader = tempreader
        self.pid = pid
        self.lcd = lcd

        self.ssr = digitalio.DigitalInOut(SSR_PIN)
        self.ssr.direction = digitalio.Direction.OUTPUT

        self.brew = digitalio.DigitalInOut(BREW_PIN)
        self.brew.direction = digitalio.Direction.INPUT
        self.brew.pull = digitalio.Pull.DOWN
        
        self.switch_time = time.time()
        self.start_time = time.time()
        
        self.state = self.readState()
        self.control = 0.0 # [%]

    def readState(self):
        if time.time() - self.start_time > TIMEOUT_TIME:
            return State.TIMEOUT
        elif self.brew.value:
            return State.BREW
        else:
            return State.IDLE

    def stateUpdate(self):
        staleness = time.time() - self.switch_time
        
        new_state = self.state
        if staleness < SWITCH_DELAY:
            new_state = self.readState()
            if new_state != self.state:
                self.switch_time = time.time()
        self.state = new_state

    def controlUpdate(self):
        self.control = self.pid(self.tempreader.updateTempError())

        window_position = 100.0 * \
            np.mod(time.time(), WINDOW_SIZE) / WINDOW_SIZE

        self.ssr.value = window_position < self.control \
            and (self.state is not State.TIMEOUT)

    def displayUpdate(self):
        self.lcd.updateText(self)

    def step(self):
        """
        go through transition
        """
        self.stateUpdate()
        self.controlUpdate()
        self.displayUpdate()
        
