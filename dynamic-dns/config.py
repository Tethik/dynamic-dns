from configparser import ConfigParser

class Config(object):
    def __init__(self, file):
        self.config = ConfigParser()
        self.file = file
        self.config.read(file)
        self.section = "Settings"
        if not self.section in self.config.sections():
            self.config.add_section(self.section)

    def get(self, key):
        return self.config.get(self.section, key)

    def set(self, key, value):
        self.config.set(self.section, key, value)

    def save(self):
        self.config.write(self.file)
