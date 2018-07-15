from copy import Copy


class FromSsh(Copy):
    def __init__(self):
        Copy.__init__(self)

    def create_target_dir(self):
        return "{sshcommand} mkdir -p {target}".format(sshcommand=self.ssh.get_command(), target=self.target)

    def copy_command(self):
        return 'rsync {ssh} -avR "{sshserver}:{source}" {rsyncconf} "{target}/{fname}" {inc}'.format(
            source=self.source
            , ssh=self.ssh.get_option()
            , sshserver=self.ssh.get_server()
            , rsyncconf=self.rsyncconf
            , target=self.target
            , fname=self.filename
            , inc=self.link
        )
