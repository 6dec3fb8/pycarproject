#!/usr/bin/env python3
# coding=utf-8

# main entry

# import pycar

import time

import mylogger
from pycar import misc, motor
try:
    from pycar.picam import *
    _use_picam = True
except:
    from pycar.cvcam import *
    _use_picam = False
from erlthread import *


def main():
    mylogger.loggerinit('log/loggingconf.yml')
    misc.RPiGPIOinit()

    md = motor.MotorDifferentor(12, 16, 18, 11)
    md.set_speed(30, 0)
    time.sleep(1)
    md.set_speed(0, 0)

    print("Dummy")


if __name__ == '__main__':
    main()

