from music21 import *
import produce_song
from sklearn.model_selection import train_test_split
from keras.layers import *
from keras.models import *
from keras.callbacks import *
from keras.models import load_model
import keras.backend as k
from tensorflow import *

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
    #Initial loading of the midi file within the network
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
    for i in range(0, len(note), 1):
        input = note[i:i + timesteps]
        output = note[i]

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
    for j in i:
        print(x_int[j])
        temp.append(x_int[j])
    x_seq.append(temp)

x_seq = np.array(x_seq)

#Initialising training and evaluation values for CNN
x_train, x_eval, y_train, y_eval = train_test_split(x_seq, y_seq, test_size = 0.2, random_state = 0)

k.clear_session()
model = Sequential

model.add(Embedding(len(x_num), 100, input_length=32, trainable = True))

model.add(Conv1D(64,3, padding='causal',activation='relu'))
model.add(Dropout(0.2))
model.add(MaxPool1D(2))
    
model.add(Conv1D(128,3,activation='relu',dilation_rate=2,padding='causal'))
model.add(Dropout(0.2))
model.add(MaxPool1D(2))

model.add(Conv1D(256,3,activation='relu',dilation_rate=4,padding='causal'))
model.add(Dropout(0.2))
model.add(MaxPool1D(2))
          
model.add(GlobalMaxPool1D())
    
model.add(Dense(256, activation='relu'))

model.add(Dense(len(y_num), activation="softmax"))

model.compile(loss = "sparse_categorical_crossentropy", optimizer = 'adam')

model.summary()

#Finding and creating the best model
callback = ModelCheckpoint('bestmodel.h5', monitor='val_loss', mode='min', save_best_only=True, verbose=1)
history = model.fit(np.array(x_train), np.array(y_train), batch_size=128, epochs=50, validation_data=(np.array(x_eval), np.array(y_eval)), verbose=1, callbacks=[callback])

model = load_model('best_model.h5')

rand = np.random.randint(0, len(x_eval) - 1)
random_song = x_eval[rand]

prediction = []

for i in range(30):
    #Create a new song by predicting notes based on WaveNet CNN
    random_song = random_song.reshape(1, timesteps)

    prob = model.predict(random_song)[0]
    y_pred = np.argmax(prob, axis = 0)
    prediction.append(y_pred)

    random_song = np.insert(random_song[0], len(random_song[0]), y_pred)
    random_music = random_music[1:]

x_int = dict((number, note) for number, note in enumerate(x_num))
pred_notes = [x_int[i] for i in prediction]

produce_song.produce_midi(pred_notes)
