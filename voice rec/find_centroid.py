from dtw import dtw
import matplotlib.pyplot as plt
import numpy as np
import librosa
import copy
import time
import serial
import wave

D_E_B_U_G = False
T_I_M_E = True
NUM_SAMPLES = 10

def findCentroid (mfccVec):
	distList = [None] * (NUM_SAMPLES)
	for i in range(0, NUM_SAMPLES):
		m1 = np.array(mfccVec[i])
		distTemp = 0
		for j in range (0, NUM_SAMPLES):
			if (i != j):
				m2 = np.array(mfccVec[j])
				distTemp = distTemp + dtw(m1.T, m2.T,dist = lambda x, y: np.exp(np.linalg.norm(x - y, ord=1)))[0]

		distList[i] = distTemp
	return distList

# REMOVE MEAN AND NORMALIZE EACH COLUMN OF MFCC
def preprocess_mfcc(mfcc):
	mfcc_cp = copy.deepcopy(mfcc)
	for i in range(mfcc.shape[1]):
		mfcc_cp[:,i] = mfcc[:,i] - np.mean(mfcc[:,i])
		mfcc_cp[:,i] = mfcc_cp[:,i]/np.max(np.abs(mfcc_cp[:,i]))
	return mfcc_cp



train_names = np.array(['branco', 'azul', 'vermelho'])
min_ov = 99999
for tr_ch in range(3):

	train_chosen = train_names[tr_ch]

	if T_I_M_E:
		elp = time.time()

	y1, sr1 = librosa.load('audio_samples/' + train_chosen + '_train1.wav')
	y2, sr2 = librosa.load('audio_samples/' + train_chosen + '_train2.wav')
	y3, sr3 = librosa.load('audio_samples/' + train_chosen + '_train3.wav')
	y4, sr4 = librosa.load('audio_samples/' + train_chosen + '_train4.wav')
	y5, sr5 = librosa.load('audio_samples/' + train_chosen + '_train5.wav')
	y6, sr6 = librosa.load('audio_samples/' + train_chosen + '_train6.wav')
	y7, sr7 = librosa.load('audio_samples/' + train_chosen + '_train7.wav')
	y8, sr8 = librosa.load('audio_samples/' + train_chosen + '_train8.wav')
	y9, sr9 = librosa.load('audio_samples/' + train_chosen + '_train9.wav')
	y10, sr10 = librosa.load('audio_samples/' + train_chosen + '_train10.wav')

	if T_I_M_E:
		elp = time.time() - elp
		print('TIME TO LOAD TRAIN: ' + str(elp))
		elp = time.time()


	mfccTemp = [None] * NUM_SAMPLES
	mfccTemp[0] = librosa.feature.mfcc(y1, sr1)
	mfccTemp[1] = librosa.feature.mfcc(y2, sr2)
	mfccTemp[2] = librosa.feature.mfcc(y3, sr3)
	mfccTemp[3] = librosa.feature.mfcc(y4, sr4)
	mfccTemp[4] = librosa.feature.mfcc(y5, sr5)
	mfccTemp[5] = librosa.feature.mfcc(y6, sr6)
	mfccTemp[6] = librosa.feature.mfcc(y7, sr7)
	mfccTemp[7] = librosa.feature.mfcc(y8, sr8)
	mfccTemp[8] = librosa.feature.mfcc(y9, sr9)
	mfccTemp[9] = librosa.feature.mfcc(y10, sr10)
	
	mfccVec = [None] * NUM_SAMPLES
	# # PREPROCESS MFCC
	for i in range (0,NUM_SAMPLES):		
		mfccVec[i] = preprocess_mfcc(mfccTemp[i])

	distList = findCentroid (mfccVec)
	# print (distList)
	idx = distList.index(min(distList))

	print ("Para a cor " + train_chosen + ", o centróide é o elemento nº" + str(idx + 1))

