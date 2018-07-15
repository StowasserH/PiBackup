import subprocess

class Copy():
    def __init__(self, source="", target="", filename="", link="",ssh=None,rsyncconf="",logger=None):
        self.source = source
        self.target = target
        self.filename = filename
        self.link = link
        self.ssh = ssh
        self.rsyncconf = rsyncconf
        self.logging = logger

    def set_ssh(self, ssh):
        self.ssh = ssh

    def set_source(self, source):
        self.source = source

    def set_target(self, target):
        self.target = target

    def set_filename(self, filename):
        self.filename = filename

    def set_link(self, link):
        self.link = link

    def set_rsyncconf(self, rsyncconf):
        self.rsyncconf = rsyncconf

    def create_target_dir(self):
        raise Exception("NotImplementedException")

    def do_copy(self):
        command=self.create_target_dir()
        self.logging.debug("  create dir command:{}".format(" ".join(command)))
        output = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]
        self.logging.debug("  output:{}".format(output))

        command=self.copy_command()
        self.logging.debug("  copy command:{}".format(" ".join(command)))
        output = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]
        self.logging.debug("  output:{}".format(output))

    def set_logger(self,logging):
        self.logging = logging

    def copy_command(self):
        raise Exception("NotImplementedException")
