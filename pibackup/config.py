import ConfigParser
import imp
import os


class ConfigParserWithComments(ConfigParser.ConfigParser):
    def add_comment(self, section, comment):
        self.set(section, '; %s' % (comment,), None)

    def set_plugin_folder(self, plugin_folder):
        self.plugin_folder = plugin_folder

    def get_plugin_folder(self, folder):
        return self.plugin_folder

    def getPlugins(self):
        plugins = {}
        possibleplugins = os.listdir(self.plugin_folder)
        for name in possibleplugins:
            if name[-3:] == ".py":
                plugin_class = name.replace(".py", "")
                # location = os.path.join(PluginFolder, name)
                info = imp.find_module(plugin_class, [self.plugin_folder])
                plugins[plugin_class] = info
        return plugins

    def write(self, fp):
        """Write an .ini-format representation of the configuration state."""
        if self._defaults:
            fp.write("[%s]\n" % ConfigParser.DEFAULTSECT)
            for (key, value) in self._defaults.items():
                self._write_item(fp, key, value)
            fp.write("\n")
        for section in self._sections:
            fp.write("[%s]\n" % section)
            for (key, value) in self._sections[section].items():
                self._write_item(fp, key, value)
            fp.write("\n")

    def _write_item(self, fp, key, value):
        if key.startswith(';') and value is None:
            fp.write("%s\n" % (key,))
        else:
            fp.write("%s = %s\n" % (key, str(value).replace('\n', '\n\t')))

    def get_config(self, config_filename):
        self.conf_created = False
        self.fequencies = {"none": 1, "weekly": 2, "monthly": 3, "yearly": 4}
        self.occurrence = {"once": 1, "all": 2, }
        self.methods = {"rsync": 1, "ssh": 2, }
        self.sshmodes = {"none": 0, "push": 1, "pull": 2}
        self.bool = {"true": 1, "false": 0}
        self.plugins = self.getPlugins()
        self.config_filename = config_filename
        if not os.path.isfile(config_filename):
            self.add_section('folders')
            self.set('folders', 'sources', '/root;/etc;/home;/boot')
            self.set('folders', 'target', '/media/nas/backup')
            self.add_comment('folders', 'If you mount a storage the script can check if it is realy mounted before running')
            self.set('folders', 'check_mountpoint', '/media/nas')
            self.add_section('ssh')
            self.add_comment('ssh', 'The alternative to mount a storage ist to stream over ssh. Please take care of the users permissions and use a separate user.')
            self.set('ssh', 'user', 'sshuser')
            self.set('ssh', 'server', 'servberry')
            self.set('ssh', 'port', '22')
            self.add_comment('ssh', 'none = you dont use ssh and copy to local/mount')
            self.add_comment('ssh', 'push = move the Files to server via rsync + ssh')
            self.add_comment('ssh', 'pull = move the Files from a host to local via rsync + ssh')
            self.add_comment('ssh', 'mode = {none|push|pull}')
            self.set('ssh', 'mode', 'none')
            self.add_section('rsync')
            self.set('rsync', 'conf', '--delete')
            self.add_section('logging')
            self.set('logging', 'logfile', '/media/nas/log/pibackup.log')
            self.add_comment('logging', 'levels={debug|info|warning|error|critical}')
            self.set('logging', 'level', 'debug')
            self.set('logging', 'format', '%(asctime)s %(levelname)s:%(message)s')
            self.add_section('rotation')
            self.add_comment('rotation', 'frequency={' + '|'.join(self.occurrence.keys()) + '};')
            self.add_comment('rotation', '           ' + '|'.join(self.fequencies.keys()) + '};')
            self.add_comment('rotation', '           ' + '|'.join(self.methods.keys()) + '}')
            # self.add_comment('rotation', '           ' + '|'.join(self.fequencies.keys()) + '};{' + '|'.join(self.methods.keys()) + '}')
            self.set('rotation', 'quick', 'all;weekly;rsync;folder')
            self.set('rotation', ';ssh', 'all;weekly;ssh;folder')
            self.set('rotation', 'mysqldb', 'all;weekly;ssh;mysql')
            self.set('rotation', 'full', 'once;weekly;ssh;sd')
            self.add_section('mysqldb')
            self.add_comment('rotation', 'Example for the configutation of the mysql-plugin')
            # self.set('mysqldb', 'mysql_user', 'zabbix')
            self.set('mysqldb', 'mysql_dump_options', '--compact --disable-keys --dump-date --comments --lock-tables -u root')
            # mysqldump --compact --disable-keys --dump-date --comments --lock-tables -u root --all-databases
            self.set('mysqldb', 'database', '--all-databases')

            self.add_section('systemd')
            self.add_comment('systemd', 'PiBackup can stop daemons!')
            self.add_comment('systemd', 'stop daemons={' + '|'.join(self.bool.keys()) + '}')
            self.set('systemd', 'stopdaemons', 'true')
            self.add_comment('systemd', 'This daemons! should not be stoped')
            self.set('systemd', 'whitelist', '')

            # level = logging.INFO
            with open(config_filename, 'wb') as configfile:
                self.write(configfile)
                self.conf_created = True
            configfile.close()
        self.read(config_filename)
