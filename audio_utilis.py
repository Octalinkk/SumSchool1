import wave as wave
import pygame
import librosa
import numpy as numpy
from pygame import mixer as mixer

def playAudio(filePath: str) -> None :
    pygame.mixer.init(frequency=44100)      #44.1kHz frequence du wav il me semble
    pygame.mixer.music.load(filePath)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

def readFile(filePath: str) -> wave.Wave_read :
    w: wave.Wave_read = wave.open(filePath, 'rb')  #rb veux dire read binary comme ça tu oublieras pas demain IDIOT!
    return w

def loadAudio(wavFile: str) -> tuple[numpy.ndarray, int]:
    waveForm, sampleRate = librosa.load(wavFile)
    print("Number of samples : ", waveForm.shape)#print de debug a delete après
    print("Duration : ", librosa.get_duration(y=waveForm, sr=sampleRate))#print de debug a delete après
    return waveForm, sampleRate