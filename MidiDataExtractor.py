
import pretty_midi
from pretty_midi import Note

class MidiDataExtractor:

    def __init__(self, path:str):
        self.midi_data = pretty_midi.PrettyMIDI(path) 

    def getNotesForIntru(self, IntruId:int=0) -> list[Note]:
        if (IntruId > len(self.midi_data.instruments)-1) : IntruId = len(self.midi_data.instruments)-1
        return self.midi_data.instruments[IntruId].notes
        
    
    def getAllNotes(self) -> list[Note]:
        allNotes = []
        for instrument in self.midi_data.instruments:
            for note in instrument.notes:
                allNotes.append(note)
        return allNotes

    def getMidiDuration(self):
        allDur:float = 0
        for note in self.getAllNotes():
           allDur += note.duration
        return allDur

    def getNotesCount(self) -> int : 
        return len(self.getAllNotes())

    def getAvrgPitch(self) -> float :  
        allPitch:float = 0
        for note in self.getAllNotes():
            allPitch += note.pitch
        return allPitch / len(self.getAllNotes())

    def getAvrgVelo(self) -> float :  
        allVelo:float = 0
        for note in self.getAllNotes():
            allVelo += note.velocity
        return allVelo / len(self.getAllNotes())
    
