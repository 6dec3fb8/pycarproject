#!/usr/bin/env python3
# coding=utf-8

# for emulating GPIO functions

BOARD = 1
BCM = 2
_gpio_mode = None


def setmode(mode):
    _gpio_mode = mode
    


def getmode():
    return _gpio_mode



