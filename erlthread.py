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
    - [x] class ErlThread
    - [x] spawn, send and halt
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
    'halt',
    'receive',
]

# Imports

import time
import threading
import queue


# Constants and global variables

DEFAULT_POLL_INTERVAL = 0.02

# Functions and decorators

# for the default behavior. May deprecate.

def default_(env, msg):
    return True


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


def receive(poll_action, time_out=None):
    """
    Receive *all* the message from current thread and poll them.
    if the poll_action returns True, the message is removed.
    After polling, the unprocessed message will be put back.
    This method will lock the thread's Condition lock.
    """
    th = threading.current_thread()
    cv = th.notification
    q = th.inbox
    env = th.env
    with cv:
        result = cv.wait(time_out)
        if result:
            # Received message. The only trigger of polling.
            msgs = []
            while not q.empty():
                msgs.append(q.get())
            for i in range(len(msgs)):
                message = msgs[i]
                # poll
                if poll_action(env, message):
                    del msgs[i]
            for message in msgs:
                q.put(message)
        return result


def erl_loop(enter_action, poll_action,
             tick_action, exit_action,
             poll_interval=DEFAULT_POLL_INTERVAL):
    """
    Loop and tick.
    """
    th = threading.current_thread()
    ev = th.exit_event
    # cv = th.notification
    # q = th.inbox
    env = th.env

    if poll_action is None:
        poll_action = dummy

    if enter_action is not None:
        enter_action(env)

    while not ev.is_set():
        if tick_action is not None:
            tick_timer = threading.Timer(poll_interval, tick_action, args=(env,))
        result = receive(poll_action, poll_interval)
        if not result and tick_action is not None:
            tick_timer.join()

    if exit_action is not None:
        exit_action(env)


def erl_empty():
    pass


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
        self.env = env or {}

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


# simple test

def _example_poll_handler(env, msg):
    if 'certainkey' in env:
        print(msg)
        send(env['certainkey'], 'test')
        if msg == 'test':
            threading.current_thread().exit_event.set()
    return True


def _test_1():
    env={}
    th1 = spawn(
        env=env, handler=erl_loop,
        handler_args=(None, _example_poll_handler,
                      None, None)
    )
    th2 = spawn(
        env=env, handler=erl_loop,
        handler_args=(None, dummy, None, None)
    )
    env['certainkey'] = th1

    th1.start()
    th2.start()
    time.sleep(1)
    send(th1, 'test')
    send(th2, 'test')
    time.sleep(1)
    halt(th1)
    th1.join()
    th2.join()
    print("_TEST_1")


def _test_2():
    env={}
    def print_msg(env, msg):
        print("Message:", msg)
    def send_loop(env, msg):
        send(msg[0], msg)
    th1 = spawn(
        env,
        message_handler=print_msg
    )
    th1.start()
    time.sleep(0.2)
    send(th1, 'hello')
    halt(th1)
    th1.join(1)
    print(th1.is_alive())


# main

if __name__ == '__main__':
    _test_2()


# DEPRECATED

# def _erl_poll(env, action_poll, poll_interval=DEFAULT_POLL_INTERVAL):
#     """
#     To poll over the action_poll when thread gets a message.
#
#     The action_poll is like this:
#         [
#             [predicator(env, msg), processor(env, msg)],
#             [predicator(env, msg), processor(env, msg)],
#             ...
#             [predicator(env, msg), processor(env, msg)]
#         ]
#     """
#     th = threading.current_thread()
#     # print("Current thread:", th)
#     # print("Thread inbox", th.inbox)
#     # print("Thread condition", th.notification)
#     # print("Thread exit", th.exit_event)
#     # print("Action poll:", action_poll)
#     # From here are the real code
#
#     q = th.inbox
#     cv = th.notification
#     ev = th.exit_event
#
#     while not ev.is_set():
#         # lock condition
#         with cv:
#             result = cv.wait(poll_interval)
#             if result:
#                 # start poll
#                 # get all message
#                 msgs = []
#                 while not q.empty():
#                     msgs.append(q.get())
#                 for i in range(len(msgs)):
#                     message = msgs[i]
#                     # poll
#                     for predicator, processor in action_poll:
#                         if predicator(env, message):
#                             processor(env, message)
#                             del msgs[i]
#                             break
#                 # put back
#                 for message in msgs:
#                     q.put(message)
#                 time.sleep(poll_interval / 2)
#             # poll over
#     # exit the thread
#     # debug
#     # print("The thread is dead.")


# def _erl_tick(env, action_poll, poll_interval=0.02):
#     """
#     Do some special job per poll_interval.
#     -------------------------------------------
#     The action_poll is like this:
#         [
#             func1(env),
#             func2(env),
#             ...
#         ]
#     and will call all func at once.
#     """
#     pass

# EOF
