#!/usr/bin/env python3
# coding=utf-8

# for emulating GPIO functions
import logging

BOARD = 1
BCM = 2
IN = -1
OUT = -2
_gpio_mode = None


def setmode(mode):
    global _gpio_mode
    # print("setmode", __name__)
    _gpio_mode = mode
    logger = logging.getLogger(__name__)
    logger.info("Set mode to %s",
                 ("BOARD" if _gpio_mode==BOARD else "BCM"))


def getmode():
    global _gpio_mode
    logger = logging.getLogger(__name__)
    logger.info("Returns mode %s.",
                 ("BOARD" if _gpio_mode==BOARD else "BCM"))
    return _gpio_mode


def cleanup(port=None):
    logger = logging.getLogger(__name__)
    if port is None:
        logger.warning("GPIO cleans up ALL ports")
    else:
        logger.info("GPIO cleanup port %d", port)


def setup(port, iomode):
    logger = logging.getLogger(__name__)
    logger.info("Set port %d to mode %s",
                port, "OUT" if iomode==OUT else "IN")

# class PWM for motor control.
class PWM:
    """
    A fake PWM class for testing.
    """
    def __init__(self, channel, frequency):
        self.channel = channel
        self.frequency = frequency
        self._ison = False
        self.dutycycle = 0
        self.logger = logging.getLogger(__name__)
        self.logger.info("PWM Ch#%d created at freq %d", self.channel, self.frequency)


    def start(self, dutycycle):
        self._ison = True
        self.dutycycle = dutycycle
        self.logger.info("PWM Ch#%d starts at dc=%d", self.channel, self.dutycycle)


    def ChangeFrequency(self, freq):
        self.frequency = freq
        self.logger.info("PWM Ch#%d changed frequency to %d", self.channel, self.frequency)


    def ChangeDutyCycle(self, dc):
        self.dutycycle = dc
        self.logger.info("PWM Ch#%d changed dutycycle to %d", self.channel, self.dutycycle)


    def stop(self):
        self._ison = False
        self.logger.info("PWM Ch#%d stops", self.channel)

