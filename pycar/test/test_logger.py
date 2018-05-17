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
    logging.info("The string is %s", teststr)

    # test multi-module
    logging.debug("before enter another module's function")
    from test_logger_multimodule import testfunc_to_log as tftl
    tftl("str1", "str2", "str3")
    logging.debug("After enter another module's func")


def test2():
    # test format
    logging.basicConfig(
            format='[%(levelname)s:%(module)s:%(lineno)d]:%(name)s@%(msecs)d %(message)s',
            filename='example.log',
            filemode='w',
            level=logging.DEBUG)
    
    # test: normal logging
    logging.warning("Test warning")
    logging.info("Test info")
    logging.debug("Test debug info")
    logging.error("Test error")
    # logging.exception("Test exception")
    logging.critical("Test critical")


if __name__ == '__main__':
    test2()
