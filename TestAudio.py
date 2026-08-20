import wave as wave
import os 
import librosa
import pygame
import numpy as numpy
import matplotlib.pyplot as plt
import pretty_midi

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
    
    onset_env, onset_peaks, onset_detect = detectOnSets(waveForm, sampleRate, hopLength)
    f0, pitchTimes = detectPitchesCqt(waveForm, sampleRate, hopLength)

    onset_times = librosa.frames_to_time(onset_detect, sr=sampleRate, hop_length=hopLength)
    notePitches = aggregatePitchesByNote(f0, pitchTimes, onset_detect, sampleRate, hopLength)
    
    total_duration = librosa.get_duration(y=waveForm, sr=sampleRate)
    
    midi_data = midi_builder(onset_times=onset_times, note_pitches=notePitches, total_duration=total_duration)
    midi_writer(midi_data)
    '''print(f"Notes start : {onset_times}") #print de debug a delete après
    print(f"Notes pitches : {notePitches}")#print de debug a delete après
    print(f"Number of notes : {notePitches.size}")#print de debug a delete après'''
    #plotOnsetAnalysis(waveForm, sampleRate, onset_env, onset_peaks, onset_detect, hopLength, r"./Image/test.png") #a remplacer par le chjemin de fichier qu il faut pas garder le meme sinon tout casser si on veux sauvegarder l'image

def midi_builder(onset_times: numpy.ndarray, note_pitches: numpy.ndarray, total_duration: float): 
    midi_data = []
    
    for n in range(len(onset_times)):
        pitch_hz = note_pitches[n]
        if numpy.isnan(pitch_hz) or pitch_hz <= 0:
            continue
            
        midi_pitch = int(round(librosa.hz_to_midi(pitch_hz)))
        midi_pitch = max(0, min(127, midi_pitch))
        
        start_time = onset_times[n]
        end_time = onset_times[n + 1] if n < len(onset_times) - 1 else total_duration

        midi_data.append((midi_pitch, start_time, end_time))
    
    return midi_data

def midi_writer(midi_data: tuple):
    midi_object = pretty_midi.PrettyMIDI()
    cello = pretty_midi.Instrument(program=1)
    i = 0
    for element in midi_data:
        print(i) #print de debug a delete
        i+=1 #print de debug a delete
       
        # Create a Note instance for this note, starting at 0s and ending at .5s
        note = pretty_midi.Note(velocity=100, pitch=element[0], start=element[1], end=element[2])
        # Add it to our cello instrument
        cello.notes.append(note)
    midi_object.instruments.append(cello)
    midi_object.write('./Midi/sound.mid')


def loadAudio(wavFile: str) -> tuple[numpy.ndarray, int]:
    waveForm, sampleRate = librosa.load(wavFile)
    print("Number of samples : ", waveForm.shape)#print de debug a delete après
    print("Duration : ", librosa.get_duration(y=waveForm, sr=sampleRate))#print de debug a delete après
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
''' 
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
    plt.close(fig)'''

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

    return f0, pitchTimes

def aggregatePitchesByNote(f0: numpy.ndarray, pitchTimes: numpy.ndarray, onset_detect: numpy.ndarray, sampleRate: int, hopLength: int) -> numpy.ndarray:
    onset_times: numpy.ndarray = librosa.frames_to_time(onset_detect, sr=sampleRate, hop_length=hopLength)

    notePitches: list = []

    for i in range(len(onset_times)):
        startNote = onset_times[i]
        endNote = onset_times[i + 1] if i + 1 < len(onset_times) else pitchTimes[-1]

        masque = (pitchTimes >= startNote) & (pitchTimes < endNote)
        NoteFreq = f0[masque]

        PitchNote = numpy.median(NoteFreq)
        notePitches.append(PitchNote)

    return numpy.array(notePitches)

mp3ToMidi(r"./Song/PinkPanther_Piano_Only.mp3") #a changer le chemin d'acces pour le prochain utilisatuer