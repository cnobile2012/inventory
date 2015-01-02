#
# setupenv.py
#
# SVN/CVS Info
#----------------------------------
# $Author: cnobile $
# $Date: 2010-08-29 22:22:56 -0400 (Sun, 29 Aug 2010) $
# $Revision: 12 $
#----------------------------------

import os
import logging, logging.handlers


LOGGER_NAME = "inventory"
# Valid levels NOTSET, DEBUG, INFO, WARNING, ERROR, and CRITICAL.
LOG_LEVEL = logging.DEBUG
LOG_FILENAME = "inventory.log"
BASE_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
LOG_PATH = BASE_PATH

def initializeLogging():
    """
    Initialize the logger.
    """
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(LOG_LEVEL)
    args=(os.path.join(LOG_PATH, 'logs', LOG_FILENAME), 'midnight', 1, 9)
    handler = logging.handlers.TimedRotatingFileHandler(*args)
    fmt = "%(asctime)s %(module)s %(funcName)s [line:%(lineno)d]" + \
          " %(levelname)s %(message)s"
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.info("Logging is initialized for the %s application.", LOGGER_NAME)

def getLogger(name=LOGGER_NAME):
    """
    Get the default logger or the named logger.

    @keyword name: The logger to get.
    @return: The logging object.
    """
    if name not in logging.Logger.manager.loggerDict:
        initializeLogging()

    return logging.getLogger(name)
