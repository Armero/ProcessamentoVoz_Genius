from dtw import dtw
#import matplotlib.pyplot as plt
import numpy as np
import librosa
import copy
import time
import serial
import wave
import random
import pyaudio

D_E_B_U_G = False
T_I_M_E = True
NUM_CENTROIDS = 3

def selectColor (mfccVec, userInput):
	distList = [None] * (NUM_CENTROIDS)
	for i in range(0, NUM_CENTROIDS):
		m1 = np.array(mfccVec[i])
		distList[i] = dtw(m1.T, userInput.T,dist = lambda x, y: np.exp(np.linalg.norm(x - y, ord=1)))[0]

	idx = distList.index(min(distList))
	color = ""
	if (idx == 0):
		color = "BRANCO"
	if (idx == 1):
		color = "AZUL"
	if (idx == 2):
		color = "VERMELHO"
		
	return color
    


# REMOVE MEAN AND NORMALIZE EACH COLUMN OF MFCC
def preprocess_mfcc(mfcc):
	mfcc_cp = copy.deepcopy(mfcc)
	for i in range(mfcc.shape[1]):
		mfcc_cp[:,i] = mfcc[:,i] - np.mean(mfcc[:,i])
		mfcc_cp[:,i] = mfcc_cp[:,i]/np.max(np.abs(mfcc_cp[:,i]))
	return mfcc_cp


y1, sr1 = librosa.load('audio_samples/branco_train3.wav')
y2, sr2 = librosa.load('audio_samples/azul_train1.wav')
y3, sr3 = librosa.load('audio_samples/vermelho_train2.wav')

mfccTemp = [None] * NUM_CENTROIDS
mfccTemp[0] = librosa.feature.mfcc(y1, sr1)
mfccTemp[1] = librosa.feature.mfcc(y2, sr2)
mfccTemp[2] = librosa.feature.mfcc(y3, sr3)

mfccVec = [None] * NUM_CENTROIDS

# # PREPROCESS MFCC
for i in range (0,NUM_CENTROIDS):		
	mfccVec[i] = preprocess_mfcc(mfccTemp[i])

train_names = np.array(['branco', 'azul', 'vermelho'])

if T_I_M_E:
	elp = time.time()
	
for j in range (0, 3):
	train_chosen = train_names[j]
	#for i in range (1, 4):
	for i in range (1, 7):
		
		if T_I_M_E:
			elp = time.time()	
			
		yTest, srTest = librosa.load('audio_samples/' + train_chosen + '_test' +str(i)+ '.wav')	
		mfccTest = librosa.feature.mfcc(yTest,srTest)
		mfccTest = preprocess_mfcc(mfccTest)
		color = selectColor (mfccVec, mfccTest)
		print ("Para a amostra  //" + train_chosen + "_test" + str(i) + "//  a cor identificada é " + color )
		
		if T_I_M_E:
			elp = time.time() - elp
			print('TIME TO PROCESS: ' + str(elp))

'''
for j in range (0, 3):
    for i in range (1, 10):
        train_chosen = train_names[j]

        # LOAD TRAINING DATA
        # REMOVE CENTROID ITSELF
        if ( not((j == 0) and i == 3) and \
            not((j == 1) and i == 1) and \
            not((j == 2) and i == 2)):

            if T_I_M_E:
                elp = time.time()

            yTest, srTest = librosa.load('audio_samples/' + train_chosen + '_train' +str(i)+ '.wav')
            mfccTest = librosa.feature.mfcc(yTest,srTest)
            mfccTest = preprocess_mfcc(mfccTest)
            color = selectColor (mfccVec, mfccTest)
            print ("Para a amostra  " + train_chosen + "_" + str(i) +", a cor identificada é " + color )
            
            if T_I_M_E:
                elp = time.time() - elp
                print('TIME TO PROCESS: ' + str(elp))
'''