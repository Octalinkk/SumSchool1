from SoundExtract import *

print ("Project start mdr")
extract = SoundExtract(mp3ToMidi(r"C:\Users\adrie\Documents\SummerSchool1\SumSchool1\Song\pinkPanther_Both.mp3")) 

print("========================================")
print("============= Instrument 1 =============")
print("========================================")
var1 = extract.getNotesForIntru(0)
print('\n')
print("========================================")
print("============= Instrument 2 =============")
print("========================================")
var2 = extract.getNotesForIntru(1)