import librosa as lr
import os
import math
import numpy as np
import scipy.io.wavfile as wav
import sys
import random

def calculate_x(human, noise):
    energyh = np.sum(np.power(human, 2))/len(human)
    energyn = np.sum(np.power(noise, 2))/len(noise)
    x = math.sqrt(energyh/energyn/(10**(int(db)/20))) # x1要乘上雜訊s1
    
    return x

def energy(pcm):
    energy_pcm = np.sum(np.power(pcm, 2))/len(pcm)
    return energy_pcm

def snr_cal(x, y):
    ex = np.sum(np.power(x, 2))/len(x)
    ey = np.sum(np.power(y, 2))/len(y)
    snr = 20*math.log(ex/ey,10) 

    return snr

audio1 = sys.argv[1]
audio2 = sys.argv[2]
db_variance = sys.argv[3]

pcm1, sample_rate1 = lr.load(audio1, sr=16000)
#sample_rate1, pcm1 = wav.read(audio1)
print('audio1 sample rate: ', sample_rate1)
pcm2, sample_rate2 = lr.load(audio2, sr=16000)
#sample_rate2, pcm2 = wav.read(audio2)
print('audio2 sample rate: ', sample_rate2)

print('audio1 energy: ', energy(pcm1))
print('audio2 energy: ', energy(pcm2))

# x is the coefficinet for adjusting the pcm2
x = math.sqrt(energy(pcm1)/energy(pcm2)/(10**(int(db_variance)/20)))
print('x: ', x)
pcm2 = pcm2*x
print('audio2 energy after adjsut: ',  energy(pcm2))

pcm2 = pcm2*32768
wav.write(audio1.split('.')[0]+'_'+audio2.split('.')[0]+'_'+db_variance+'.wav', 16000, pcm2.astype(np.int16))
