import wave as wave
import pydub as pydub
import os 
import librosa
import pygame
import basic_pitch

from pydub import AudioSegment
from pydub import playback as playback
from pygame import mixer as mixer
from basic_pitch.inference import predict_and_save
from basic_pitch import ICASSP_2022_MODEL_PATH

def playAudio(filePath) :
    pygame.mixer.init(frequency=44000)      #44kHz frequence du wav il me semble
    pygame.mixer.music.load(filePath)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

def readFile(filePath) :
    w = wave.open(filePath, 'rb')  #rb veux dire read binary comme ça tu oublieras pas demain IDIOT!
    return w

def mp3ToWav(mp3File):
    song = AudioSegment.from_mp3(mp3File)
    wavFile = os.path.splitext(mp3File)[0] + ".wav"
    song.export(wavFile, format="wav")
    return wavFile 


def wavToMidi(wavFile):
    outputDir = os.path.dirname(wavFile)
    midiFile = os.path.join(outputDir, os.path.splitext(os.path.basename(wavFile))[0] + "_basic_pitch.mid")
    if os.path.exists(midiFile):
        os.remove(midiFile)

    predict_and_save(#code pris directment du repo git de la lib
        audio_path_list=[wavFile],
        output_directory=outputDir,
        save_midi=True,
        sonify_midi=False,
        save_model_outputs=False,
        save_notes=False,
        model_or_model_path=ICASSP_2022_MODEL_PATH,
    )
    
    return midiFile

def mp3ToMidi(fileName) :
    wavFile = mp3ToWav(fileName)
    midFile = wavToMidi(wavFile)
    return midFile

midiFile = mp3ToMidi(r"C:\Users\adrie\Documents\SummerSchool1\SumSchool1\Song\Ecossaise_Piano.mp3")

