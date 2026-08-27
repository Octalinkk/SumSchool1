import os
import librosa
import numpy as np
import pretty_midi

def detectOnSets(waveForm: np.ndarray, sampleRate: int, hopLength: int):
    stft_complex = librosa.stft(waveForm, hop_length=hopLength)
    logS = librosa.amplitude_to_db(np.abs(stft_complex), ref=np.max)

    onset_env = librosa.onset.onset_strength(S=logS, sr=sampleRate, hop_length=hopLength)
    onset_peaks = librosa.util.localmax(onset_env)
    onset_detect = librosa.onset.onset_detect(
        onset_envelope=onset_env, 
        sr=sampleRate, 
        hop_length=hopLength,
    )
    return onset_env, onset_peaks, onset_detect


def detectPolyphonicPitches(waveForm: np.ndarray, sampleRate: int, hopLength: int, peakTreshold: float = 0.20):
    y_harmonic, _ = librosa.effects.hpss(waveForm)
    binsPerOctaves = 36
    numberOctaves = 6
    fmin = librosa.note_to_hz('A2')
    cqtMatrix = np.abs(librosa.cqt(
        y_harmonic,
        sr=sampleRate,
        hop_length=hopLength,
        fmin=fmin,
        bins_per_octave=binsPerOctaves,
        n_bins=binsPerOctaves * numberOctaves)
    )

    normC = librosa.util.normalize(cqtMatrix, axis=0)
    local_peaks = librosa.util.localmax(normC, axis=0)

    peak_mask = local_peaks & (normC >= peakTreshold)

    midi_numbers = librosa.cqt_frequencies(
        n_bins=binsPerOctaves * numberOctaves, fmin=fmin, bins_per_octave=binsPerOctaves
    )
    midi_pitches = np.round(librosa.hz_to_midi(midi_numbers)).astype(int)

    harmonic_intervals = [12, 19, 24, 28, 31]

    framesPitches = []
    nFrames = normC.shape[1]
    for t in range(nFrames):
        active_bins = np.where(peak_mask[:, t])[0]
        if len(active_bins) > 0:
            notes = sorted(np.unique(midi_pitches[active_bins]))
            clean_notes = []
            for n in notes:
                if not any(abs((n - fund) - h) <= 1 for fund in clean_notes for h in harmonic_intervals):
                    clean_notes.append(n)

            framesPitches.append(clean_notes)
        else:
            framesPitches.append([])

    pitchTimes = librosa.times_like(normC[0], sr=sampleRate, hop_length=hopLength)
    return framesPitches, pitchTimes

def aggregatePitchPolyphonic(framePitches : list, pitchTime : np.ndarray, onsetDetect : np.ndarray, 
                             sampleRate : int, hopLength : int, minOccurenceRato : float = 0.50) -> tuple[list[list[int]], np.ndarray]:
    onset_times = librosa.frames_to_time(onsetDetect, sr=sampleRate, hop_length=hopLength)
    notePitches = []

    for i in range(len(onset_times)):
        startNote = onset_times[i]
        if(i+1 < len(onset_times)):
            endNote = onset_times[i+1]
        else:
            endNote = pitchTime[-1]
            
        mask = (pitchTime >= startNote) & (pitchTime < endNote)
        indices = np.where(mask)[0]
        numFrames = len(indices)
        if numFrames == 0:
            notePitches.append([])
            continue

        segmentNotes = []
        for idx in indices:
            for note in framePitches[idx]:
                segmentNotes.append(int(note))

        if not segmentNotes:
            notePitches.append([])
            continue   
            
        uniqueNotes, occurrences = np.unique(segmentNotes, return_counts=True)
        minCount = max(1, int(numFrames * minOccurenceRato))
        validNotes = uniqueNotes[occurrences >= minCount]

        notePitches.append(validNotes.tolist())

    return notePitches, onset_times 

def midi_builder_poly(onset_times: np.ndarray, notePitches: list, total_duration: float) -> list[tuple[int, float, float]]:
    midi_data = []

    for n in range(len(onset_times)):
        notesInChord = set(notePitches[n])
        if not notesInChord:
            continue

        start_time = onset_times[n]
        if n + 1 < len(onset_times):
            end_time = onset_times[n + 1]
        else:
            end_time = total_duration

        for midi_pitch in notesInChord:
            if 0 <= midi_pitch <= 127:
                midi_data.append((int(midi_pitch), start_time, end_time))

    return midi_data

def midi_writer(midi_data: list, output_path: str = './Midi/sound.mid'):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    midi_object = pretty_midi.PrettyMIDI(resolution=600)
    piano = pretty_midi.Instrument(program=0)

    for pitch, start, end in midi_data:
        note = pretty_midi.Note(velocity=100, pitch=pitch, start=start, end=end)
        piano.notes.append(note)

    midi_object.instruments.append(piano)
    midi_object.write(output_path)


def wavToMidi(audioFile: str, outputFile: str = './Midi/sound.mid') -> None:
    hopLength = 512
    waveForm, sampleRate = librosa.load(audioFile, sr=None, mono=True)
    total_duration = librosa.get_duration(y=waveForm, sr=sampleRate)

    _, _, onset_detect = detectOnSets(waveForm, sampleRate, hopLength)
    f0, pitchTimes = detectPolyphonicPitches(waveForm, sampleRate, hopLength)

    notePitches, onset_times = aggregatePitchPolyphonic(f0, pitchTimes, onset_detect, sampleRate, hopLength)
    midi_data = midi_builder_poly(onset_times, notePitches, total_duration)
    
    midi_writer(midi_data, outputFile)
    print(f"MIDI généré dans : {outputFile} ({len(midi_data)} notes)")


def mp3ToMidi(fileName: str) -> None:
    wavToMidi(fileName)


if __name__ == "__main__":
    mp3ToMidi("./Song/PinkPanther_Piano_Only.mp3")