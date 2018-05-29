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


"""

# Future imports are written before # import.
# And the __all__, __version, __author__ are here too.


__version__ = '0.1'
__author__ = 'HexFaker'

__all__ = [
    'ErlThread',
    'spawn',
    'send',
    'halt',
]

# Imports

import time
import threading
import queue


# Constants and global variables

DEFAULT_POLL_INTERVAL = 0.02

# Functions and decorators

# for the default behavior. May deprecate.


def dummy(env, msg):
    # debug
    print("Dummy received msg:", msg)
    pass

# Thread factory. Will not run at creation.

def spawn(env=None, name=None,
          poll_interval = DEFAULT_POLL_INTERVAL,
          message_handler=dummy,
          tick_action=None):
    env = env or {}
    th = ErlThread(
        env, name, poll_interval,
        message_handler, tick_action
    )
    return th


# Other important methods.

def send(thread, message):
    """Send the message to the thread and notify the thread to receive the message."""
    q = thread.inbox
    cv = thread.notification
    with cv:
        q.put(message)
        cv.notify()


def halt(thread, timeout=None):
    """
    Halt the thread.
    (DEPRECATED)You need join manually to wait for the thread to end.
    (update 1)  This function will automatically join for you.
    """
    ev = thread.exit_event
    ev.set()
    if time is None:
        thread.join()
    else:
        thread.join(timeout)


# for precious ticking


def ticker(ev, job, *args):
    job(*args)
    while not ev.is_set():
        pass


def halt_ticker(ev):
    ev.set()


# Classes and metaclasses

class ErlThread(threading.Thread):
    """
    The erlang-like thread.
    ------------------------------------------------------------

    basic structure:
        - A queue inbox
        - An event to tell the thread to check the inbox
          (or to use an condition)
        - An event to tell the thread to exit.
        - An inner lock to makesure that all the polling are atomic
          (or to use the condition instead)
        - getters and setters to the inbox, notice_event(or condition)
          and the exit_event(will use property)

    """
    def __init__(self, env=None, name=None,
                 poll_interval=DEFAULT_POLL_INTERVAL,
                 message_handler=None,
                 tick_action=None):
        """
        Constructor.
        The parameter are almost the same as Thread.
        """
        # if not args:
        #     args = ([[default_, dummy]],)
        super(ErlThread, self).__init__(name = name)
        self._inbox = queue.Queue()
        self._condition_getmsg = threading.Condition()
        self._exit_event = threading.Event()
        self._message_handler = message_handler
        self._tick_action = tick_action
        self._poll_interval = poll_interval
        self._env = env or {}

    def run(self):
        while not self._exit_event.is_set():
            if self._tick_action is not None:
                ev = threading.Event()
                tickth = threading.Thread(
                    target=ticker,
                    args=(ev, self._tick_action, self.env)
                )
                tick_timer = threading.Timer(
                    self._poll_interval,
                    halt_ticker,
                    args=(ev,)
                )
                tickth.start()
                tick_timer.start()
            with self._condition_getmsg:
                result = self._condition_getmsg.wait(self._poll_interval)
                if result:
                    while not self._inbox.empty():
                        msg = self._inbox.get()
                        self._message_handler(self.env, msg)
                    if self._tick_action is not None:
                        tick_timer.join(self._poll_interval)

    @property
    def inbox(self):
        return self._inbox

    @inbox.setter
    def inbox(self, value):
        raise RuntimeError("Cannot change the inbox of a thread!")

    @property
    def notification(self):
        return self._condition_getmsg

    @notification.setter
    def notification(self, value):
        raise RuntimeError("Cannot change the Condition of a thread!")

    @property
    def exit_event(self):
        return self._exit_event

    @exit_event.setter
    def exit_event(self, value):
        raise RuntimeError("Cannot change the exit event of a thread!")

    @property
    def env(self):
        return self._env

    @env.setter
    def env(self, value):
        if isinstance(value, dict):
            self._env = value
        else:
            raise ValueError("Environment should be a dict!")


# simple test


def _test_2():
    env={}
    def print_msg(env, msg):
        print("Message:", msg)
    def tick_test(env):
        print('Tick')
        send(env['t1'], 'hello')
    def send_loop(env, msg):
        send(msg[0], msg)
    th1 = spawn(
        message_handler=print_msg
    )
    th2 = spawn(
        tick_action=tick_test
    )
    env['t1'] = th1
    th2.env = env
    th1.start()
    th2.start()
    time.sleep(0.2)
    send(th1, 'hello')
    halt(th1)
    halt(th2)
    print(th1.is_alive())
    print(th2.is_alive())


# main

if __name__ == '__main__':
    _test_2()

