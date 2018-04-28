from dtw import dtw
import matplotlib.pyplot as plt
import numpy as np
import librosa
import copy
import time
import serial
import pyaudio
import wave


#import IPython.display
#from IPython.display import Image
#%matplotlib inline

D_E_B_U_G = False
T_I_M_E = True
EXTRA_TRAIN = 0

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 2
WAVE_OUTPUT_FILENAME = "file.wav"
audio = pyaudio.PyAudio()

comport = serial.Serial("COM3", 9600)
time.sleep(2)

# REMOVE MEAN AND NORMALIZE EACH COLUMN OF MFCC
def preprocess_mfcc(mfcc):
	mfcc_cp = copy.deepcopy(mfcc)
	for i in range(mfcc.shape[1]):
		mfcc_cp[:,i] = mfcc[:,i] - np.mean(mfcc[:,i])
		mfcc_cp[:,i] = mfcc_cp[:,i]/np.max(np.abs(mfcc_cp[:,i]))
	return mfcc_cp


# LOAD TEST FILE
#yTest1, srTest1 = librosa.load('audio_samples/vermelho_test1.wav')
#yTest2, srTest2 = librosa.load('audio_samples/azul_test1.wav')
#yTest3, srTest3 = librosa.load('audio_samples/branco_test1.wav')
#yTest, srTest = librosa.load('audio_samples/vermelho_test1.wav')

# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
print ("recording...")
frames = []
 
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
print ("finished recording")
 
# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()

waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()

yTest, srTest = librosa.load(WAVE_OUTPUT_FILENAME)


train_names = np.array([ 'azul','vermelho', 'branco'])
min_ov = 99999
for tr_ch in range(3):

	train_chosen = train_names[tr_ch]

	if T_I_M_E:
		elp = time.time()

	# LOAD TRAINING DATA
	y1, sr1 = librosa.load('audio_samples/' + train_chosen + '_train1.wav')
	y2, sr2 = librosa.load('audio_samples/' + train_chosen + '_train2.wav')
	y3, sr3 = librosa.load('audio_samples/' + train_chosen + '_train3.wav')

	if T_I_M_E:
		elp = time.time() - elp
		print('TIME TO LOAD TRAIN: ' + str(elp))
		elp = time.time()

	#print(y1)
	#print('####################################################')
	#print(yTest)

	# CONVERT DATA TO MFCC
	mfcc1 = librosa.feature.mfcc(y1, sr1)
	mfcc2 = librosa.feature.mfcc(y2, sr2)
	mfcc3 = librosa.feature.mfcc(y3, sr3)
	mfccTest = librosa.feature.mfcc(yTest,srTest)

	# PREPROCESS MFCC
	mfcc1 = preprocess_mfcc(mfcc1)
	mfcc2 = preprocess_mfcc(mfcc2)
	mfcc3 = preprocess_mfcc(mfcc3)
	mfccTest = preprocess_mfcc(mfccTest)

	if T_I_M_E:
		elp = time.time() - elp
		print('TIME TO CONVERT AND PREPROCESS DATA: ' + str(elp))
		elp = time.time()

	window_size = mfcc1.shape[1]
	dists = np.zeros(mfccTest.shape[1] - window_size)

	for i in range(len(dists)):
		mfcci = mfccTest[:,i:i+window_size]
		dist1i = dtw(mfcc1.T, mfcci.T,dist = lambda x, y: np.exp(np.linalg.norm(x - y, ord=1)))[0]
		dist2i = dtw(mfcc2.T, mfcci.T,dist = lambda x, y: np.exp(np.linalg.norm(x - y, ord=1)))[0]
		dist3i = dtw(mfcc3.T, mfcci.T,dist = lambda x, y: np.exp(np.linalg.norm(x - y, ord=1)))[0]
		
		dists[i] = (dist1i + dist2i + dist3i)/3
		#dists[i] = dist1i

	if T_I_M_E:
		elp = time.time() - elp
		print('TIME TO TRAIN DATA: ' + str(elp))
		elp = time.time()

	word_match_idx = dists.argmin()

	if( min_ov > word_match_idx):
		min_ov = word_match_idx
		print('BEST: ', train_names[tr_ch])

		if (tr_ch == 0):
			comport.write(b"a")
			#comport.flush()
			#time.sleep(0.2)
			#comport.close()
		elif (tr_ch == 1):
			comport.write(b"v")
			#comport.close()
		elif (tr_ch == 2):
			comport.write(b"b")
			#comport.close()
		#comport.close()

			
if D_E_B_U_G:
	plt.plot(dists)
	
# SELECT MINIMUM DISTANCE WINDOW
word_match_idx = dists.argmin()

# CONVERT MFCC TO TIMDE DOMAIN
word_match_idx_bnds = np.array([word_match_idx,np.ceil(word_match_idx + window_size)])
samples_per_mfcc = 512
word_samp_bounds = 1 + (word_match_idx_bnds*samples_per_mfcc)
word_samp_bounds = np.array(word_samp_bounds, dtype=int)
word = yTest[word_samp_bounds[0]:word_samp_bounds[1]]


np.savetxt('answer.csv', dists)

#comport.write(b"a")
comport.close()

#librosa.output.write_wav('answer.wav',word,22000)


