

class mysql:

    def __init__(self, mysql_dump_options, database):
        self.mysql_dump_options = mysql_dump_options
        self.database = database

    def get_stream(self):
        return ["mysqldump", self.mysql_dump_options, self.database, "|", "gzip", "-3", "-c"]
