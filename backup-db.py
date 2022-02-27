# -*- coding: utf-8 -*-

# @autor: Felipe Ucelli
# @github: github.com/felipeucelli

# Built-in
import os
import logging
import subprocess
from time import sleep
from datetime import datetime


def mount(address: list, db: str):
    """
    Role responsible for mounting the devices in the system
    :param address: List of device addresses
    :param db: Database path
    :return:
    """
    for i in range(len(address)):
        try:
            result = subprocess.Popen(
                ['mount', '-t', 'cifs', address[i][0], address[i][1], '-o', 'password'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            result_stdout = result.stdout.read().decode()
            result_stderr = result.stderr.read().decode()

            if result_stderr != '':
                if os.path.exists(f'{address[i][1]}Backup'):  # Checks if the device is mounted.
                    logging.info(f'{address[i][0]} - Already Mounted')
                    copy_db(address=address[i], db=db)
                else:
                    logging.error(f'{address[i][0]} - {result_stderr}')

            if result_stdout == '' and result_stderr == '':
                logging.info(f'{address[i][0]} - Successfully Mounted in {address[i][1]}')
                copy_db(address=address[i], db=db)

        except Exception as erro:
            logging.critical(f'{address[i][0]} - {erro}')


def umount(address: str):
    """
    Role responsible for unmounting system devices
    :param address: Address to be unmounted
    :return:
    """
    try:
        result = subprocess.Popen(
            ['umount', '-t', 'cifs', address],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        result_stdout = result.stdout.read().decode()
        result_stderr = result.stderr.read().decode()

        if result_stderr != '':
            logging.error(f'{address} - {result_stderr}')
        elif result_stdout == '':
            logging.info(f'{address} - Successfully Unmounted')

    except Exception as erro:
        logging.critical(f'{address} - {erro}')


def zip_db(db: str) -> str:
    """
    Function responsible for compressing the database in a .zip file
    :param db: Database path
    :return: Returns the full path of the database
    """
    try:
        db_path = '/'.join(db.split('/')[:-1]) + '/'
        if not os.path.exists(f'{db_path}temp'):
            result = subprocess.Popen(
                ['mkdir', '-v', f'{db_path}temp'],  # Add the "-r" parameter to compress the directory recursively
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            result_stdout = result.stdout.read().decode()
            result_stderr = result.stderr.read().decode()

            logging.info(f'{result_stdout}') if result_stdout != '' else logging.error(f'{result_stderr}')

        now = str(datetime.now()).split('.')[0]
        file = f'{db_path}temp/Backup - {now}.zip'
        result = subprocess.Popen(
            ['zip', '-v', f'{file}', f'{db}'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        result_stdout = result.stdout.read().decode()
        result_stderr = result.stderr.read().decode()

        logging.info(f'{result_stdout}') if result_stdout != '' else logging.error(f'{result_stderr}')

        return file

    except Exception as erro:
        logging.critical(f' {erro}')


def copy_db(address: list, db: str):
    """
    Copy the zipped file into the mounted device folder
    :param address: List of device addresses
    :param db: Database path
    :return:
    """
    try:
        file = zip_db(db=db)
        """
        It is necessary to select a folder inside the mounted device, 
        otherwise the file will be saved within the linux and windows system
        """
        result = subprocess.Popen(
            ['cp', '-r', '-v', f'{file}', f'{address[1]}Backup'],  # The files will be copied into the "Backup" folder
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        result_stdout = result.stdout.read().decode()
        result_stderr = result.stderr.read().decode()

        if result_stdout != '':
            logging.info(f'{address[0]} - {result_stdout}')
            umount(address=address[0])
        if result_stderr != '':
            logging.error(f'{address[0]} - {result_stderr}')
            umount(address=address[0])

    except Exception as erro:
        logging.critical(f'{address[0]} - {erro}')


def del_temp_folder(db: str):
    """
    Delete the temporary folder
    :param db: Database path
    :return:
    """
    try:
        db_path = '/'.join(db.split('/')[:-1]) + '/'
        if os.path.exists(f'{db_path}temp'):
            result = subprocess.Popen(
                ['rm', '-r', '-v', f'{db_path}temp'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            result_stdout = result.stdout.read().decode()
            result_stderr = result.stderr.read().decode()

            logging.info(f'{result_stdout}') if result_stdout != '' else logging.error(f'{result_stderr}')

    except Exception as erro:
        logging.critical(f'{erro}')


def main(address: list, list_time: list, db: str):
    """
    Check the time and perform the backup
    :param address: List of device addresses
    :param list_time: List of times to call the algorithm
    :param db: Database path
    :return:
    """
    while True:
        sleep(1)
        for time in list_time:
            now = str(datetime.now().time()).split('.')[0]
            if now == time:
                mount(address=address, db=db)
                del_temp_folder(db=db)


log_format = '%(asctime)s - %(levelname)s : %(message)s'
log_path = '/var/log/backup-server.log'  # Full path to save the log file
logging.basicConfig(
    filename=log_path,
    level=logging.DEBUG,
    format=log_format)

_address = [
    # Devices IP               # Path to mount on linux system
    ('//192.168.0.114/share_folder', '/opt/mount_folder1/'),
    ('//192.168.0.115/share_folder', '/opt/mount_folder2/')
]

_db = '/FULL/PATH/DATABASE'  # Only one file is allowed for backup

_time = ['09:00:00', '19:00:00']  # Examples of hours

if __name__ == '__main__':
    main(address=_address, list_time=_time, db=_db)
