from dtw import dtw
import matplotlib.pyplot as plt
import numpy as np
import librosa
import copy
import time
import serial
import pyaudio
import wave

# REMOVE MEAN AND NORMALIZE EACH COLUMN OF MFCC
def preprocess_mfcc(mfcc):
	mfcc_cp = copy.deepcopy(mfcc)
	for i in range(mfcc.shape[1]):
		mfcc_cp[:,i] = mfcc[:,i] - np.mean(mfcc[:,i])
		mfcc_cp[:,i] = mfcc_cp[:,i]/np.max(np.abs(mfcc_cp[:,i]))
	return mfcc_cp

def selectColor (mfccVec, userInput):
	distList = [None] * (NUM_CENTROIDS)
	for i in range(0, NUM_CENTROIDS):
		m1 = np.array(mfccVec[i])
		distList[i] = dtw(m1.T, userInput.T,dist = lambda x, y: np.exp(np.linalg.norm(x - y, ord=1)))[0]
		
	return distList.index(min(distList)) 

	
D_E_B_U_G = True
T_I_M_E = True
USING_ARDUINO = False
SAVE_AUDIO = False
NUM_CENTROIDS = 30

train_names = np.array(['branco', 'azul', 'vermelho'])

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 2
WAVE_OUTPUT_FILENAME = "output_audio.wav"
audio = pyaudio.PyAudio()

if (USING_ARDUINO):
	serialPort = "COM6"
	comport = serial.Serial(serialPort, 9600)
	time.sleep(1)
	
'''
y1, sr1 = librosa.load('audio_samples/branco_train3.wav')
y2, sr2 = librosa.load('audio_samples/azul_train1.wav')
y3, sr3 = librosa.load('audio_samples/vermelho_train2.wav')
'''

mfccTemp = [None] * NUM_CENTROIDS
mfccVec = [None] * NUM_CENTROIDS

cnt = -1
for j in range (3):
	for i in range (1, 11):
		cnt += 1
		yTrain, srTrain = librosa.load('audio_samples/' + train_names[j] + '_train' + str(i) + '.wav')
		mfccTemp[cnt] = librosa.feature.mfcc(yTrain, srTrain)

'''
mfccTemp[0] = librosa.feature.mfcc(y1, sr1)
mfccTemp[1] = librosa.feature.mfcc(y2, sr2)
mfccTemp[2] = librosa.feature.mfcc(y3, sr3)
'''

# # PREPROCESS MFCC
for i in range (0,NUM_CENTROIDS):		
	mfccVec[i] = preprocess_mfcc(mfccTemp[i])

# LOOP VOICE RECORDING AND ALGORITHM
while True:
	input("Press Enter to continue...")
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
	#audio.terminate()

	waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	waveFile.setnchannels(CHANNELS)
	waveFile.setsampwidth(audio.get_sample_size(FORMAT))
	waveFile.setframerate(RATE)
	waveFile.writeframes(b''.join(frames))
	waveFile.close()

	yTest, srTest = librosa.load(WAVE_OUTPUT_FILENAME)
	mfccTest = librosa.feature.mfcc(yTest,srTest)
	mfccTest = preprocess_mfcc(mfccTest)

	if T_I_M_E:
		elp = time.time()
		
	best_ch = selectColor (mfccVec, mfccTest)
	
	if T_I_M_E:
		elp = time.time() - elp
		print('TIME TO PROCESS: ' + str(elp))

		idx = best_ch
		if (idx < 10):
			best_ch = 0
		if ((idx >= 10) and (idx < 20)):
			best_ch = 1
		if (idx >= 20):
			best_ch = 2
				
	if D_E_B_U_G:
		print ("chosen color: " + train_names[best_ch])

	if (USING_ARDUINO):
		if (best_ch == 0):
			comport.write(b"w")
		elif (best_ch == 1):
			comport.write(b"b")
		elif (best_ch == 2):
			comport.write(b"r")
			
		
			



