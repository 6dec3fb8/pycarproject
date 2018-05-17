#!/usr/bin/env python3
# coding=utf-8

# for multi logging test.

import logging

def testfunc_to_log(testvar1, testvar2, testvar3):
    logging.info("Var1: %s", testvar1)
    logging.warning("warning:var2: %s", testvar2)
    logging.error("Error: var3 is %s", testvar3)
    return "Vars: (%s, %s, %s)" % (testvar1, testvar2, testvar3)
