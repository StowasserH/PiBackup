from copy import Copy


class ToSsh(Copy):
    def __init__(self):
        Copy.__init__(self)

    def create_target_dir(self):
        return "{sshcommand} mkdir -p {target}".format(sshcommand=self.ssh.get_command(), target=self.target)

    def copy_command(self):
        return ["rsync"
                , "-e"
                , self.ssh.get_option()
                , "-avR"
                , self.source
                , self.rsyncconf
                , "{}:{}/{}".format(self.ssh.get_server(), self.target, self.filename)
                , "--link-dest"
                , self.link]
        #-e \"$S\" S="ssh -p $SSHPORT -l $SSHUSER";

    def create_link_command(self):
        return [self.ssh.get_option, self.ssh.get_server(), "ln", "-nsf", "{}/{}".format(self.target, self.filename),
                self.link]

    def pipe(self,stream):
        return [self.ssh.get_option, self.ssh.get_server(), stream]
        #"mysqldump -mysqldumpoptions database | gzip -3 -c" > /localpath/localfile.sql.gz
        #this works:
        #mysqldump --compact --disable-keys --dump-date --comments --lock-tables -u root --all-databases | gzip -c | ssh backups@servberry 'cat > ~/zabbix.dump.gz'