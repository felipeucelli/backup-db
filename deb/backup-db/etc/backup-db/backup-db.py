# -*- coding: utf-8 -*-

# @autor: Felipe Ucelli
# @github: github.com/felipeucelli

# Built-in
import os
import logging
import subprocess
import configparser
from time import sleep
from datetime import datetime, date


def mount(ip: str, backup_folder: str, mount_point: str, username: str, password: str):
    """
    Role responsible for mounting the devices in the system
    :return:
    """
    try:
        if username != '' and password != '':
            result = subprocess.Popen(
                ['mount', '-t', 'cifs', f'//{ip}/{backup_folder}' , mount_point, '-o', f'username={username},password={password}'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            result = subprocess.Popen(
                ['mount', '-t', 'cifs', f'//{ip}/{backup_folder}', mount_point, '-o', 'password'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        result_stdout = result.stdout.read().decode()
        result_stderr = result.stderr.read().decode()

        if result_stderr != '':
            if os.path.exists(f'{mount_point}Backup'):  # Checks if the device is mounted.
                logging.info(f'{ip} - Already Mounted')
                copy_db(ip,backup_folder, mount_point)
            else:
                logging.error(f'{ip} - {result_stderr}')

        if result_stdout == '' and result_stderr == '':
            logging.info(f'{ip} - Successfully Mounted in {mount_point}')
            copy_db(ip,backup_folder, mount_point)

    except Exception as error:
        logging.critical(f'{ip} - {error}')


def umount(ip: str, backup_folder: str):
    """
    Role responsible for unmounting system devices
    :return:
    """
    try:
        result = subprocess.Popen(
            ['umount', '-t', 'cifs', f'//{ip}/{backup_folder}'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        result_stdout = result.stdout.read().decode()
        result_stderr = result.stderr.read().decode()

        if result_stderr != '':
            logging.error(f'{ip}/{backup_folder} - {result_stderr}')
        elif result_stdout == '':
            logging.info(f'{ip}/{backup_folder} - Successfully Unmounted')

    except Exception as error:
        logging.critical(f'{ip}/{backup_folder} - {error}')


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

    except Exception as error:
        logging.critical(f' {error}')

def copy_db(ip: str, backup_folder: str, mount_point: str):
    """
    Copy the zipped file into the mounted device folder
    :return:
    """
    try:
        file = zip_db(db=config.get('DATABASE', 'path'))
        """
        It is necessary to select a folder inside the mounted device, 
        otherwise the file will be saved within the linux and windows system
        """
        result = subprocess.Popen(
            ['cp', '-r', '-v', f'{file}', f'{mount_point}'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        result_stdout = result.stdout.read().decode()
        result_stderr = result.stderr.read().decode()

        if result_stdout != '':
            logging.info(f'{ip}/{backup_folder} - {result_stdout}')
            umount(ip, backup_folder)
        if result_stderr != '':
            logging.error(f'{ip}/{backup_folder} - {result_stderr}')
            umount(ip, backup_folder)

    except Exception as error:
        logging.critical(f'{ip}/{backup_folder} - {error}')


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

    except Exception as error:
        logging.critical(f'{error}')


def main(section: list):
    """
    Check the time and perform the backup
    :return:
    """
    while True:
        now = str(datetime.now().time()).split('.')[0]
        day = str(date(date.today().year, date.today().month, date.today().day).weekday())
        sleep(1)
        for items in section:
            item = dict(config.items(items))
            if now in item['time'] and day in item['days']:
                mount(item['ip'], item['backup_folder'], item['mount_point'], item['username'], item['password'])
                del_temp_folder(db=config.get('DATABASE', 'path'))


config = configparser.RawConfigParser()
config.read('/etc/backup-db/backup-db.conf')

log_format = '%(asctime)s - %(levelname)s : %(message)s'
log_path = config.get('LOG', 'path')
logging.basicConfig(
    filename=log_path,
    level=logging.DEBUG,
    format=log_format)

if __name__ == '__main__':
    main(list(config.sections()[2:]))
