# -*- coding: utf-8 -*-
"""
Created on Fri May 20 09:19:25 2022

@author: Alexander Mueller
"""

import numpy as np;
import json;
import soundfile as sf;


class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """
    def default(self, obj):
        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
                            np.int16, np.int32, np.int64, np.uint8,
                            np.uint16, np.uint32, np.uint64)):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32,
                              np.float64)):
            return float(obj)
        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
    

def loadSentenceAudio(listIndex, sentenceIndex, dbLevel, hintDir):

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

    data,fs = sf.read(audioPath);
    return data;


def loadListSentences(listIndex, hintDir):
    
    if listIndex < 10:
        filePath = hintDir + '0' + str(listIndex) + '\\' + 'list' + str(listIndex) + '.txt';
    else:
        filePath = hintDir  + str(listIndex) + '\\' + 'list' + str(listIndex) + '.txt';
    
    return open(filePath, "r", encoding='utf8').readlines();


def circularNoise(noise, segmentLen, noiseIndex):

    noiseLen = len(noise);

    if circularNoise.counter == 0:
        circularNoise.counter = noiseLen;


    if circularNoise.counter != noiseLen:
        circularNoise.counter = noiseLen;
        # reset noiseIndex if a new noise was submitted!
        noiseIndex = 0;
        print("New noise file detected");


    noiseBuf = noise;
    print("Len: " + str(segmentLen) + " noiseInd: " + str(noiseIndex) + " noiseLen: " + str(noiseLen));

    # circ case
    if noiseIndex + segmentLen > noiseLen:
        print("Circ overflow");
        #print("nL - NI+1: " + str(len(0:noiseLen - noiseIndex)) + " nI:NL " + str(len(noiseIndex:noiseLen)));
        noiseBuf[0:noiseLen - noiseIndex] = noise[noiseIndex:noiseLen];
        #print("nL - NI+1: " + str(length(noiseLen - noiseIndex:segmentLen)) + " nI:NL " + str(length(1:segmentLen - (noiseLen - noiseIndex))))
        noiseBuf[noiseLen - noiseIndex + 1:segmentLen] = noise[0:segmentLen - (noiseLen - noiseIndex)];
        noiseIndex = segmentLen - (noiseLen - noiseIndex);
    else:
        noiseBuf = noise[noiseIndex:noiseIndex + segmentLen];
        noiseIndex = noiseIndex + segmentLen;
    

    print("Post noiseInd: " + str(noiseIndex));
    
    return noiseBuf, noiseIndex;
