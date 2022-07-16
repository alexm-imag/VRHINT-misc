# -*- coding: utf-8 -*-
"""
Created on Fri May 20 09:19:25 2022

@author: Alexander Mueller
"""

import numpy as np;
import os;
import json;
import soundfile as sf;
import datetime as dt;
import sounddevice as sd;

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
 
    
def getUserIndex():
     return len(os.listdir('results'));  
    
def exportResults(resultStorage, userIndex, userName):
    
    resultFileName = "results\\%s-%s-%s.json" % (userIndex, userName,  dt.datetime.now().strftime("%d-%m-%y--%H-%M-%S"));
    
    results = json.dumps(resultStorage, indent = 4, cls=NumpyEncoder);
    # store json into file
    with open(resultFileName, "w") as outfile:
        outfile.write(results)
        

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
    sd.default.samplerate = fs;
    
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



def playAudio(curr_sent, noise, condition, ChFront, ChLeft, ChRight):

    if condition == "noiseLeft":
        audioBuffer = np.array([curr_sent, noise[0:len(curr_sent)]]).transpose();
        sd.play(audioBuffer, blocking = 'true', mapping = [ChFront, ChLeft]);
    elif condition == "noiseRight":
        audioBuffer = np.array([curr_sent, noise[0:len(curr_sent)]]).transpose();
        sd.play(audioBuffer, blocking = 'true', mapping = [ChFront, ChRight]);
    elif condition == "noiseFront":
        sd.play(curr_sent + noise[0:len(curr_sent)], blocking = 'true', mapping = [ChFront]);
    else:
        sd.play(curr_sent, blocking = 'true', mapping = [ChFront]);
        
        
def playNoise(hintDir):
    noise, fs = sf.read(hintDir + "noiseGR_male.wav");   
    sd.play(noise, blocking = 'true', mapping = [1, 2]);


def playSentence(sentence):
    sd.play(sentence, blocking = 'true', mapping = [1, 2]);