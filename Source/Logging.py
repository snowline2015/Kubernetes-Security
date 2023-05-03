import os
import logging


# Add custom log levels to logging module
LOW = 21
MEDIUM = 22
HIGH = 23
logging.addLevelName(LOW, "LOW")
logging.addLevelName(MEDIUM, "MEDIUM")
logging.addLevelName(HIGH, "HIGH")



class Logging:
    def __init__(self, log_name: str = 'Log/KUBE_SEC.log', level: str = 'INFO', message: str = ''):
        self.FILE_NAME = log_name
        self.LEVEL = level
        self.MESSAGE = message

        if not os.path.exists('Log'):
            os.mkdir('Log')

        if self.LEVEL not in ['INFO', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL']:
            raise ValueError('Invalid log level')
        
        self.LOGGER = logging.getLogger()
        self.FORMAT = logging.Formatter('%(asctime)s|%(levelname)s|%(message)s')
        self.HANDLER = logging.FileHandler(self.FILE_NAME)
        self.HANDLER.setFormatter(self.FORMAT)
        self.LOGGER.addHandler(self.HANDLER)


    def log(self):
        if self.LEVEL == 'INFO':
            self.LOGGER.setLevel(logging.INFO)
            self.LOGGER.log(logging.INFO, self.MESSAGE)

        elif self.LEVEL == 'LOW':
            self.LOGGER.setLevel(LOW)
            self.LOGGER.log(LOW, self.MESSAGE)

        elif self.LEVEL == 'MEDIUM':
            self.LOGGER.setLevel(MEDIUM)
            self.LOGGER.log(MEDIUM, self.MESSAGE)

        elif self.LEVEL == 'HIGH':
            self.LOGGER.setLevel(HIGH)
            self.LOGGER.log(HIGH, self.MESSAGE)

        elif self.LEVEL == 'CRITICAL':
            self.LOGGER.setLevel(logging.CRITICAL)
            self.LOGGER.log(logging.CRITICAL, self.MESSAGE)
