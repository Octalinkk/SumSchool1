import wave as wave
import pydub as pydub
import os 
import librosa
import pygame
import numpy as numpy
import matplotlib.pyplot as plt

from pydub import AudioSegment
from pydub import playback as playback
from pygame import mixer as mixer
from librosa import display

def playAudio(filePath: str) -> None :
    pygame.mixer.init(frequency=44100)      #44.1kHz frequence du wav il me semble
    pygame.mixer.music.load(filePath)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

def readFile(filePath: str) -> wave.Wave_read :
    w: wave.Wave_read = wave.open(filePath, 'rb')  #rb veux dire read binary comme ça tu oublieras pas demain IDIOT!
    return w

def mp3ToWav(mp3File: str) -> str:
    song: AudioSegment = AudioSegment.from_mp3(mp3File)
    wavFile: str = os.path.splitext(mp3File)[0] + ".wav"
    song.export(wavFile, format="wav")
    return wavFile 

def loadAudio(wavFile: str) -> tuple[numpy.ndarray, int]:
    waveForm, sampleRate = librosa.load(wavFile)
    print("Number of samples : ", waveForm.shape)
    print("Duration : ", librosa.get_duration(y=waveForm, sr=sampleRate))
    return waveForm, sampleRate

def detectOnSets(waveForm: numpy.ndarray, sampleRate: int, hopLength: int) -> tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray]:
    stft_complex: numpy.ndarray = librosa.stft(waveForm, hop_length=hopLength)
    logS: numpy.ndarray = librosa.amplitude_to_db(numpy.abs(stft_complex), ref=numpy.max)

    onset_env = librosa.onset.onset_strength(S=logS, sr=sampleRate, hop_length=hopLength)
    onset_peaks = librosa.util.localmax(onset_env)
    onset_detect = librosa.onset.onset_detect(
        onset_envelope=onset_env, sr=sampleRate, hop_length=hopLength
    )
    return onset_env, onset_peaks, onset_detect


def plotOnsetAnalysis(waveForm: numpy.ndarray, sampleRate: int, onset_env: numpy.ndarray, onset_peaks: numpy.ndarray, onset_detect: numpy.ndarray, hopLength: int, outputImagePath: str) -> None:
    times = librosa.times_like(onset_env, sr=sampleRate, hop_length=hopLength)

    fig, ax = plt.subplots(nrows=2, sharex=True, height_ratios=(3, 1))

    librosa.display.waveshow(y=waveForm, sr=sampleRate, ax=ax[1], label="Waveform")
    ax[1].legend()

    ax[0].plot(times, onset_env, label="Onset envelope", color="C1")
    ax[0].scatter(times[onset_peaks], onset_env[onset_peaks], marker="^", color="k", label="Localmax Peaks")
    ax[0].scatter(times[onset_detect], onset_env[onset_detect], marker="o", edgecolor="C2", facecolor="none", label="onset_detect")
    ax[0].legend()
    ax[0].label_outer()

    plt.savefig(outputImagePath)
    plt.close(fig)



def wavToMidi(wavFile: str) -> None:
    hopLength: int = 512

    waveForm, sampleRate = loadAudio(wavFile)
    onset_env, onset_peaks, onset_detect = detectOnSets(waveForm, sampleRate, hopLength)
    plotOnsetAnalysis(waveForm, sampleRate, onset_env, onset_peaks, onset_detect, hopLength, r"/home/adrien/Documents/SumSchool1/Image/test.png")


def mp3ToMidi(fileName: str) -> None :
    wavFile: str = mp3ToWav(fileName)
    midFile: None = wavToMidi(wavFile)
    return midFile

mp3ToMidi(r"/home/adrien/Documents/SumSchool1/Song/TestPiano.mp3")