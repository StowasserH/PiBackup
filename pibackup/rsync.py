from copy import Copy


class Rsync(Copy):
    def __init__(self):
        Copy.__init__(self)

    def create_target_dir(self):
        return ["mkdir","-p",self.target]

    def copy_command(self):
        return ["rsync","-avR",self.source,self.rsyncconf,"{target}/{fname}".format(target=self.target, fname=self.filename) ,self.link]
