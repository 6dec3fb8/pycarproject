#!/usr/bin/env python3
# coding=utf-8

# test logger function

# well there is actually no use of this file.
# import ../logger.py
import logging


def test():
    logging.basicConfig(filename='example.log',
            filemode='w', level=logging.DEBUG)
    # test: normal logging
    logging.warning("Test warning")
    logging.info("Test info")
    logging.debug("Test debug info")
    logging.error("Test error")
    # logging.exception("Test exception")
    logging.critical("Test critical")

    # test: variables with logging
    teststr = 'Loggers are fun!'
    testvar = 16

    logging.debug("The var is %d", testvar)
    logging.info("The string is $s", teststr)


if __name__ == '__main__':
    test()
