#!/usr/bin/env python3
# coding=utf-8

# for multi logging test.

import logging

def testfunc_to_log(testvar1, testvar2, testvar3):
    logger = logging.getLogger(__name__)
    logger.info("Var1: %s", testvar1)
    logger.warning("warning:var2: %s", testvar2)
    logger.error("Error: var3 is %s", testvar3)
    return "Vars: (%s, %s, %s)" % (testvar1, testvar2, testvar3)
