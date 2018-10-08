import os

from Settings import Settings

class AudioBoxSettings:
    __settings = None
    def __init__(self, path):
        path = path if path != None else self.__getDefaultSettingsFilePath()
        self.__settings = Settings(path)

    def setPlayPauseCardId(self, cardId):        
        self.__settings.setSetting("PlayPauseCardId", str(cardId))
        
    def getPlayPauseCardId(self):
        return self.__settings.getSetting("PlayPauseCardId")

    def setAudioLibraryPath(self, path):
        return self.__settings.setSetting("AudioLibraryPath", path)

    def getAudioLibraryPath(self):
        return self.__settings.getSetting("AudioLibraryPath")

    def __getDefaultSettingsFilePath(self):
        return os.path.join(os.getcwd(), "settings.ini")
