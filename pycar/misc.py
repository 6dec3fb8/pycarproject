#!/usr/bin/python3
# coding=utf-8

# used to put in init func

import logging
import logging.config
import yaml
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


def init():

    pass


# default config file is in ./log/loggingconf.yml
# however, it is not provided as a default param.
def loggerinit(filepath):
    # initialize the global logger config
    try:
        # logging_conf_file = open(filepath)
        with open(filepath) as logging_conf_file:
            conf_yaml = yaml.load(logging_conf_file)
            logging.config.dictConfig(conf_yaml)
        print("Logging init OK")
    except:
        # file not exist: just use logging default.
        # however an error will be recorded
        print("Logging file failed")
        logging.basicConfig(
            format='[%(asctime)s %(levelname)s]%(name)s:%(message)s',
            level = logging.DEBUG
        )
        logging.error(
            "Config file %s is missing or not able to open.",
            filepath
        )


def RPiGPIOinit():
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
    GPIO.setmode(GPIO.BOARD)


# test
def _test1():
    _logger = logging.getLogger(__name__)
    loggerinit('./log/loggingconf.yml')
    RPiGPIOinit()
    _logger.debug("Test 01 finished")


if __name__ == '__main__':
    _test1()
