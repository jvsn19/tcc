from datetime import datetime
from enum import Enum
import os

LOG_PATH = './logs'

class LogTypes(Enum):
    INFO = 0
    WARNING = 1
    ERROR = 2


class Logger:
    '''
    This class implements a Logger. An alternative for this is using the logging from python
    import logging
    '''
    class __LoggerSingleton:
        def __init__(self):
            # Check if exists a log file
            if not os.path.exists(LOG_PATH) or not os.path.isfile(LOG_PATH):
                self._create_log()

             # Private Methods
        def _create_log(self):
            now = self._get_now()

            with open(LOG_PATH, 'w+') as log_file:
                log_file.write(f'Starting Log at {now}')

        def _get_now(self):
            return str(datetime.now())

        def _log(self, log_type: LogTypes, message: str):
            now = self._get_now()

            with open(LOG_PATH, 'a+') as log_file:
                log_file.write(f'[{now}][{log_type}] - {message}')

    _instance = None

    @property
    def instance(self):
        if self._instance is None:
            self._instance = self.__LoggerSingleton()

        return self._instance

    def _get_instance(self):
        if self._instance is None:
            self._instance = self.__LoggerSingleton()

        return self._instance

    # Public Methods
    @classmethod
    def log_error(cls, message: str):
        cls._get_instance(cls)._log(LogTypes.ERROR, message + '\n')

    @classmethod
    def log_warning(cls, message: str):
        cls._get_instance(cls)._log(LogTypes.WARNING, message + '\n')


    @classmethod
    def log_info(cls, message: str):
        cls._get_instance(cls)._log(LogTypes.INFO, message + '\n')
