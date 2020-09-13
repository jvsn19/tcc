from datetime import datetime
from enum import Enum
import os

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
            if not os.path.exists(LOG_PATH) or not os.path.isfile(LOG_PATH):
                self._create_log()

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

    def __init__(self):
        print("oi")
        self._log_path = None
        self._log_level = None

    @property
    def log_path(self):
        return self._log_path

    @property
    def log_level(self):
        return self._log_level

    @log_path.setter
    def log_path(self, new_log_path):
        self._log_path = new_log_path

    @log_level.setter
    def log_level(self, new_log_level):
        self._log_level = new_log_level

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
