#!/usr/bin/env python3
# coding=utf-8

# test logger function

# well there is actually no use of this file.
# import ../logger.py
import logging


def test():
    logging.warning("Test warning")
    logging.info("Test info")
    logging.debug("Test debug info")
    logging.error("Test error")
    # logging.exception("Test exception")
    logging.critical("Test critical")


if __name__ == '__main__':
    test()
