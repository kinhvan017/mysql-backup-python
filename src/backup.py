import os
import subprocess
import time
import logging
import zipfile
import requests
from ms_graph import generate_access_token, GRAPH_API_ENDPOINT
from datetime import datetime

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'your_password'
DB_NAME = 'your_database_name'

APP_ID = 'your_app_id'
CLIENT_SECRET = 'your_client_secret'
SCOPES = ['Files.ReadWrite.All']

PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
BACKUP_DIR = os.path.join(PROJECT_DIR, 'backups')
LOG_DIR = os.path.join(PROJECT_DIR, 'Logs')

DATE_FORMAT = '%Y-%m-%d_%H-%M-%S'
MAX_BACKUP_AGE = 7

log_file_path = os.path.join(LOG_DIR, 'backup_log.txt')
logging.basicConfig(filename=log_file_path, level=logging.ERROR, format='%(asctime)s [%(levelname)s]: %(message)s')

def create_backup():
    current_time = time.strftime(DATE_FORMAT)
    backup_file = f'{DB_NAME}-{current_time}.sql'
    backup_file_path = os.path.join(BACKUP_DIR, backup_file)

    mysqldump_cmd = f'mysqldump -h {DB_HOST} -u {DB_USER} -p{DB_PASSWORD} {DB_NAME} > {backup_file_path}'

    try:
        subprocess.run(mysqldump_cmd, shell=True, check=True)
        print(f"Backup created successfully: {backup_file_path}")
        return backup_file_path
    except subprocess.CalledProcessError as e:
        error_message = f"Error creating backup: {e}"
        print(error_message)
        logging.error(error_message)
        return None

def compress_backup(backup_file_path):
    try:
        current_time = time.strftime(DATE_FORMAT)
        zip_file_name = f'backup_{current_time}.zip'
        zip_file_path = os.path.join(BACKUP_DIR, zip_file_name)

        with zipfile.ZipFile(zip_file_path, 'w') as zip:
            zip.write(backup_file_path)

        os.remove(backup_file_path)

        print(f"Backup compressed successfully: {zip_file_path}")
        return zip_file_path
    except subprocess.CalledProcessError as e:
        error_message = f"Error compressing backup: {e}"
        print(error_message)
        logging.error(error_message)
        return None

def remove_old_backups_os():
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

def save_files_ondrive(zip_file_path):
    try:
        access_token = generate_access_token(APP_ID, SCOPES)

        headers = {
            'Authorization': 'Bearer ' + access_token['access_token']
        }

        one_drive_folder_id = 'your_one_drive_folder_id'

        with open(zip_file_path, 'rb') as upload:
            media_content = upload.read()

        response = requests.put(
            f"{GRAPH_API_ENDPOINT}/me/drive/items/{one_drive_folder_id}:/{os.path.basename(zip_file_path)}:/content",
            headers=headers,
            data=media_content
        )

        print(response.json())
    except Exception as e:
        error_message = f"Error saving backup in OneDrive: {e}"
        print(error_message)
        logging.error(error_message)

def remove_old_backups_onedrive():
    try:
        access_token = generate_access_token(APP_ID, SCOPES)
        one_drive_folder_id = 'your_one_drive_folder_id'

        onedrive_files = get_files_in_onedrive(one_drive_folder_id, access_token)

        current_time = datetime.now()
        for file_info in onedrive_files:
            file_last_modified = datetime.strptime(file_info['lastModifiedDateTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
            delta = current_time - file_last_modified

            if delta.days > MAX_BACKUP_AGE:
                try:
                    delete_file_from_onedrive(file_id=file_info['id'], access_token=access_token)
                    print(f"OneDrive backup removed successfully: {file_info['id']}")
                except Exception as e:
                    error_message = f"Error removing old OneDrive backup '{file_info['id']}': {e}"
                    print(error_message)
    except Exception as e:
        error_message = f"Error removing old OneDrive backups: {e}"
        print(error_message)
        logging.error(error_message)

def get_files_in_onedrive(folder_id, access_token):
    try:
        headers = {
            'Authorization': 'Bearer ' + access_token['access_token']
        }

        response = requests.get(
            f"{GRAPH_API_ENDPOINT}/me/drive/items/{folder_id}/children",
            headers=headers
        )

        files = response.json().get('value', [])
        return files
    except Exception as e:
        error_message = f"Error getting files from OneDrive: {e}"
        print(error_message)
        return []

def delete_file_from_onedrive(file_id, access_token):
    try:
        headers = {
            'Authorization': 'Bearer ' + access_token['access_token']
        }

        response = requests.delete(
            f"{GRAPH_API_ENDPOINT}/me/drive/items/{file_id}",
            headers=headers
        )

        print(response.status_code)
        print(response.text)
    except Exception as e:
        error_message = f"Error deleting file from OneDrive: {e}"
        print(error_message)

def main():
    try:
        backup_file_path = create_backup()

        if backup_file_path:
            zip_file_path = compress_backup(backup_file_path)
            remove_old_backups_os()
            save_files_ondrive(zip_file_path)
            remove_old_backups_onedrive()
    except Exception as e:
        error_message = f"Unexpected error: {e}"
        print(error_message)
        logging.error(error_message)

if __name__ == "__main__":
    main()
