import os
import sys
import logging
import yaml

from utils.logger import Logger

ROOT_DIR = os.getcwd()

def configure_logger(log_level, log_path):
    Logger.log_level = log_level
    Logger.log_path = log_path

    _create_log_folder()

def _create_log_folder(log_path):
    if not os.path.exists(log_path) or not os.path.isdir(log_path):
        try:
            os.mkdir(log_path)
        except Exception as e:
            logging.critical(f'Cannot create the new directory {log_path}', e.args)
            return -1

    return 0

def main():
    '''
    This class do the initial setup for the user
    '''
    python_version = sys.version_info

    if python_version < (3,8):
        logging.warning(f'The current python version \n {sys.version} \nis not recomended. Do you want to proceed? Y/N')
        answer = input().lower()

        while answer not in ('y', 'n', ''):
            answer = input('y/n').lower()

        if answer == 'n':
            return 0

if __name__ == '__main__':
    main()
