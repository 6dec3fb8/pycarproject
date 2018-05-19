#!/usr/bin/python3

# common part of a test file.

test_subject = 'MotorDifferentor'

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

#GPIO, may mot used.
try:
    from RPi import GPIO
except:
    import fakeGPIO as GPIO

from pycar.motor import MotorDifferentor


def test1():
    # test PWM functions
    print("Initialize logger")
    misc.loggerinit('log/loggingconf.yml')
    print("Initialize RPi GPIO board mode")
    misc.RPiGPIOinit()
    print("Begin test %s" % test_subject)
    logger = logging.getLogger('test')
    logger.info("Test of %s start.", test_subject)
    # TODO:
    # add test-code here.
    mdiff = MotorDifferentor(12, 16, 18, 11)
    mdiff.set_speed(0, 0)
    mdiff.set_speed(100, 20)
    mdiff.set_speed(20, 20)
    mdiff.set_speed(20, 10)
    mdiff.set_speed(20, 30)
    mdiff.set_speed(-20, -20)
    mdiff.set_speed(-20, -30)
    mdiff.set_speed(-20, -10)
    mdiff.set_speed(20, -20)
    mdiff.set_speed(-20, 20)
    mdiff.set_speed(20, 20)
    mdiff.set_speed(20, 20)
    mdiff.set_speed(0, 0)
    logger.info("Test of %s end.", test_subject)
    print("End test %s" % test_subject)


if __name__ == '__main__':
    test1()
