from socket import SO_LINGER
import librosa
import librosa.display
from scipy.io import wavfile
import numpy as np
import os

#For after prepare song
#TODO: See how many similar frequencies (represented by number -1 to 1) are in the array
#TODO: Focus on the similar numbers, these similarities are going to pair to make desired sound

#Initialising dataset
dir = "DataSet/Wet Leg/Wet Leg/"
music = [i for i in os.listdir(dir) if i.endswith(".wav")]

def soundToInt(SD):
    #Converting song data from original float value to more interpretable int
    return [ int(s*32768) for s in SD]

def soundToFloat(SD):
    #Reversing previous function
    return np.array([ np.float32((s>>2)/(32768.0)) for s in SD])

def prepare_song(song_path):
    print("LOADING SONG...", song_path)
    audio_data = []

    #y is the song file as an array, sr is the sample rate at 22hz, the first 10 seconds are clipped
    #With 30 second clips being taken
    y,sr = librosa.load(song_path, sr=22050, offset=10.0, duration=30.0, dtype="float32") #standard sample rate of 22hz

    audio_data = np.array(y)
    return audio_data

prepare_song("DataSet/Wet Leg/Wet Leg/05 Wet Dream.wav")

def group_freq(data_arr):
    #Creating arrays for each frequency range
    high_freq = [] #1
    midhigh_freq = []
    mid_freq = [] #0
    midlow_freq =[]
    low_freq = [] #-1

    for i in data_arr:
        #Song array range is from 1 (high frequency) to -1 (low frequency)
        if data_arr[i] <= 1 & data_arr[i] >= 0.6:
            high_freq.append(data_arr(i))
        elif data_arr[i] < 0.6 & data_arr[i] > 0.2:
            midhigh_freq.append(data_arr(i))
        elif data_arr[i] < 0.2 & data_arr[i] > -0.2:
            mid_freq.append(data_arr(i))
        elif data_arr[i] < 0.2 & data_arr[i] > 0.6:
            midlow_freq.append(data_arr(i))
        elif data_arr[i] < -0.6 & data_arr[i] >= -1:
            low_freq.append(data_arr(i))

    return high_freq, midhigh_freq, mid_freq, midlow_freq, low_freq

def convert_to_song(song_array):
    #To be used to convert a new array created by CNN to WAV file
    song_array = []
    sr = 22050
    wavfile.write("test_file.wav", sr, song_array.uniform(-1, 1))
