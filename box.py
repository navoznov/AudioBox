import RPi.GPIO as GPIO
import MFRC522
import SimpleMFRC522

import sys
import vlc
from pygame import mixer

import os
from os.path import isfile, join
from time import sleep
import random

# идентификатор карты для проигрывания/паузы
PlayPauseCardId = 123123

# Возвращает полный путь к папке с музыкальной библиотекой
def getAudioLibraryPath():
    currentFolder = os.getcwd()
    audioLibrarySubfolderName = "Music"
    return join(currentFolder, audioLibrarySubfolderName)

# Проигрывает папку
def playFolder(mixer, folderToPlay, useRandom):
    for root, dirs, files in os.walk(folderToPlay):
        playlist = files

    if len(playlist) == 0:
        print("The folder has no files")
        return

    if useRandom:
        random.shuffle(playlist)

    # если проигрыватель занят, то стопаем его. 
    if mixer.music.get_busy():
        print("Stop")
        mixer.music.stop()

    # запускаем проигрывание первого файла из списка
    fileToPlay = playlist[0]       
    mixer.music.load(fileToPlay)
    print("Play {}".format(fileToPlay))
    mixer.music.play()

    # ставим в очередь остальные файлы в списке
    for q in playlist[1:]:
        mixer.music.queue(q)

# выводит информацию о библиотеке аудиозаписей
def printAudioLibraryInfo(audioLibraryPath):
    print('Audio library path: {}'.format(audioLibraryPath))
    print('\n')
    print('Folders in the audio library:')
    for dirpath, dirnames, fileNames in os.walk(audioLibraryPath):
        print(dirpath)
                    
# Для каждой папки в библиотеке с аудиозаписями назначает карту.
# Возвращает словарь: ключ - id карты, значение - путь к папке.
def assignCardsToFolders(audioLibraryPath):
    dirs = []
    cards = dict()

    for root, dirs, files in os.walk(audioLibraryPath):
        try:
            for dir in dirs:
                # todo: добавить проверку, что карта еще не используется.
                
                # читаем карту (идентификатор и текст, который не используем)
                id, text = cardReader.read()
                # склеиваем путь к папке из пути к библиотеке и названия папки
                cards[id] = join(audioLibraryPath, dir)
                print("{0} => {1}".format(dir, id))
                # ставим задержку 1 секуду, чтобы одна и та же карта не 
                sleep(1)        
        except:
            print("error")
        finally:
            print("cleanup")
            GPIO.cleanup()
    return cards

# создаем инстанс кардридера            
cardReader = SimpleMFRC522.SimpleMFRC522()
 
# получаем путь к папке с аудиозаписями    
audioLibraryPath = getAudioLibraryPath()

printAudioLibraryInfo(audioLibraryPath)

# назначаем карты на папки с аудиозаписями
assignedCards = assignCardsToFolders(audioLibraryPath)
    
print("start")   

mixer.init()
isPaused = False
useRandom = True
while True:
    id, text = cardReader.read()
    if id == PlayPauseCardId:
        if mixer.get_busy(): 
            if isPaused:
                mixer.pause()
                print("Pause")
            else:
                mixer.unpause()
                print("Unpause")

        else:
            print("Choose and use one of the assigned cards")
    else:
        folder = assignedCards.get(id)
        if folder == None:        
            print("Unknown card")
        else: 
            playFolder(mixer, folder, useRandom)      
     
    sleep(1)
    
mixer.quit()

