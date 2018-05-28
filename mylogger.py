#!/usr/bin/python3

# This file is the logging init functions.
# The logging-relevant things are put together here.

import logging
import yaml

# default config file is in ./log/loggingconf.yml
# however, it is not provided as a default param.
def loggerinit(filepath):
    # initialize the global logger config
    try:
        logging_conf_file = open(filepath)
        # with open(filepath) as logging_conf_file:
    except:
        # file not exist: just use logging default.
        # however an error will be recorded
        print("Logging file failed")
        logging.basicConfig(
            format='[%(asctime)s %(levelname)s]%(name)s:%(message)s',
            level = logging.DEBUG
        )
        logging.error(
            "Config file %s is missing or not able to open.",
            filepath
        )
        return False

    conf_yaml = yaml.load(logging_conf_file)
    print("mylogger.loggerinit: yaml loaded is:")
    print(conf_yaml)
    logging.config.dictConfig(conf_yaml)
    print("Logging init OK")
    return True


def getLogger(name):
    return logging.getLogger(name)
