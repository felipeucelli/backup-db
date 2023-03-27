# backup-db
A simple python script to distribute copies of a file on a windows local network.

## Description
The script was built to run inside a linux machine with the aim of distributing a copy of a file to Windows machines on the local network.

## Installation
backup-db requires an installation of Python3 or greater. And run on a linux machine with 'cifs-utils' packages installed

Installing packages with apt

```bash
$ sudo apt install cifs-utils
```

## Windows configuration
* Turn on network discovery
* Share the folder with everyone the folder you want to save the file and give everyone read and write permission.

## Configuring the script
It is necessary to configure the **backup-db.conf** file before starting to use it.

* Change the parameters as needed.
* You can create more than one machines session.

```text
[LOG]
path=/var/log/backup-db.log

[DATABASE]
path=/FULL/PATH

[PC1]
ip=192.168.0.2
username=user
password=pass
time=12:00:00, 19:00:00
days=0,1,2,3,4,5,6
backup_folder=backup/folder
mount_point=/mount/point/
```

