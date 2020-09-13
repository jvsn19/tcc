from ._enums import LogTypes
import os

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

    instance = None

    def _get_instance(self):
        if self.instance is None:
            self.instance = self.__LoggerSingleton()

        return self.instance

    # Public Methods
    @classmethod
    def log_error(cls, message: str):
        cls._get_instance(cls)._log(self, LogTypes.ERROR, message)

    @classmethod
    def log_warning(cls, message: str):
        cls._get_instance(cls)._log(self, LogTypes.WARNING, message)


    @classmethod
    def log_info(cls, message: str):
        cls._get_instance(cls)._log(self, LogTypes.INFO, message)
