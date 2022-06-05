#!/usr/bin/python3
import os
import time

MANAGER = os.path.join(os.path.dirname(__file__),'manager.py')
LOG = os.path.join(os.path.dirname(__file__),'gaggia_log.txt')
RUN_COMMAND = f'python3 {MANAGER} > /dev/null 2>&1'
with open(LOG,'w+') as log:
    log.write(f'[{time.time()}] starting machine\n')
    while True:
        os.system(RUN_COMMAND)
        time.sleep(5)
        log.write(f'[{time.time()}] restarting\n')
