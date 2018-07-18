import subprocess

class SysCtl:
    def __init__(self):
        self.daemons=[]
    def create_daemon_list(self):
        output = subprocess.Popen(["service","--status-all"], stdout=subprocess.PIPE).communicate()[0]
        self.daemons={}
        for line in output.split("\n"):
            tuff=line.strip().split(" ")
            name=tuff[-1]
            if len(name)>2:
                if tuff[1]=='+':
                    self.daemons[name]=True
                elif tuff[1]=='-':
                    pass
                    #self.daemons[name]=False
                else:
                    raise Exception("service --status-all has no daemons")

    def stop_daemons(self):
        self.create_daemon_list()
        for daemon in self.daemons.keys():
            if self.daemons[daemon]==True:
                print daemon

    def start_daemons(self):
        pass
