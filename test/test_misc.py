#!/usr/bin/python3

# test for misc.py

import logging

import sys
from os import path
print(path.abspath('..'))
sys.path.append(
    path.join(
        path.abspath(".."),
        'pycarproject'
    )
)
print(sys.path)
import pycar
misc = pycar.misc
# import from parent. Got some hacks here.
# if __name__ == '__main__':
#     if __package__ is None:
#         import sys
#         # from os import path
#         sys.path.append('~/pycarproject/')
#         from . import pycar
# else:
# # print(os.curdir)
# # print(os.listdir())
# # print(__file__, __package__, __name__)
# # sys.path.append('..')
# # print(sys.path)
#     from ..pycar import misc


def test1():
    print("Test 01 for module misc")
    misc.loggerinit('log/loggingconf.yml')
    logger =logging.getLogger(__name__)
    logger.debug("Test01 in %s: testing logger", __name__)
    print("Test RPi sim/real init")
    misc.RPiGPIOinit()
    print("Test over.")


if __name__ == '__main__':
    test1()
