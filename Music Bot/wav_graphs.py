#import IPython
import librosa
import sklearn
import matplotlib.pyplot as plt
import librosa.display

song = "DataSet/Wet Leg/Wet Leg/05 Wet Dream.wav"
y, sr = librosa.load(song, sr=22050) #standard sample rate of 22hz
#print(y) #Shows the initial unfiltered array of the WAV file
print(y.size())

def basic_spectrogram(y):
    plt.figure(figsize=(14, 5))
    librosa.display.waveshow(y, sr=sr)
    plt.show()

def stft_spectrogram(y):
    X = librosa.stft(y)
    Xdb = librosa.amplitude_to_db(abs(X))
    plt.figure(figsize=(14, 5))
    librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='hz') 
    librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='log')
    plt.colorbar()
    plt.show()

def centroid_spectogram(y):
    spectral_centroids = librosa.feature.spectral_centroid(y, sr=sr)[0]
    spectral_centroids.shape

    # Computing the time variable for visualization
    frames = range(len(spectral_centroids))
    t = librosa.frames_to_time(frames)
    # Normalising the spectral centroid for visualisation
    def normalize(y, axis=0):
        return sklearn.preprocessing.minmax_scale(y, axis=axis)
    #Plotting the Spectral Centroid along the waveform
    librosa.display.waveshow(y, sr=sr, alpha=0.4)
    plt.plot(t, normalize(spectral_centroids), color='r')
    plt.show()

#inp = input("Do you want to look at songs: \n 1. Spectogram ('s') \n 2. Short-Time Fourier Transform (stft) \n 3. Spectoral Centroid (sc) \n ???")

#if(inp =="s"):
#    basic_spectrogram(y)
#elif(inp == "stft"):
#    stft_spectrogram(y)
#elif("sc"):
#    centroid_spectogram(y)