#!/usr/bin/env python3
# coding=utf-8

# main entry

# import pycar
from pycar import misc, motor

import time

def main():
    md = motor.MotorDifferentor(12, 16, 18, 11)
    md.set_speed(30, 0)
    time.sleep(1)
    md.set_speed(0, 0)

    print("Dummy")


if __name__ == '__main__':
    misc.init()
    main()

