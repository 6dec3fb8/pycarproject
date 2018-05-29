#!/usr/bin/python3

# This module is used to simulate the behavior of Erlang threads.
# It is really convenient to handle multi-threading things.

#      8      16      24      32      40      48      56      64      72      80
# ruler:-------+-------+-------+-------+-------+-------+-------+-------+-------+

"""
Python erlang thread simulate module
--------------------------------------------------------------

Basic structure:
    class ErlThread(threading.Thread):
        the thread to use.
    def spawn:
        create a thread (but not invoking it).
    def send:
        send a message (like dict, list, etc) to a thread.
    def halt:
        stop a thread by setting an event of that thread

--------------------------------------------------------------

TODO:
    - [ ] class ErlThread
    - [ ] spawn, send and halt
    - [ ] test

"""

# Future imports are written before # import.
# And the __all__, __version, __author__ are here too.


__version__ = '0.0'
__author__ = 'HexFaker'

__all__ = [
    'ErlThread',
    'spawn',
    'send',
    'halt'
]

# Imports

import time
import threading
import queue


# Constants and global variables


# Functions and decorators

def default_(msg):
    return True


def dummy(msg):
    pass


def spawn(name=None, receive_methods=(default_, dummy), *args, **kwargs):
    pass


def send(thread, message):
    pass


def halt(thread):
    pass


# Classes and metaclasses

class ErlThread(threading.Thread):
    pass


# simple test

def _test_1():
    print("_TEST_1")


# main

if __name__ == '__main__':
    _test_1()
