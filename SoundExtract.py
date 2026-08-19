
import pretty_midi
from pretty_midi import Note
import typing

class SoundExtract:

    def __init__(self, path:str):
        self.midi_data = pretty_midi.PrettyMIDI(path) 

    def getNotesForIntru(self, IntruId:int=0) -> typing.List[Note]:
        if (IntruId > len(self.midi_data.instruments)-1) : IntruId = len(self.midi_data.instruments)-1
        return self.midi_data.instruments[IntruId].notes
        # Rassembler toutes les notes de tous les instruments dans une seule liste triée par temps de début
        #all_notes = []
        #for instrument in self.midi_data.instruments:
        #    for note in instrument.notes:
        #        all_notes.append(note)
