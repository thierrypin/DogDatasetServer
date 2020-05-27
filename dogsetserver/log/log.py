# -*- coding: utf-8 -*-

import logging

class Logger:
    __logger = None

    def __init__(self):
        if Logger.__logger is None:
            # create logger
            self.logger = logging.getLogger('sisu')
            self.logger.setLevel(logging.DEBUG)

            # create formatter
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            # create console handler
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            ch.setFormatter(formatter)

            self.logger.addHandler(ch)

            # create file
            sh = logging.FileHandler('var/logs/cerberus.log')
            sh.setLevel(logging.INFO)
            sh.setFormatter(formatter)

            self.logger.addHandler(sh)

            Logger.__logger = self
        else:
            raise Exception("This class is a singleton!")

    @staticmethod
    def check_init():
        if Logger.__logger is None:
            Logger()

    @staticmethod
    def debug(*args, **kwargs):
        Logger.check_init()
        Logger.__logger.logger.debug(*args, **kwargs)

    @staticmethod
    def info(*args, **kwargs):
        Logger.check_init()
        Logger.__logger.logger.info(*args, **kwargs)

    @staticmethod
    def warning(*args, **kwargs):
        Logger.check_init()
        Logger.__logger.logger.warning(*args, **kwargs)

    @staticmethod
    def error(*args, **kwargs):
        Logger.check_init()
        Logger.__logger.logger.error(*args, **kwargs)

    @staticmethod
    def exception(*args, **kwargs):
        Logger.check_init()
        Logger.__logger.logger.exception(*args, **kwargs)

    @staticmethod
    def critical(*args, **kwargs):
        Logger.check_init()
        Logger.__logger.logger.critical(*args, **kwargs)

