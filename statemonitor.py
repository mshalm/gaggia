import time
import board
import digitalio
from enum import Enum
import numpy as np

BREW_PIN = board.D17
SSR_PIN = board.D27
SWITCH_DELAY = 0.05 # [s]

WINDOW_SIZE = 5.0 # [s]
# required on percentage to drive zero steady-state error
FIX_POINT = 2.1

CONTROL_RESET_STEPS = round(30.0 / SWITCH_DELAY) # [steps]

class State(Enum):
    IDLE = 1
    BREW = 2
    OFF = 3

class Monitor(object):
    def __init__(self, tempreader, pid, lcd, server):
        self.tempreader = tempreader
        self.pid = pid
        self.lcd = lcd
        self.server = server

        self.ssr = digitalio.DigitalInOut(SSR_PIN)
        self.ssr.direction = digitalio.Direction.OUTPUT
        #self.ssr.pull = digitalio.Pull.DOWN

        self.brew = digitalio.DigitalInOut(BREW_PIN)
        self.brew.direction = digitalio.Direction.INPUT
        self.brew.pull = digitalio.Pull.DOWN
        
        self.switch_time = time.time()
        self.start_time = time.time()
        
        self.state = self.readState()
        self.control = 0.0 # [%]
        self.steps = 0

    def readState(self):
        #print(self.brew.value)
        if not self.server.is_powered():
            return State.OFF
        elif self.brew.value:
            return State.BREW
        else:
            return State.IDLE

    def stateUpdate(self):
        staleness = time.time() - self.switch_time
        
        new_state = self.state
        if staleness > SWITCH_DELAY:
            new_state = self.readState()
            if new_state != self.state:
                self.switch_time = time.time()
            self.steps += 1
        self.state = new_state

    def controlUpdate(self):
        if self.steps > CONTROL_RESET_STEPS or self.state == State.OFF:
            self.steps = 0
            self.pid.reset()
            #print('control reset!')
        self.control = self.pid(self.tempreader.updateTempError())
        # print(self.control)

        # adjust for equilibrium
        self.control = FIX_POINT + self.control 
        window_position = 100.0 * \
            np.mod(time.time(), WINDOW_SIZE) / WINDOW_SIZE

        self.ssr.value = window_position < self.control \
            and (self.state is not State.OFF)

    def displayUpdate(self):
        self.lcd.updateText(self)
        #self.lcd.writeText()

    def stateCleanup(self):
        self.state = State.OFF

    def controlCleanup(self):
        # turn off ssr
        self.ssr.value = False

    def displayCleanup(self):
        self.displayUpdate()
        self.lcd.cleanupScreen()

    def step(self):
        """
        go through transition
        """
        self.stateUpdate()
        self.controlUpdate()
        self.displayUpdate()

    def cleanup(self):
        self.stateCleanup()
        self.controlCleanup()
        self.displayCleanup()

        
