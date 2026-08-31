import numpy as np
import pretty_midi
import os

def midi_builder_poly(
    onset_times: np.ndarray,
    notePitches: list[list[int]],
    instruments: list[str],
    total_duration: float
) -> list[tuple[int, float, float, str]]:
    midi_data = []

    for n in range(len(onset_times)):
        notesInChord = set(notePitches[n])
        if not notesInChord:
            continue

        start_time = onset_times[n]
        end_time = onset_times[n + 1] if n + 1 < len(onset_times) else total_duration
        instrument = instruments[n] if n < len(instruments) else "Piano"

        for midi_pitch in notesInChord:
            if 0 <= midi_pitch <= 127:
                midi_data.append((int(midi_pitch), start_time, end_time, instrument))

    return midi_data


def midi_writer(midi_data: list[tuple[int, float, float, str]], output_path: str = './Midi/sound.mid') -> None:
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    midi_object = pretty_midi.PrettyMIDI(resolution=600)
    piano = pretty_midi.Instrument(program=0, name="Piano")
    trumpet = pretty_midi.Instrument(program=56, name="Trumpet")

    for pitch, start, end, instrument in midi_data:
        note = pretty_midi.Note(velocity=100, pitch=pitch, start=start, end=end)
        if instrument == "Piano":
            piano.notes.append(note)
        else:
            trumpet.notes.append(note)

    if piano.notes:
        midi_object.instruments.append(piano)
    if trumpet.notes:
        midi_object.instruments.append(trumpet)

    midi_object.write(output_path)