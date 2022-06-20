import logging
from logging import handlers
import os


str_format = '[%(asctime)s] - [%(name)s:%(lineno)s] - [%(levelname)s] >> %(message)s'
date_format = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(fmt=str_format, datefmt=date_format)


def get_file_handler():
    if not os.path.isdir('logs'):
        os.mkdir('logs')
    file_handler = logging.handlers.RotatingFileHandler("logs/log.log")
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)
    return file_handler


def get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    return stream_handler


def get_logger(name):
    """Create logger with settings from 'logger_app'"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_file_handler())
    logger.addHandler(get_stream_handler())
    return logger
