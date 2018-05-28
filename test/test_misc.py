#!/usr/bin/python3

# test for misc.py

# import logging

import sys
from os import path
print("Parent path at:", path.abspath('..'))
sys.path.append(
    path.join(
        path.abspath(".."),
        'pycarproject'
    )
)

import logger
# print(sys.path)
from pycar import misc
try:
    from RPi import GPIO
except:
    import fakeGPIO as GPIO


def test1():
    print("Test 01 for module misc")
    from os import path
    print(path.abspath(path.curdir))
    logger.loggerinit(
        path.join(
            path.abspath('.'),
            'log/loggingconf.yml'
        )
    )
    # misc.loggerinit('log/loggingconf.yml')
    print("Module", __name__)
    # logger = logging.getLogger('test')
    _logger = logger.getLogger('test')
    _logger.debug("Test01 in %s: testing logger 'test'", __name__)
    # print("System modules:", sys.modules)
    print("Test RPi sim/real init")
    misc.RPiGPIOinit()
    print("Module same test")
    print(id(GPIO), id(misc.GPIO), id(GPIO)==id(misc.GPIO),
          GPIO._gpio_mode, misc.GPIO._gpio_mode)
    print("Test getmode")
    mode = GPIO.getmode() or -1
    _logger.debug("Get mode:%d", mode)
    print("Test over.")


if __name__ == '__main__':
    test1()
