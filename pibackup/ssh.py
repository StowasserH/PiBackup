class Ssh:
    def __init__(self,user,server,port,mode):
        self.user=user
        self.server=server
        self.port=port
        self.mode=mode

    @classmethod
    def fromconfig(cls, config):
        propbag={}
        for key, item in config:
            if key.strip()[0] == ";":
                continue
            propbag[key]=item
        return cls(propbag['user'],propbag['server'],propbag['port'],propbag['mode'])

    def get_command(self):
        if self.mode==0:
            return ""
        return "ssh {}@{}".format(self.user,self.server)

    def get_option(self):
        if self.mode==0:
            return []
        return ["ssh","-p",""+self.port,"-l",self.user]

    def get_server(self):
        return self.server