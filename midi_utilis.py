import librosa
import numpy as numpy
import pretty_midi

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
        i+=1
       
        #Create a Note instance for this note, starting at 0s and ending at .5s
        note = pretty_midi.Note(velocity=100, pitch=element[0], start=element[1], end=element[2])
        #Add it to our cello instrument
        cello.notes.append(note)
    midi_object.instruments.append(cello)
    midi_object.write('./Midi/sound.mid')