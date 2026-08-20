import wave as wave
import os 
import librosa
import pygame
import numpy as numpy
import matplotlib.pyplot as plt

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

def mp3ToMidi(fileName: str) -> None :
    midFile: None = wavToMidi(fileName)
    return midFile

def wavToMidi(wavFile: str) -> None:
    hopLength: int = 512
    waveForm, sampleRate = librosa.load(wavFile, sr=None)
    print(sampleRate)
    onset_env, onset_peaks, onset_detect = detectOnSets(waveForm, sampleRate, hopLength)
    f0, pitchTimes = detectPitchesCqt(waveForm, sampleRate, hopLength)
    plotOnsetAnalysis(waveForm, sampleRate, onset_env, onset_peaks, onset_detect, hopLength, r"/home/adrien/Documents/SumSchool1/Image/test.png") #a remplacer par le chjemin de fichier qu il faut pas garder le meme sinon tout casser si on veux sauvegarder l'image


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

def detectPitchesCqt(waveForm: numpy.ndarray, sampleRate: int, hopLength: int) -> tuple[numpy.ndarray, numpy.ndarray]:
    binsPerOctave: int = 36
    numHarmonics: int = 5
    numOctaves: int = 7
    fmin: float = librosa.note_to_hz('C2')

    cqtMatrix: numpy.ndarray = librosa.cqt(waveForm, sr=sampleRate, hop_length=hopLength, fmin=fmin, bins_per_octave=binsPerOctave, n_bins=binsPerOctave * numOctaves)
    cqtMagnitue: numpy.ndarray = numpy.abs(cqtMatrix)
    nBins, nFrames = cqtMagnitue.shape

    offsets: numpy.ndarray = binsPerOctave * numpy.log2(numpy.arange(1, numHarmonics + 1))
    weights: numpy.ndarray = 1.0 / numpy.arange(1, numHarmonics + 1)

    cands: numpy.ndarray = numpy.arange(0, nBins - int(numpy.ceil(offsets[-1])), 3)

    def salience(C: numpy.ndarray) -> numpy.ndarray:
        scores: list = []
        for b in cands:
            total: float = 0
            for k in range(1, numHarmonics + 1):
                p = b + binsPerOctave * numpy.log2(k)
                total += (1 / k) * C[int(round(p))]
            scores.append(total / weights.sum())
        return numpy.array(scores)

    maxBinIndices: numpy.ndarray = numpy.array([
        cands[numpy.argmax(salience(cqtMagnitue[:, t]))] for t in range(nFrames)
    ])

    binFreq: numpy.ndarray = librosa.cqt_frequencies(n_bins=nBins, fmin=fmin, bins_per_octave=binsPerOctave)
    f0: numpy.ndarray = binFreq[maxBinIndices]
    pitchTimes: numpy.ndarray = librosa.times_like(f0, sr=sampleRate, hop_length=hopLength)

    print(f"f0 : {f0}")
    print('\n')
    print(f"pitch time : {pitchTimes}")
    print(f"f0 size : {f0.size}")
    print(f"pitch size : {pitchTimes.size}") #si meme taille victoire hihih  yipeeeee
    return f0, pitchTimes

mp3ToMidi(r"/home/adrien/Documents/SumSchool1/Song/PinkPanther_Piano_Only.mp3") #a changer le chemin d'acces pour le prochain utilisatuer