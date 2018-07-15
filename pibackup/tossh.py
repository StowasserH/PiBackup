from copy import Copy


class ToSsh(Copy):
    def __init__(self):
        Copy.__init__(self)

    def create_target_dir(self):
        return "{sshcommand} mkdir -p {target}".format(sshcommand=self.ssh.get_command(), target=self.target)

    def copy_command(self):
        return ["rsync"
                , self.ssh.get_option()
                , "-avR"
                , self.source
                , self.rsyncconf
                , "{}:{}/{}".format(self.ssh.get_server(), self.target, self.filename)
                , "--link-dest"
                , self.link]

    def create_link_command(self):
        return [self.ssh.get_option, self.ssh.get_server(), "ln", "-nsf", "{}/{}".format(self.target, self.filename),
                self.link]
