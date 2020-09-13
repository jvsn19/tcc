import os
import sys
import logging

current_dir = os.getcwd()

def create_log_folder():
    '''
    The default log path is {pwd}/logs
    '''
    python_version = sys.version_info

    if python_version < (3,8):
        logging.warning(f'The current python version \n {sys.version} \nis not recomended. Do you want to proceed? Y/N')
        answer = input().lower()

        while answer not in ('y', 'n', ''):
            answer = input('y/n').lower()

        if answer == 'n':
            return 0

    log_path = f'{current_dir}/logs'

    if not os.path.exists(log_path) or not os.path.isdir(log_path):
        try:
            os.mkdir(log_path, 755)
        except Exception as e:
            logging.critical(f'Cannot create the new directory {log_path}', e.args)
            return -1

    return 0


def main():
    '''
    This class do the initial setup for the user
    '''
    print(sys.version)
    create_log_folder()

if __name__ == '__main__':
    main()
