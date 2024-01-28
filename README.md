# MySql Backup with Python 🐍
The Python Database Backup Script is a versatile and robust tool designed to simplify and automate the backup process for MySQL databases.

## Features 🚀
#### Database Backup Automation
- The script automates the backup process, reducing the manual effort required for routine database backups.

  1. __Backup Compression:__ Backups are compressed into a .zip file, optimizing storage space and facilitating efficient data transfer.
  
  2. __Customizable Configuration:__ Easily configure your database connection details such as host, user, password, and database name to suit your specific requirements.
  
  3. __Logging Functionality:__ Comprehensive logging captures exceptions and errors, providing a detailed record of the backup process.
  
  4. __Backup Retention Policy:__ The script includes a default backup retention policy, removing older backups after a specified number of days. Customize the retention period as needed.

## Configuration ⚙️
1. Configure your database connection details:
  ```python
  DB_HOST = 'localhost'
  DB_USER = 'your_username'
  DB_PASSWORD = 'your_password'
  DB_NAME = 'your_database_name'
  ```

2. Set the path for storing backups:
  ```python
  BACKUP_DIR = ''
  ```
   
3. Configure the path for logs:
  ```python
  log_file_path = ''
  ```

4. Backups are automatically removed after 7 days by default. You can adjust this duration by modifying the MAX_BACKUP_AGE variable.
  ```python
  MAX_BACKUP_AGE = 7
  ```

## Instructions 📝
1. Adjust the configuration variables in the script to match your database and desired backup paths.

2. Run the script:
  ```console
  python backup.py
  ```

Optionally, set up Windows Task Scheduler for automated and scheduled backups following the tips below.

Feel free to customize the script to suit your specific needs. If you encounter any issues, refer to the logs for detailed error messages.

## Tips 💡
You can use [Windows Task Scheduler](https://www.jcchouinard.com/python-automation-using-task-scheduler/) to determine how often the script runs.

## Next Features 🛠️
- __Cloud Backup__

  After completing the backup compression in .zip format, the script will be enhanced to allow automatic upload of the backup to a cloud platform such as OneDrive or a similar service. This will provide a comprehensive and secure solution for remote backup storage. Stay tuned for future updates and enjoy these additional features to enhance the efficiency and security of your backup process!

## Common Errors 🚨
- Issue with mysqldump Command 'mysqldump' is not recognized as an internal or external command, operable program or batch file":

  If you encounter the error 'mysqldump' is not recognized as an internal or external command, operable program or batch file, it means that the system cannot find the mysqldump executable.
  
  ### Solutions 💡
  Add the path to the mysqldump executable to your system's PATH environment variable. For XAMPP users, add C:\xampp\mysql\bin to both user variables and system variables. For WAMP server users, add C:\wamp64\bin\mysql\mysql8.0.27\bin to both user and system variables. Note: The MySQL version path may vary based on your installation.
  
  Alternate Solution:
  
  If the above step don't resolve the issue, you can modify the script to directly reference the mysqldump executable's full path.
  ```python
  mysqldump_cmd = f'C:\\xampp\\mysql\\bin\\mysqldump.exe -h {DB_HOST} -u {DB_USER} -p{DB_PASSWORD} {DB_NAME} > {BACKUP_FILE_PATH}'
  ```
  Adjust the path accordingly based on the installation directory of your mysqldump executable.
