# -*- coding: utf-8 -*-

from ssh import Ssh
from rsync import Rsync
from tossh import ToSsh
from fromssh import FromSsh
import logging
import subprocess
import datetime


class PiBackup:
    """ Writes Backups to a specific folder.

    Needs a configuration Object.
    Needs a logging Object. """

    def __init__(self, config):
        self.config = config;
        self.mountpoint = self.config.get('folders', 'check_mountpoint')
        self.ssh = Ssh.fromconfig(self.config.items("ssh"))
        self.last = "last"
        self.target = self.config.get('folders', 'target')
        self.rsyncconf = self.config.get('rsync', 'conf')
        self.link = "{target}/{last}".format(target=self.target, last=self.last)

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
            occurrence, frequency, method, plugin = rotation.split(";")
            self.process_backup(key, occurrence, frequency, method, plugin)

    @staticmethod
    def build_filename(key, frequency):
        now = datetime.datetime.now()
        if frequency < 1 or frequency > 4: frequency = 1
        formats = {1: "%Y%m%d", 2: "%w", 3: "%d", 4: "m%d"}
        return now.strftime(formats[frequency]) + "_" + key

    def build_copy(self, fname, folder,key):
        if self.ssh.mode != 0:
            copy = Rsync()
        elif self.ssh.mode != 1:
            copy = ToSsh()
        elif self.ssh.mode != 2:
            copy = FromSsh()
        #copy.set_logger(logging)
        copy.set_filename(fname)
        copy.set_ssh(self.ssh)
        copy.set_source(folder)
        copy.set_target(self.target)
        copy.set_link("{}/{}".format(self.link, key))
        copy.set_rsyncconf(self.rsyncconf)
        return copy

    def process_backup(self, key, occurrence, frequency, method,plugin):
        # quick = all;weekly;rsync
        # full = once;weekly;sd
        frequency = self.config.fequencies[frequency]
        method = self.config.methods[method] #methods = {"rsync": 1, "sd": 2, }
        fname = self.build_filename(key, frequency)
        logging.info('  processing ' + fname)
        copy = None
        if method==1:
            #copy files via rsync
            for folder in self.config.get('folders', 'sources').split(";"):
                copy = self.build_copy(fname, folder,key)
                copy.do_copy()
            # just use the last copy-instance to create the link
            copy.create_link()
        elif method==2:
            #copy the whole sd via dd
            raise Exception("NotImplementedException")
