
import pretty_midi
midi_path = "wasd.midi"  # Remplacez par votre fichier MIDI
midi_data = pretty_midi.PrettyMIDI(midi_path)

class SoundExtract:

    @staticmethod
    def getNotesForIntru(IntruId:int=0):
        if (IntruId > len(midi_data.instruments)-1) : IntruId = len(midi_data.instruments)-1
        print(midi_data.instruments[IntruId].notes)
        # Rassembler toutes les notes de tous les instruments dans une seule liste triée par temps de début
        all_notes = []
        for instrument in midi_data.instruments:
            for note in instrument.notes:
                all_notes.append(note)
