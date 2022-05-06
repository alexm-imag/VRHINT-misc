# -*- coding: utf-8 -*-
"""
Created on Fri May  6 10:22:05 2022

@author: cocot
"""

import numpy as np;
from pydub import AudioSegment;
import sounddevice as sd;
import soundfile as sf;
import os;

hintDir = 'german-hint-adaptive-48kHz\\';
base_type = 'wav';
importDir = 'G:\VRHINT-misc\HINT-python\german-hint-adaptive-48kHz\\';

listIndex = 9;
dbLevel = -4;
sentenceIndex = 7;

randOrder = np.random.permutation(range(20));
testOrder = np.zeros(20);

#data, fs = sf.read("german-hint-adaptive-48kHz\\noiseGR_male.wav");
data, fs = sf.read(importDir + "noiseGR_male.wav");
sd.play(data, fs);
status = sd.wait();
#noise = AudioSegment.from_file(hintDir + "noiseGR_male.wav", base_type);
#sd.play(noise, 48000);


#%%
if listIndex < 10:
    filePath = hintDir + '0' + str(listIndex) + '\\' + 'list' + str(listIndex) + '.txt';
else:
    filePath = hintDir  + str(listIndex) + '\\' + 'list' + str(listIndex) + '.txt';

sentenceStrings = open(filePath).readlines();

#%%
if listIndex < 10:
    audioPath = hintDir + '0' + str(listIndex); 
else:
    audioPath = hintDir + str(listIndex); 

if dbLevel == 0:
    audioPath = audioPath + '\-' + str(dbLevel) + 'dB';
elif dbLevel > 0:
    audioPath = audioPath + '\+' + str(dbLevel) + 'dB';
else:
    audioPath = audioPath + '\\'  + str(dbLevel) + 'dB';

sentenceNum = sentenceIndex + (listIndex - 1) * 20;

if sentenceNum < 10:
    audioPath = audioPath + '\Ger_male00' + str(sentenceNum) + '.wav';
elif sentenceNum < 100:
    audioPath = audioPath + '\Ger_male0' + str(sentenceNum) + '.wav';
else:
    audioPath = audioPath + '\Ger_male' + str(sentenceNum) + '.wav';

sound = AudioSegment.from_file(audioPath, base_type);


 #%%  
chnNums = max([audioStruct["Channel"]]);
print("Channels: " + chnNums);

buffer = np.zeros(buflen);

# preallocate buffer    
for i in range(chnNums-1):
    buffer.append(np.zeros(buflen));

for i in range(len(audioStruct)):
    # check for channel dublications
    if (max(buffer(audioStruct[i]["Channel"])) > 0):
        buffer[audioStruct[i]["Channel"]] += audioStruct[i]["AudioData"][1:min(buflen, len(audioStruct[i]["AudioData"]))];

        if (max(buffer[audioStruct[i]["Channel"]]) > 1):
            print("Warning: Clipping on channel " + audioStruct[i]["Channel"]);
    else:
        buffer[audioStruct[i]["Channel"]] = audioStruct[i]["AudioData"][1:min(buflen, len(audioStruct[i]["AudioData"]))];
    