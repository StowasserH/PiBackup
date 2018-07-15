import subprocess
import logging

class Copy():
    def __init__(self, source="", target="", filename="", link="",ssh=None,rsyncconf=""):
        self.source = source
        self.target = target
        self.filename = filename
        self.link = link
        self.ssh = ssh
        self.rsyncconf = rsyncconf
        #self.logging = logger

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
        return ["mkdir","-p",self.target]

    def do_copy(self):
        command=self.create_target_dir()
        logging.debug("  create dir command:{}".format(" ".join(command)))
        output = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]
        logging.debug("  output:{}".format(output))

        command=self.copy_command()
        logging.debug("  copy command:{}".format(" ".join(command)))
        output = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]
        logging.debug("  output:{}".format(output))


    def create_link(self):
        raise Exception("NotImplementedException")

    def create_link_command(self):
        return ["ln", "-nsf", "{}/{}".format(self.target, self.filename), self.link]

    def create_link(self):
        # echo "ln -nsf $TARGET$TODAY $TARGET$LAST" >> $LOG
        # ln -nsf "$TARGET"$TODAY "$TARGET"last  >> $LOG 2>&1
        command = self.create_link_command()
        logging.debug("  link command:{}".format(" ".join(command)))
        output = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]
        logging.debug("  output:{}".format(output))
