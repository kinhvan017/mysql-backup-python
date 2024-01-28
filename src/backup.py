import os
import subprocess
import time
import logging
import zipfile
from datetime import datetime

DB_HOST = 'localhost'
DB_USER = 'your_username'
DB_PASSWORD = 'your_password'
DB_NAME = 'your_database_name'

BACKUP_DIR = 'your_backup_files_path'
DATE_FORMAT = '%Y-%m-%d_%H-%M-%S'
MAX_BACKUP_AGE = 7

BACKUP_FILE = ''
BACKUP_FILE_PATH = ''

# Configuring o logging
log_file_path = 'your_log_files_path'
logging.basicConfig(filename=log_file_path, level=logging.ERROR, format='%(asctime)s [%(levelname)s]: %(message)s')

def create_backup():
    current_time = time.strftime(DATE_FORMAT)
    BACKUP_FILE = f'{DB_NAME}-{current_time}.sql'
    BACKUP_FILE_PATH = f'{BACKUP_DIR}\\{BACKUP_FILE}'
    
    mysqldump_cmd = f'mysqldump -h {DB_HOST} -u {DB_USER} -p{DB_PASSWORD} {DB_NAME} > {BACKUP_FILE_PATH}'

    try:
        subprocess.run(mysqldump_cmd, shell=True, check=True)
        
        print(f"Backup created successfully: {BACKUP_FILE_PATH}")
    except subprocess.CalledProcessError as e:
        error_message = f"Error creating backup: {e}"
        print(error_message)
        logging.error(error_message)

def compress_backup():
    try:
        current_time = time.strftime(DATE_FORMAT)
        zip_file_path = f'{BACKUP_DIR}\\backup_{current_time}.zip'

        with zipfile.ZipFile(zip_file_path, 'w') as zip:
          zip.write(BACKUP_FILE_PATH)

        os.remove(BACKUP_FILE_PATH)

        print(f"Backup compressed successfully: {zip_file_path}")
    except subprocess.CalledProcessError as e:
        error_message = f"Error compressing backup: {e}"
        print(error_message)
        logging.error(error_message)

def remove_old_backups():
    current_time = datetime.now()
    for entry in os.scandir(BACKUP_DIR):
        if entry.is_file() and entry.name.endswith('.zip'):
            delta = current_time - datetime.fromtimestamp(entry.stat().st_mtime)
            if delta.days > MAX_BACKUP_AGE:
                try:
                    os.remove(entry.path)
                    print(f"Old backup removed successfully: {entry.path}")
                except Exception as e:
                    error_message = f"Error removing old backup '{entry.path}': {e}"
                    print(error_message)
                    logging.error(error_message)

def main():
    try:
        create_backup()
        compress_backup()
        remove_old_backups()
    except Exception as e:
        error_message = f"Unexpected error: {e}"
        print(error_message)
        logging.error(error_message)

if __name__ == "__main__":
    main()
