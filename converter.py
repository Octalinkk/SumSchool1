import librosa
import numpy as numpy

from analys import detectOnSets, detectPitchesCqt, aggregatePitchesByNote
from midi_utilis import midi_builder, midi_writer

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