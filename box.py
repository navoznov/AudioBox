import RPi.GPIO as GPIO
import MFRC522
import SimpleMFRC522

import sys
import vlc
from  pygame import mixer

import os
from os.path import isfile, join
from time import sleep
import random

def playFolder(toPlay, use_random):
    
    for root, dirs, files in os.walk(toPlay):
        play_list = files

    if use_random:
        random.shuffle(play_list)
    f = play_list[0]
    
    if mixer.music.get_busy():
        print("stop")
        mixer.music.stop()
        
    mixer.music.load(f)
    print("play {}".format(f))
    mixer.music.play()

    for q in play_list[1:]:
        mixer.music.queue(q)
            

cardReader = SimpleMFRC522.SimpleMFRC522()
 
currentFolder = os.getcwd()
audioPath = join(currentFolder, "Music")
print(audioPath)

for a in os.walk(audioPath):
    print(a)
    
print("start")   

dirs = []
cards = dict()

for root, dirs, files in os.walk(audioPath):
    n = len(dirs)
    print(n)
    try:
        for dir in dirs:
            id, text = cardReader.read()
            print("{0} => {1}".format(dir, id))
            cards[id] = dir
            sleep(1)        
    except:
        print("error")
    finallyllall python
    :
        print("cleanup")
        GPIO.cleanup()
        
GPIO.cleanup()


mixer.init()

while True:
    id, text = cardReader.read()
    folder = cards.get(id)
    if folder == None:
        print("Unknown card")
    else: 
        toPlay = join(audioPath, folder)
        
        playFolder(toPlay, True)      
     
    sleep(1)
    
mixer.quit()

