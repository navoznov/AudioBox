#!/usr/bin/env python3
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522

import sys
import vlc
from pygame import mixer

import os
from time import sleep
import random

from AudioBoxSettings import AudioBoxSettings

# задержка после считывания карты (до следующего считывания карты)
cardReadingDelay = 1
settingsFileName = "settings.ini"

settings = AudioBoxSettings(settingsFileName)

def getAudioLibraryPath():
    """
    Возвращает полный путь к папке с музыкальной библиотекой
    """
    path = settings.getAudioLibraryPath()
    if path == None:
        currentFolder = os.getcwd()
        audioLibrarySubfolderName = "Music"
        path = os.path.join(currentFolder, audioLibrarySubfolderName)
        settings.setAudioLibraryPath(path)
    return path

def playFolder(mixer, folderToPlay, useRandom):
    """
    Воспроизводит аудиозаписи в папке
    """
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

def printAudioLibraryInfo(audioLibraryPath):
    """
    выводит информацию о библиотеке аудиозаписей
    """
    print('Audio library path: {}'.format(audioLibraryPath))
    print('\n')
    print('Folders in the audio library:')
    for dirpath, dirnames, fileNames in os.walk(audioLibraryPath):
        print(dirpath)
                    
def assignCardsToFolders(audioLibraryPath):
    """
    Для каждой папки в библиотеке с аудиозаписями назначает карту.
    Возвращает словарь: ключ - id карты, значение - путь к папке.
    """
    dirs = []
    cards = dict()

    for root, dirs, files in os.walk(audioLibraryPath):
        try:
            for dir in dirs:                
                # todo: если считывается уже использованная карта, то эта карта назначается на текущую папку, а предыдущая папка (которая была до этого назначена) ""освобождается" и добавляется в список папок для назначения

                # читаем карту. если уже используется, то снова читаем.
                while True:
                    # читаем карту (идентификатор и текст, который не используем)
                    id, text = cardReader.read()
                    
                    if id in cards:
                        print("This card is used already. Scan another card.")
                    else:
                        break

                # склеиваем путь к папке из пути к библиотеке и названия папки
                cards[id] = os.path.join(audioLibraryPath, dir)
                print("{0} => {1}".format(dir, id))
                # ставим задержку, чтобы одна и та же карта не считывалась несколько раз подряд
                sleep(cardReadingDelay)        
        except:
            print("error")
        finally:
            print("cleanup")
            GPIO.cleanup()
    return cards

def assignPlayPauseCardIfNeed():
    if PlayPauseCardId > 0:
        return

# создаем инстанс кардридера            
cardReader = SimpleMFRC522.SimpleMFRC522()
 
# получаем путь к папке с аудиозаписями    
audioLibraryPath = getAudioLibraryPath()
# идентификатор карты для проигрывания/паузы
PlayPauseCardId = settings.getPlayPauseCardId()

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
     
# ставим задержку, чтобы одна и та же карта не считывалась несколько раз подряд
sleep(cardReadingDelay)        

mixer.quit()

