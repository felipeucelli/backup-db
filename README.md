# backup-bd
A simple python script to distribute copies of a file on a windows local network.

## Description
The script was built to run inside a linux machine with the aim of distributing a copy of a file to Windows machines on the local network.

## Quickstart
This guide covers faster script usage.

### Installation
backup-bd requires an installation of Python3 or greater. And run on a linux machine with 'cifs-utils' packages installed

Installing packages with apt

```bash
$ sudo apt install cifs-utils
```

### Windows configuration
* Turn on network discovery and turn off secure sharing
* Share the folder with everyone the folder you want to save the file and give everyone read and write permission
* OBS: It is recommended to create a 'Backup' folder inside the shared folder

### Configuring the script
It is necessary to configure the script before starting to use it.

Change IP, PATHS and HOURS as per your need

```python
_address = [
    # Devices IP               # Path to mount on linux system
    ('//192.168.0.114/share_folder', '/opt/mount_folder1/'),
    ('//192.168.0.115/share_folder', '/opt/mount_folder2/')
]

_db = '/FULL/PATH/DATABASE'  # Only one file is allowed for backup

_time = ['09:00:00', '19:00:00']  # Examples of hours
```

