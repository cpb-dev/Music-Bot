from music21 import *
import os
import numpy as np

dir = 'DataSet/Midi Set/'
music = [i for i in os.listdir(dir) if i.endswith(".mid")]
# http://www.piano-midi.de/  (Dataset used, beethoven specifically)

#test_song = converter.parse("DataSet/Midi Set/beethoven_opus10_1.mid", format="midi", forceSource = True, quantizePost = True)

def instruments(midi):
    #Method to scan midi file and find instruments used to compose song
    #Used for testing putposes only
    partStream = midi.parts.stream()
    print("instruments found: ")
    for p in partStream:
        aux = p
        print(p.partName)

#instruments(test_song)

def load_song(song):
    notes = []
    notes_parse = None

    #Initialise music21 converter
    midi = converter.parse(song)
    s2 = instrument.partitionByInstrument(midi)

    for part in s2.parts:
        if "Piano" in str(part):
            #Checks the midi file for the piano tag, gathering just the notes
            notes_parse = part.recurse()

            for element in notes_parse:
                if isinstance(element, note.Note):
                    notes.append(str(element.pitch))
                elif isinstance(element, chord.Chord):
                    notes.append('.'.join(str(n) for n in element.normalOrder))
    
    return np.array(notes)

notes_arr = np.array([load_song(dir+i) for i in music])

#Seperating the notes within above array
notes = [element for note in notes_arr for element in note]
unique = list(set(notes))

note_music = np.array(notes)

timesteps = 32
x = []
y = []

for note in note_music:
    #Creating array to split some notes
    for i in range(0, len(note) - timesteps, 1):
        input = note[i:i + timesteps]
        output = note[i + timesteps]

        x.append(input)
        y.append(output)

x = np.array(x)
y = np.array(y)

#Giving integer values to each note
x_num = list(set(x.ravel()))
y_num = list(set(y))
x_int = dict((note, number) for number, note in enumerate(x_num))
y_int = dict((note, number) for number, note in enumerate(y_num))

x_seq = []
y_seq = np.array([y_int[i] for i in y])

for i in x:
    temp = []
    for i in note:
        temp.append(x_int[i])

x_seq = np.array(x_seq)