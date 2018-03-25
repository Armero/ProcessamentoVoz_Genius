from dtw import dtw
import matplotlib.pyplot as plt
import numpy as np
import librosa
import copy
#import IPython.display
#from IPython.display import Image
#%matplotlib inline

D_E_B_U_G = 0

EXTRA_TRAIN = 0

# REMOVE MEAN AND NORMALIZE EACH COLUMN OF MFCC
def preprocess_mfcc(mfcc):
	mfcc_cp = copy.deepcopy(mfcc)
	for i in range(mfcc.shape[1]):
		mfcc_cp[:,i] = mfcc[:,i] - np.mean(mfcc[:,i])
		mfcc_cp[:,i] = mfcc_cp[:,i]/np.max(np.abs(mfcc_cp[:,i]))
	return mfcc_cp

# LOAD TEMPLATE
y, sr = librosa.load('audio_samples/vermelho_template.wav')

if D_E_B_U_G:
	plt.plot(y)

# LOAD TEST FILE
#yTest, srTest = librosa.load('audio_samples/vermelho_test3.wav')
yTest, srTest = librosa.load('audio_samples/vermelho_bruno.wav')

# LOAD TRAINING DATA
y1, sr1 = librosa.load('audio_samples/vermelho_train1.wav')
y2, sr2 = librosa.load('audio_samples/vermelho_train2.wav')
y3, sr3 = librosa.load('audio_samples/vermelho_train3.wav')

if EXTRA_TRAIN:
	y4, sr4 = librosa.load('audio_samples/vermelho_train4.wav')
	y5, sr5 = librosa.load('audio_samples/vermelho_train5.wav')


# CONVERT DATA TO MFCC
mfcc1 = librosa.feature.mfcc(y1, sr1)
mfcc2 = librosa.feature.mfcc(y2, sr2)
mfcc3 = librosa.feature.mfcc(y3, sr3)
mfccTest = librosa.feature.mfcc(yTest,srTest)

if EXTRA_TRAIN:
	mfcc4 = librosa.feature.mfcc(y4, sr4)
	mfcc5 = librosa.feature.mfcc(y5, sr5)


# PREPROCESS MFCC
mfcc1 = preprocess_mfcc(mfcc1)
mfcc2 = preprocess_mfcc(mfcc2)
mfcc3 = preprocess_mfcc(mfcc3)
mfccTest = preprocess_mfcc(mfccTest)

if EXTRA_TRAIN:
	mfcc4 = preprocess_mfcc(mfcc4)
	mfcc5 = preprocess_mfcc(mfcc5)


window_size = mfcc1.shape[1]
dists = np.zeros(mfccTest.shape[1] - window_size)

for i in range(len(dists)):
	mfcci = mfccTest[:,i:i+window_size]
	dist1i = dtw(mfcc1.T, mfcci.T,dist = lambda x, y: np.exp(np.linalg.norm(x - y, ord=1)))[0]
	dist2i = dtw(mfcc2.T, mfcci.T,dist = lambda x, y: np.exp(np.linalg.norm(x - y, ord=1)))[0]
	dist3i = dtw(mfcc3.T, mfcci.T,dist = lambda x, y: np.exp(np.linalg.norm(x - y, ord=1)))[0]
	
	if EXTRA_TRAIN:
		dist4i = dtw(mfcc4.T, mfcci.T,dist = lambda x, y: np.exp(np.linalg.norm(x - y, ord=1)))[0]
		dist5i = dtw(mfcc5.T, mfcci.T,dist = lambda x, y: np.exp(np.linalg.norm(x - y, ord=1)))[0]
	
	if EXTRA_TRAIN:
		dists[i] = (dist1i + dist2i + dist3i + dist4i + dist5i)/5
	else:
		dists[i] = (dist1i + dist2i + dist3i)/3
	
		
if D_E_B_U_G:
	plt.plot(dists)
	
# SELECT MINIMUM DISTANCE WINDOW
word_match_idx = dists.argmin()

# CONVERT MFCC TO TIMDE DOMAIN
word_match_idx_bnds = np.array([word_match_idx,np.ceil(word_match_idx + window_size)])
samples_per_mfcc = 512
#samples_per_mfcc = 1024
#word_samp_bounds = (2/2) + (word_match_idx_bnds*samples_per_mfcc)
word_samp_bounds = 1 + (word_match_idx_bnds*samples_per_mfcc)

word_samp_bounds = np.array(word_samp_bounds, dtype=int)

#print(yTest.shape)
#print(word_samp_bounds[0])
#print(word_samp_bounds[1])

word = yTest[word_samp_bounds[0]:word_samp_bounds[1]]

print(dists)
np.savetxt('answer.csv', dists)

#librosa.output.write_wav('answer.wav',word,22000)


