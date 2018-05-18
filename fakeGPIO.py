#!/usr/bin/env python3
# coding=utf-8

# for emulating GPIO functions
import logging

BOARD = 1
BCM = 2
_gpio_mode = None


def setmode(mode):
    global _gpio_mode
    print("setmode", __name__)
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



