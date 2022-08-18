# In the name of God
# Omid

import datetime
from configparser import ConfigParser


class VariableLogger:

    def __init__(self):
        self.prompt = ""
        config_file = 'adjust.conf'
        config = ConfigParser()
        config.read(config_file)
        self.var_log_file = config['Logging']['var_log_file']
        with open(self.var_log_file, 'w') as f:
            f.write('')

    def update_prompt(self, p):
        self.prompt = p

    def varlogwr(self):
        with open(self.var_log_file, 'a') as f:
            now = str(datetime.datetime.now())
            s = "\n" + now + "\n" + self.prompt + "\n----------------------------------"
            f.writelines(s)
