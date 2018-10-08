import os

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

class Settings:
    __defaultSectionName = "Settings"
    __path = None

    def __init__(self, path):        
        self.__path = path

        if not os.path.exists(path):
            self.__createDefaultConfigFile(path)

    def getSetting(self, setting):
        config = self.__getConfig()
        return config.get(self.__defaultSectionName, setting)

    def setSetting(self, setting, value):
        config = self.__getConfig()
        config.set(self.__defaultSectionName, setting, value)

        with open(self.__path, "w") as configFile:
            config.write(configFile)

    def __getConfig(self):
        config = configparser.ConfigParser()
        config.read(self.__path)
        return config

    def __createDefaultConfigFile(self, path):
        config = configparser.ConfigParser()
        config.add_section(self.__defaultSectionName)

        with open(path, "w") as configFile:
            config.write(configFile)



