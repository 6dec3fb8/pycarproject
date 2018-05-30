#!/usr/bin/python3

#   This module is used to control the Raspi camera using its native
# package `picamera` and process its image using the opencv.
#
# structure
# (temp):
# thread,0.5s->data->queue
#
# A contour list is:
# [ (x, y, area, contour), * ]
# and will sort by area.

__all__ = [
    'ContourProducingThread',
]
# imports

import logging
import cv2
import threading
import time
import queue
import numpy as np
from picamera import PiCamera

TC_RED = (0, 0, 255)
TC_GREEN = (0, 255, 0)
TC_BLUE = (255, 0, 0)

_contour_color = TC_RED
_center_color = TC_GREEN

# functions


# classes

class ContourProducingThread(threading.Thread):
    pass

# tests

def _test_1():
    print('TEST 01')


if __name__ == '__main__':
    _test_1()
