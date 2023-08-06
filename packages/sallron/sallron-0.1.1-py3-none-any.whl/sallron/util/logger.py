#!/usr/bin/env python

from sallron.util import settings
import logging
import traceback
import sys
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

def setup_logger(level = logging.INFO):
    '''Prints logger info to terminal'''
    logger = logging.getLogger()
    logger.setLevel(level)
    ch = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

def setup_logbook(name, extension='.txt', level=logging.INFO):
    """Setup logger that writes to file, supports multiple instances with no overlap.
       Available levels: DEBUG|INFO|WARN|ERROR"""
    formatter = logging.Formatter(fmt='%(asctime)s.%(msecs)03d (%(name)s) - %(message)s', datefmt='%d-%m-%y %H:%M:%S')
    date = datetime.today().strftime('%Y-%m-%d')
    log_path = str(settings.LOG_DIR + name +'_' + date + extension)
    try:
        handler = RotatingFileHandler(log_path, maxBytes=settings.MAX_LOG_SIZE, backupCount=1)
    except FileNotFoundError:
        os.mkdir(settings.LOG_DIR)
        handler = RotatingFileHandler(log_path, maxBytes=settings.MAX_LOG_SIZE, backupCount=1)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

# Global error_logger so all functions can use it
error_logger = logging.getLogger('errors')

def setup_error_logger():
    '''Basic handler setup for error_logger'''
    date = datetime.today().strftime('%Y-%m-%d')
    log_path = settings.LOG_DIR + 'errors_' + date + '.txt'

    global error_logger
    error_logger = logging.getLogger('errors')
    handler = logging.handlers.RotatingFileHandler(log_path, maxBytes=settings.MAX_LOG_SIZE, backupCount=1) # stream=sys.stdout
    error_logger.addHandler(handler)

def close_error_logger():
    error_logger.removeHandler(error_logger.handlers[0])
    return

def log_exception(exc_type, exc_value, exc_traceback):
    '''Log unhandled exceptions
    set sys.excepthook = logger.log_exception on main file for it to work'''
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    error_logger.info('-----------------------------------------------------------------')
    error_logger.info(str(datetime.now()))
    error_logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    error_logger.info('-----------------------------------------------------------------')
    error_logger.info('')
    message = ''.join(str(exc_type) + str(exc_value)).join(traceback.format_tb(exc_traceback))
    return

def log_error(message):
    '''Log handled errors'''
    error_logger.info('-----------------------------------------------------------------')
    error_logger.info(str(datetime.now()))
    error_logger.error(message)
    error_logger.info('-----------------------------------------------------------------')
    error_logger.info('')
    return