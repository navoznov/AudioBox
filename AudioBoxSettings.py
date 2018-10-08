import os

from Settings import Settings

class AudioBoxSettings:
    """Настройки приложения AudoiBox"""
    __settings = None
    def __init__(self, path):
        path = path if path != None else self.__getDefaultSettingsFilePath()
        self.__settings = Settings(path)

    def setPlayPauseCardId(self, cardId):  
        """Сохраняет идентификатор карты Play/Pause в настройки"""      
        self.__settings.setSetting("PlayPauseCardId", str(cardId))
        
    def getPlayPauseCardId(self):
        """Тянет из настроек идентификатор карты Play/Pause"""
        cardId = self.__settings.getSetting("PlayPauseCardId")
        return int(cardId) if cardId != None else -1

    def setAudioLibraryPath(self, path):
        """Сохраняет в настройки полный путь к библиотеке аудиозаписей"""
        return self.__settings.setSetting("AudioLibraryPath", path)

    def getAudioLibraryPath(self):
        """Тянет из настроек полный путь к библиотеке аудиозаписей"""       
        return self.__settings.getSetting("AudioLibraryPath")

    def __getDefaultSettingsFilePath(self):
        return os.path.join(os.getcwd(), "settings.ini")
