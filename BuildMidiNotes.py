import  numpy, librosa, pretty_midi

# Simule le retour de detectPitches() pour une gamme de Do majeur
# (comme si chaque note durait ~0.5s, avec du silence/NaN entre les notes)

pitch_times = numpy.array([
    0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45,
    0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95,
    1.00, 1.05, 1.10, 1.15, 1.20, 1.25, 1.30, 1.35, 1.40, 1.45,
    1.50, 1.55, 1.60, 1.65, 1.70, 1.75, 1.80, 1.85, 1.90, 1.95
])

# fréquences correspondantes (Hz) : Do4, Ré4, Mi4, Fa4, Sol4, La4, Si4, Do5
# avec des NaN entre les notes pour simuler les silences/transitions
f0 = numpy.array([
    261.6, 261.6, 261.6, 261.6, numpy.nan,   # Do4 (C4) 60
    293.7, 293.7, 293.7, 293.7, numpy.nan,   # Ré4 (D4)
    329.6, 329.6, 329.6, 329.6, numpy.nan,   # Mi4 (E4)
    349.2, 349.2, 349.2, 349.2, numpy.nan,   # Fa4 (F4)
    392.0, 392.0, 392.0, 392.0, numpy.nan,   # Sol4 (G4)
    440.0, 440.0, 440.0, 440.0, numpy.nan,   # La4 (A4)
    493.9, 493.9, 493.9, 493.9, numpy.nan,   # Si4 (B4)
    523.3, 523.3, 523.3, 523.3, numpy.nan,   # Do5 (C5)
])

# Et pour rappel, ce que detectOnsets t'aurait donné en parallèle
# (les débuts de chaque note, en secondes)
onset_times = numpy.array([0.00, 0.20, 0.40, 0.60, 0.80, 1.00, 1.20, 1.40])




# rajouter la différentiation des instruments
def midi_builder(onset_times, pitch_times, f0):
    i = 0   
    midi_data = []
    for n, times in enumerate(onset_times):
        note = numpy.nan
        for i in range(pitch_times.size):
            if onset_times[n] == pitch_times[i]:
                while numpy.isnan(f0[i]) and i < f0.size:
                    i += 1
                note = round(librosa.hz_to_midi(f0[i]))
                if n < onset_times.size - 1:
                    duration = onset_times[n +1] - onset_times[n]
                    midi_data.append((note, onset_times[n], onset_times[n + 1]))
                else:
                    duration = pitch_times[pitch_times.size-1] - onset_times[n]
                    midi_data.append((note, onset_times[n], pitch_times[pitch_times.size-1]))
                print("note = ", note, " start = ", onset_times[n], "duration = ", duration) #print de debug a delete
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
    midi_object.write('sound.mid')


midi_writer(midi_builder(onset_times,pitch_times,f0))