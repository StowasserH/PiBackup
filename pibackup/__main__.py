#!/usr/bin/env python

import logging
from config import ConfigParserWithComments
from sysctl import SysCtl
from pibackup import PiBackup
import imp
import os
import sys


def main():
    # args = sys.argv[1:]
    # print('count of args :: {}'.format(len(args)))
    # for arg in args:
    #    print('passed argument :: {}'.format(arg))
    # load the config
    config = ConfigParserWithComments()
    config.set_plugin_folder("./plugins")
    config_filename = "../config.ini"
    if os.path.isfile(config_filename):
        os.remove(config_filename)

    config.get_config(config_filename)
    logging.basicConfig(level=logging.DEBUG, format=config.get('logging', 'format', 1))
    if config.conf_created:
        logging.debug("No configfile ({}) create new one".format(config.config_filename))

    # plausibility checks
    frequency_items = config.items("rotation")
    config.used_plugins = {}
    for key, rotation in frequency_items:
        if key.strip()[0] == ";":
            continue
        occurrence, frequency, method, plugin = rotation.split(";")
        if frequency not in config.fequencies:
            raise Exception("Frequency '{}' of rotation section is not allowed".format(frequency))
        if occurrence not in config.occurrence:
            raise Exception("Occurrence '{}' of rotation section is not allowed".format(occurrence))
        if method not in config.methods:
            raise Exception("Method '{}' of rotation section is not allowed".format(method))
        config.used_plugins[plugin] = 1
    # load used plugins
    for plugin_class in config.used_plugins.keys():
        if plugin_class != "folder":
            imp.load_module(plugin_class, *config.plugins[plugin_class])

    # config.add_comment('systemd', 'PiBackup can stop daemons!')
    # config.set('systemd', 'stop services', 'True')
    # config.add_comment('systemd', 'This daemons! should not be stoped')
    # config.set('systemd', 'whitelist', '--all-databases')
    sysctl = SysCtl()
    if config.get('systemd', 'stopdaemons').lower() == "true":
        sysctl.stop_daemons()
    try:
        bkup = PiBackup(config)
        bkup.do_backup()
    except:
        #logging.error("Unexpected error: {}".format(sys.exc_info()))
        logging.exception("Unexpected error")
    finally:
        sysctl.start_daemons()


# print "done."

if __name__ == '__main__':
    main()

# !/bin/bash

# Setting up directories
# SUBDIR=raspberrypi_backups
# DIR=/hdd/$SUBDIR

# echo "Starting RaspberryPI backup process!"

# First check if pv package is installed, if not, install it first
# PACKAGESTATUS=`dpkg -s pv | grep Status`;

# if [[ $PACKAGESTATUS == S* ]]
# then
# echo "Package 'pv' is installed."
# else
# echo "Package 'pv' is NOT installed."
# echo "Installing package 'pv'. Please wait..."
# apt-get -y install pv
# fi

# Check if backup directory exists
# if [ ! -d "$DIR" ];
# then
# echo "Backup directory $DIR doesn't exist, creating it now!"
# mkdir $DIR
# fi

# Create a filename with datestamp for our current backup (without .img suffix)
# OFILE="$DIR/backup_$(date +%Y%m%d_%H%M%S)"

# Create final filename, with suffix
# OFILEFINAL=$OFILE.img

# First sync disks
# sync; sync

# Shut down some services before starting backup process
# echo "Stopping some services before backup."
# service apache2 stop
# service mysql stop
# service cron stop

# Begin the backup process, should take about 1 hour from 8Gb SD card to HDD
# echo "Backing up SD card to USB HDD."
# echo "This will take some time depending on your SD card size and read performance. Please wait..."
# SDSIZE=`blockdev --getsize64 /dev/mmcblk0`;
# pv -tpreb /dev/mmcblk0 -s $SDSIZE | dd of=$OFILE bs=1M conv=sync,noerror iflag=fullblock

# Wait for DD to finish and catch result
# RESULT=$?

# Start services again that where shutdown before backup process
# echo "Start the stopped services again."
# service apache2 start
# service mysql start
# service cron start

# If command has completed successfully, delete previous backups and exit
# if [ $RESULT = 0 ];
# then
# echo "Successful backup, previous backup files will be deleted."
# rm -f $DIR/backup_*.tar.gz
# mv $OFILE $OFILEFINAL
# echo "Backup is being tarred. Please wait..."
# tar zcf $OFILEFINAL.tar.gz $OFILEFINAL
# rm -rf $OFILEFINAL
# echo "RaspberryPI backup process completed! FILE: $OFILEFINAL.tar.gz"
# exit 0
# Else remove attempted backup file
# else
# echo "Backup failed! Previous backup files untouched."
# echo "Please check there is sufficient space on the HDD."
# rm -f $OFILE
# echo "RaspberryPI backup process failed!"
# exit 1
# fi
