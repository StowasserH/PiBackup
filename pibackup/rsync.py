from copy import Copy


class Rsync(Copy):
    def __init__(self):
        Copy.__init__(self)

    def copy_command(self):
        return ["rsync"
                , "-avR"
                , self.source
                , self.rsyncconf
                , "{target}/{fname}".format(target=self.target, fname=self.filename)
                , "--link-dest"
                , self.link]
