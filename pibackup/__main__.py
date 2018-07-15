#!/usr/bin/env python

import sys
import os
import logging
from config import ConfigParserWithComments
from pibackup import PiBackup

def get_config(config_filename):
    config = ConfigParserWithComments()
    config.conf_created = False
    config.fequencies = {"none": 1, "weekly": 2, "monthly": 3, "yearly": 4}
    config.occurrence = {"once": 1, "all": 2, }
    config.methods = {"rsync": 1, "sd": 2, }
    config.sshmodes = {"none": 0, "push": 1, "pull": 2}

    if not os.path.isfile(config_filename):
        config.add_section('folders')
        config.set('folders', 'sources', '/root;/etc;/home;/boot')
        config.set('folders', 'target', '/media/nas/backup')
        config.add_comment('folders', 'If you mount a storage the script can check if it is realy mounted before running')
        config.set('folders', 'check_mountpoint', '/media/nas')
        config.add_section('ssh')
        config.add_comment('ssh', 'The alternative to mount a storage ist to stream over ssh. Please take care of the users permissions and use a separate user.')
        config.set('ssh', 'user', 'sshuser')
        config.set('ssh', 'server', 'servberry')
        config.set('ssh', 'port', '22')
        config.add_comment('ssh', 'none = you dont use ssh and copy to local/mount')
        config.add_comment('ssh', 'push = move the Files to server via rsync + ssh')
        config.add_comment('ssh', 'pull = move the Files from a host to local via rsync + ssh')
        config.add_comment('ssh', 'mode = {none|push|pull}')
        config.set('ssh', 'mode', 'none')
        config.add_section('rsync')
        config.set('rsync', 'conf', '--delete')
        config.add_section('logging')
        config.set('logging', 'logfile', '/media/nas/log/pibackup.log')
        config.add_comment('logging', 'levels={debug|info|warning|error|critical}')
        config.set('logging', 'level', 'debug')
        config.set('logging', 'format', '%(asctime)s %(levelname)s:%(message)s')
        config.add_section('rotation')
        config.add_comment('rotation',
                           'frequency={' + '|'.join(config.occurrence.keys()) + '};{' + '|'.join(config.fequencies.keys()) + '};{' + '|'.join(config.methods.keys()) + '}')
        config.set('rotation', 'quick', 'all;weekly;rsync')
        config.set('rotation', 'full', 'once;weekly;sd')

        # level = logging.INFO
        with open(config_filename, 'wb') as configfile:
            config.write(configfile)
            config.conf_created = True
        configfile.close()
    config.read(config_filename)
    return config

def main():
    args = sys.argv[1:]

#    print('count of args :: {}'.format(len(args)))
#    for arg in args:
#        print('passed argument :: {}'.format(arg))
    config_filename = "../config.ini"
    config=get_config(config_filename)
    logging.basicConfig(level=logging.DEBUG, format=config.get('logging', 'format', 1))
    if config.conf_created:
        logging.debug("No configfile ({}) create new one".format(config.config_filename))

    bkup=PiBackup(config)
    bkup.do_backup()

#    print "done."

if __name__ == '__main__':
    main()


