from copy import Copy


class FromSsh(Copy):
    def __init__(self):
        Copy.__init__(self)

    def copy_command(self):
        return ["rsync"
                , self.ssh.get_option()
                , "-avR"
                , "{}:{}".format(self.ssh.get_server(), self.source)
                , self.rsyncconf
                , "{}/{}".format(self.target, self.filename)
                , "--link-dest"
                , self.link]
