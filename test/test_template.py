#!/usr/bin/python3

# common part of a test file.

test_subject = 'Template'

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
    logger.info("Test of %s end.", test_subject)
    print("End test %s" % test_subject)


if __name__ == '__main__':
    test1()
