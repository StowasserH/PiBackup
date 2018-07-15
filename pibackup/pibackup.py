from config import ConfigParserWithComments
from ssh import Ssh
from rsync import Rsync
from tossh import ToSsh
from fromssh import FromSsh
import logging
import subprocess
import os
import datetime


class PiBackup:
    def __init_enums(self):
        self.fequencies = {"none": 1, "weekly": 2, "monthly": 3, "yearly": 4}
        self.occurrence = {"once": 1, "all": 2, }
        self.methods = {"rsync": 1, "sd": 2, }
        self.sshmodes = {"none": 0, "push": 1, "pull": 2}

    def __init__(self):
        self.config_filename = "../config.ini"
        # remove ths!
        #if os.path.isfile(self.config_filename):
        #    os.remove(self.config_filename)
        self.__init_enums()
        self.conf_created = False
        self.config = self.get_config()
        logging.basicConfig(level=logging.DEBUG, format=self.config.get('logging', 'format', 1))
        if self.conf_created:
            logging.debug("No configfile ({}) create new one".format(self.config_filename))
        self.mountpoint = self.config.get('folders', 'check_mountpoint')
        self.ssh = Ssh.fromconfig(self.config.items("ssh"))
        self.last = "last"
        self.target = self.config.get('folders', 'target')
        self.rsyncconf = self.config.get('rsync', 'conf')
        self.inc = "--link-dest={target}/{last}".format(target=self.target, last=self.last)
        # self.ssh=self.sshmodes[self.config.get('ssh', 'mode')]

    def check_mountpoint(self):
        output = subprocess.Popen(["mount"], stdout=subprocess.PIPE).communicate()[0]
        if output.__contains__(self.mountpoint):
            logging.debug("gefunden")
        else:
            logging.debug("Mountpoint")
            # raise Exception('Mountpoint {} is not mounted!'.format(self.mountpoint))

    def do_backup(self):
        logging.info('Starting Backup')
        if len(self.mountpoint) > 3:
            self.check_mountpoint()
        frequency_items = self.config.items("rotation")
        for key, rotation in frequency_items:
            if key.strip()[0] == ";":
                continue
            occurrence, frequency, method = rotation.split(";")
            self.process_backup(key, occurrence, frequency, method)

    @staticmethod
    def build_filename(key, frequency):
        now = datetime.datetime.now()
        if frequency < 1 or frequency > 4: frequency = 1
        formats = {1: "%Y%m%d", 2: "%w", 3: "%d", 4: "m%d"}
        return now.strftime(formats[frequency]) + "_" + key

    def build_copy(self,fname,folder):
        if self.ssh.mode != 0:
            copy = Rsync()
        elif self.ssh.mode != 1:
            copy = ToSsh()
        elif self.ssh.mode != 2:
            copy = FromSsh()
        copy.set_logger(logging)
        copy.set_filename(fname)
        copy.set_ssh(self.ssh)
        copy.set_source(folder)
        copy.set_target(self.target)
        copy.set_link(self.inc)
        copy.set_rsyncconf(self.rsyncconf)

    def process_backup(self, key, occurrence, frequency, method):
        frequency = self.fequencies[frequency]
        fname = self.build_filename(key, frequency)
        logging.info('  processing ' + fname)
        ssh_option = self.ssh.get_option()
        for folder in self.config.get('folders', 'sources').split(";"):
            copy = self.build_copy(fname,folder)
            copy.do_copy()

    def get_config(self):
        config = ConfigParserWithComments()
        if not os.path.isfile(self.config_filename):
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
                               'frequency={' + '|'.join(self.occurrence.keys()) + '};{' + '|'.join(self.fequencies.keys()) + '};{' + '|'.join(self.methods.keys()) + '}')
            config.set('rotation', 'quick', 'all;weekly;rsync')
            config.set('rotation', 'full', 'once;weekly;sd')

            # level = logging.INFO
            with open(self.config_filename, 'wb') as configfile:
                config.write(configfile)
                self.conf_created = True
            configfile.close()
        config.read(self.config_filename)
        return config
