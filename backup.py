import os
import subprocess
import time
import logging
import zipfile
from datetime import datetime

DB_HOST = ''
DB_USER = ''
DB_PASSWORD = ''
DB_NAME = ''

BACKUP_DIR = 'C:\\Backup-py\\backups'
DATE_FORMAT = '%Y-%m-%d_%H-%M-%S'
MAX_BACKUP_AGE = 7  # Número de dias para manter os backups

BACKUP_FILE = ''
BACKUP_FILE_PATH = ''

# Configurando o logging
log_file_path = 'C:\\Backup-py\\Logs'
logging.basicConfig(filename=log_file_path, level=logging.ERROR, format='%(asctime)s [%(levelname)s]: %(message)s')

def create_backup():
    current_time = time.strftime(DATE_FORMAT)
    BACKUP_FILE = f'{DB_NAME}-{current_time}.sql'
    BACKUP_FILE_PATH = f'{BACKUP_DIR}\\{BACKUP_FILE}'
    
    mysqldump_cmd = f'mysqldump -h {DB_HOST} -u {DB_USER} -p{DB_PASSWORD} {DB_NAME} > {BACKUP_FILE_PATH}'
    print(mysqldump_cmd)
    input()

    try:
        subprocess.run(mysqldump_cmd, shell=True, check=True)
        
        print(f"Backup created successfully: {BACKUP_FILE_PATH}")
        input()
    except subprocess.CalledProcessError as e:
        error_message = f"Error creating backup: {e}"
        print(error_message)
        logging.error(error_message)

def compress_backup(backup_file_path):
    try:
        print('compress_backup')
        input()
        current_time = time.strftime(DATE_FORMAT)
        zip_file_path = f'{BACKUP_DIR}\\backup_{current_time}.zip'

        with zipfile.ZipFile(zip_file_path, 'w') as zip:
          # Adicione os arquivos que deseja compactar ao arquivo ZIP
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
        input()
        create_backup()
        compress_backup(os.path.join(BACKUP_DIR, f'{DB_NAME}-{time.strftime(DATE_FORMAT)}.sql'))
        remove_old_backups()
    except Exception as e:
        error_message = f"Unexpected error: {e}"
        print(error_message)
        logging.error(error_message)

if __name__ == "__main__":
    main()
