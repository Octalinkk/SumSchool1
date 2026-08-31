import librosa
from AudioAnalyser import *
from AudioWriter import *

def audioToMidi(audioFile: str, outputFile: str = './Midi/sound.mid') -> None:
    hopLength = 512
    waveForm, sampleRate = librosa.load(audioFile, sr=None, mono=True)
    total_duration = librosa.get_duration(y=waveForm, sr=sampleRate)

    stft_complex = librosa.stft(y=waveForm, hop_length=hopLength)
    _, _, onset_detect = detectOnSets(waveForm, sampleRate, hopLength)
    f0, pitchTimes = detectPolyphonicPitches(waveForm, sampleRate, hopLength)

    instruments = classifyInstrumentsByOnset(stft_complex, onset_detect)
    notePitches, onset_times = aggregatePitchPolyphonic(f0, pitchTimes, onset_detect, sampleRate, hopLength)
    midi_data = midi_builder_poly(onset_times, notePitches, instruments, total_duration)

    midi_writer(midi_data, outputFile)
    print(f"Fichier MIDI généré avec succès : {outputFile} ({len(midi_data)} notes écrites)")
