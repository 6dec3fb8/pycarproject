#!/usr/bin/python3

# test for misc.py

import logging

import sys
from os import path
print("Parent path at:", path.abspath('..'))
sys.path.append(
    path.join(
        path.abspath(".."),
        'pycarproject'
    )
)
# print(sys.path)
from pycar import misc
try:
    from RPi import GPIO
except:
    import fakeGPIO as GPIO


def test1():
    # test PWM functions
    print("Initialize logger")
    misc.loggerinit('log/loggingconf.yml')
    print("Initialize RPi GPIO board mode")
    misc.RPiGPIOinit()
    print("Begin test1 of PWM")
    logger = logging.getLogger('test')
    logger.info("PWM test start.")
    p = GPIO.PWM(12, 100)
    p.start(100)
    p.ChangeDutyCycle(0)
    p.ChangeFrequency(200)
    p.ChangeDutyCycle(100)
    p.stop()
    logger.info("PWM test end.")
    print("Test over")


if __name__ == '__main__':
    test1()
