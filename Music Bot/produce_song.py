from music21 import *

def produce_midi(prediction):
    offset = 0
    output = []

    for pattern in prediction:
        #Reversing the conversion of notes to ints, to create midi file
        if('.' in pattern) or pattern.isdigit():
            chord_note = pattern.split('.')
            notes = []

            for curr_note in chord_note:
                cn = int(curr_note)
                new_note = note.Note(cn)
                new_note.storedInstrument = instrument.Piano()
                notes.append(new_note)

            new_chord = chord.Chord(notes)
            new_chord.offset = offset
            output.append(new_chord)

        else:
            new_note = note.Note(pattern)
            new_note.offset = offset
            new_note.storedInstrument = instrument.Piano()

        offset += 1

    #Convert notes into midi file in local directory
    midi_stream = stream.Stream(output)
    midi_stream.write('midi', fp="DataSet/Samples/sample.mid")
