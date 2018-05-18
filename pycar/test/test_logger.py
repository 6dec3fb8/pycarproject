#!/usr/bin/env python3
# coding=utf-8

# test logger function

# well there is actually no use of this file.
# import ../logger.py

# 2018-05-17 23:52 TODO:
#   a) logging with YAML config
#   b) logging init function wrapper


import logging
import logging.config
import yaml
import os


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


def test3():
    # test format
    logging.basicConfig(
            format='[%(levelname)s:%(module)s:%(lineno)d]:%(name)s@%(msecs)d %(message)s',
            filename='example.log',
            filemode='w',
            level=logging.DEBUG)

    # test named logger
    logger = logging.getLogger(__name__)

    # test: normal logger
    logger.warning("Test warning")
    logger.info("Test info")
    logger.debug("Test debug info")
    logger.error("Test error")
    # logger.exception("Test exception")
    logger.critical("Test critical")

    # multi module test
    logger.debug("before enter another module's function")
    from test_logger_multimodule import testfunc_to_log as tftl
    tftl("str1", "str2", "str3")
    logger.debug("After enter another module's func")


def test4():
    # file config: log/loggingconf.yml
    pwd = os.curdir
    print(pwd)
    print(os.listdir())
    # return
    logging_conf_file = open('./log/loggingconf.yml')
    conf_yaml = yaml.load(logging_conf_file)

    logging.config.dictConfig(conf_yaml)
    logger = logging.getLogger('logger2')

    # simple logging tests.

    # test: normal logger
    logger.warning("Test warning")
    logger.info("Test info")
    logger.debug("Test debug info")
    logger.error("Test error")
    # logger.exception("Test exception")
    logger.critical("Test critical")

    # multi module test
    logger.debug("before enter another module's function")
    from test_logger_multimodule import testfunc_to_log as tftl
    tftl("str1", "str2", "str3")
    logger.debug("After enter another module's func")


if __name__ == '__main__':
    test4()
