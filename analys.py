import librosa
import numpy as numpy

def detectOnSets(waveForm: numpy.ndarray, sampleRate: int, hopLength: int) -> tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray]:
    stft_complex: numpy.ndarray = librosa.stft(waveForm, hop_length=hopLength)
    logS: numpy.ndarray = librosa.amplitude_to_db(numpy.abs(stft_complex), ref=numpy.max)

    onset_env = librosa.onset.onset_strength(S=logS, sr=sampleRate, hop_length=hopLength)
    onset_peaks = librosa.util.localmax(onset_env)
    onset_detect = librosa.onset.onset_detect(
        onset_envelope=onset_env, sr=sampleRate, hop_length=hopLength
    )       
    return onset_env, onset_peaks, onset_detect

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