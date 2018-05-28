#!/usr/bin/python3
# coding=utf-8

# used to put in init func

import logging
import logging.config
# deprecated
# import yaml

try:
    import RPi.GPIO as GPIO
    _GPIO_FAKE = False
except:
    from os import path
    import sys
    sys.path.append(
        path.join(
            path.abspath('..'),
            'pycarproject'
        )
    )
    import fakeGPIO as GPIO
    _GPIO_FAKE = True


# may also deprecate
def init(mode = None):
    # print("Initialize RPi GPIO board mode")
    RPiGPIOinit(mode)


def RPiGPIOinit(mode=None):
    # logging GPIO true/false
    _logger = logging.getLogger(__name__)
    if _GPIO_FAKE:
        _logger.warning(
            "GPIO module is running in simulate mode!"
        )
    else:
        _logger.info(
            "GPIO module import success."
        )
    # set boardmode
    if mode is None:
        _logger.debug("mode is None, use default")
        GPIO.setmode(GPIO.BOARD)
    else:
        _logger.debug("Use mode %d", mode)
        GPIO.setmode(mode)


def getpwm(port, freq):
    logger = logging.getLogger(__name__)
    logger.info("call to get pwm Ch#%d with freq %d",
                port, freq)
    GPIO.setup(port, GPIO.OUT)
    p = GPIO.PWM(port, freq)
    return p


# test: DEPRECATED
# def _test1():
#     _logger = logging.getLogger(__name__)
#     loggerinit('./log/loggingconf.yml')
#     RPiGPIOinit()
#     _logger.debug("Test 01 finished")
#
#
# if __name__ == '__main__':
#     _test1()
