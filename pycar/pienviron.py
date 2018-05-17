#!/usr/bin/env python3
# coding=utf-8

# module pienviron
# usage: init functions about GPIO and etc

# import necessary packages.
# here I make a fake package to emulate GPIO
try:
    import RPi.GPIO as GPIO
except:
    import fakeGPIO as GPIO

# global initialization
def init():
    pass


