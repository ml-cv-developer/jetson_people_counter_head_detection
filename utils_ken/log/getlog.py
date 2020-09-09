import sys
import logging
from logging.handlers import TimedRotatingFileHandler

FORMATLOG = logging.Formatter('%(asctime)-12s : %(name)-5s : [%(levelname)-5s] : %(message)5s')
# setup console logger
def get_console_handler() :
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(FORMATLOG)
    return console_handler

def get_file_handler(logfile) :
    file_hander = TimedRotatingFileHandler(logfile, when="midnight",interval=1, backupCount=10)
    file_hander.setFormatter(FORMATLOG)
    # file_hander.setLevel(logging.INFO)
    return file_hander
# 
# logname, logfile to save model
# 
def get_logger(logname, logfile) :
    logger = logging.getLogger(logname)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler(logfile))
    # with this pattern, it's rarely necessary to propagate the error up to paren
    logger.propagate = False
    return logger

def get_logger_console(logname) :
    logger = logging.getLogger(logname)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_console_handler())

    return logger

def get_logger_file(logname, logfile) :
    logger = logging.getLogger(logname)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_file_handler(logfile))
    # with this pattern, it's rarely necessary to propagate the error up to paren
    logger.propagate = False
    
    return logger