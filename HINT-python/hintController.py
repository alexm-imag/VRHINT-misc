# -*- coding: utf-8 -*-
"""
Created on Thu May  5 13:52:26 2022

@author: Alexander Mueller
"""

import numpy as np;
import json;
import soundfile as sf;
import sounddevice as sd;
import csv;
import datetime as dt;
import os;

#%%
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

    
# %%
hintDir = 'german-hint-adaptive-48kHz\\';
base_type = 'wav';
importDir = 'G:\VRHINT-misc\HINT-python\german-hint-adaptive-48kHz\\';

# Test setup
# lists open for test
availableTestLists = 10;
# number of lists used in the test
numTestLists = 5;
# number of sentences in each list
listSentences = 20;

# %%
# min/max available SNR
minSNR = -16;
maxSNR = 2;

# practice setup
practiceList = 12;
practiceRounds = 5;
practiceCondition = "noiseLeft";

# %% Type definitions etc

# this format works for sentence indices, SNR values and hit Quotes
templateData = np.zeros(listSentences);
templateCondition = "noiseLeft";
templateListIndex = 12;

resultTemplate = {
    "ListIndex": templateListIndex,
    "Condition": templateCondition,
    "SNRs": templateData,
    "HitQuotes:": templateData,
    "Time": dt.datetime.now().strftime("%d-%m-%y--%H-%M-%S")};

# allocate numTestLists structs to store results
resultStorage = [resultTemplate for k in range(numTestLists)];
    

with open('lqConditions.csv', mode ='r')as file:
  lqConditions = list(csv.reader(file));
        
with open('lqLists.csv', mode ='r')as file:
  lqLists = list(csv.reader(file));

# convert List<List<str>> to List<List<int>>
for i in range(len(lqLists)):
    lqLists[i] = [int(j) for j in lqLists[i]];


#%% user login
print("Enter participants name:");
name = input();
# add system to check if username has already been used!
# create file name based on user name
resultFileName = "results\\results-%s-%s.json" % (name,  dt.datetime.now().strftime("%d-%m-%y--%H-%M-%S"));
practiceFileName = "results\\results-%s-%s.json" % (name,  dt.datetime.now().strftime("%d-%m-%y--%H-%M-%S"));

#%% load noise
calibrationNoise, fs = sf.read(importDir + "NBNoise1000.wav");
noise, fs = sf.read(importDir + "noiseGR_male.wav");
sd.default.samplerate = fs;

#%% Initialize playrec
#init_playrec(fs);

# define channel map
#ChMap= [1 3 5]; % uni setup
#ChLeft = 1;
#ChFront = 3;
#ChRight = 5;

ChMap = [1, 2]; # at home
ChLeft = 1;
ChRight = 2;
# only have 2 channels here so do this for testing...
ChFront = 2;

#%% Load counterbalanced test order
userIndex = len(os.listdir('results'));
print("User Index is: " + str(userIndex));
print("Is this correct? y/n");
if str(input()) != 'y':
    exit();

# this will be determined by number of result files!
testLists = lqLists[userIndex % availableTestLists];

# pre-allocate text array
testConditions = ["emptyCondition" for k in range(numTestLists)]; 

# userIndex determines start line of lqConditions matrix
# 5th condition is taken from the next line (considering wrapping!)
testConditions[0:4] = lqConditions[userIndex % len(lqConditions)];
testConditions[4] = lqConditions[(userIndex + 1) % len(lqConditions)][0];

#%% start practice condition 
sentences = loadListSentences(practiceList, hintDir);
randOrder = np.random.permutation(range(20));

# store SNR for each sentence
listSNR = np.zeros(20);
# store hitQuote for each sentence
hitQuotes = np.zeros(20);

# starting at 0 dB
currentSNR = 0;
noiseIndex = 1;

for i in range(practiceRounds):
    # get random index
    index = randOrder[i];
    # load current sentence
    sentencePath = [hintDir + '0' + str(practiceList) + '\-0dB\Ger_male00' + str(index) + '.wav'];

    print(["Current playback level: " + str(currentSNR)]);
    print(["Round " + str(i) + " out of " + str(practiceRounds)]);
    # audio files are labeled from Ger_male001 and not Ger_male000 so add '1'
    curr_sent = loadSentenceAudio(practiceList, index + 1, currentSNR, importDir);
        
    #noiseSegment = noise[0:len(curr_sent)];
    #[noiseSegment, noiseIndex] = circularNoise(noise, sentLen, noiseIndex);

    audioBuffer = np.array([curr_sent, noise[0:len(curr_sent)]]).transpose();
    
    # get length of current sentence
    sentenceLength = len(sentences[index].split());
   
    # print out current sentence string
    print("Sentence length: " + str(sentenceLength))
    print(sentences[index]);
    
    sentLen = len(curr_sent);

    if practiceCondition == "noiseLeft":
        sd.play(audioBuffer, blocking = 'true', mapping = [ChFront, ChLeft]);
    elif practiceCondition == "noiseRight":
        sd.play(audioBuffer, blocking = 'true', mapping = [ChFront, ChRight]);
    elif practiceCondition == "noiseFront":
        sd.play(curr_sent + noise[0:len(curr_sent)], blocking = 'true', mapping = [ChFront]);
    else:
        sd.play(audioBuffer[0], blocking = 'true', mapping = [ChFront]);


    # get experimenter feedback
    print("How many words have been correct?");
    correctWords = int(input());
    #print(type(correctWords));

    # alternative: just ask if below or above 50% hit
    # less data but quicker
    while correctWords > sentenceLength:
        print("Invalid input. Try again!");
        print("How many words have been correct?");
        correctWords = input();
    
    print('Sentence len: ' + str(sentenceLength) + ' correct: ' + str(correctWords));
    hitQuote = correctWords / sentenceLength;
    print("HitQuote: " + str(hitQuote));


    # adapt SNR based on hitQuote
    if i < 4 :        
        if hitQuote < 0.5:
            currentSNR = currentSNR + 4;
        else:
            currentSNR = currentSNR - 4;
    else:
        # store sentence data
        hitQuotes[i] = hitQuote;
        listSNR[i] = currentSNR;
        
        # adapt SNR based on hitQuote
        if hitQuote < 0.5:
            currentSNR = currentSNR + 2;
        else:
            currentSNR = currentSNR - 2;


    # SNR sanity check
    if currentSNR < minSNR:
        currentSNR = minSNR;
        print(["Warning: reached min SNR!" + str(minSNR)]);
    elif currentSNR > maxSNR:
        currentSNR = maxSNR;
        print(["Warning: reached max SNR!" + str(maxSNR)]);


print("Practice done!");

#%% Test JSON format
# fill struct with list data
pracRes = resultTemplate;
pracRes["ListIndex"] = practiceList;
pracRes["Condition"] = practiceCondition;
pracRes["SNRs"] = listSNR;
pracRes["HitQuotes"] = hitQuotes;

# parse struct into json
practiceResults = json.dumps(pracRes, indent = 4, cls=NumpyEncoder);
# store json into file
with open(practiceFileName, "w") as outfile:
    outfile.write(practiceResults)

#%% Test procedure
for j in range(numTestLists):

    sentences = loadListSentences(testLists[j], hintDir);
    randOrder = np.random.permutation(range(20));
    currentCondition = testConditions[j];
    
    # store SNR for each sentence
    listSNR = np.zeros(20);
    # store hitQuote for each sentence
    hitQuotes = np.zeros(20);
    
    # starting at 0 dB
    currentSNR = 0;
    noiseIndex = 1;


    print(["Starting List " + str(testLists[j]) + " with condition" + testConditions[j]]);

    for i in range(listSentences):
        # get random index
        index = randOrder[i];
        # load current sentence
        sentencePath = [hintDir +'0' + str(testLists[j]) + '\-0dB\Ger_male00' + str(index) + '.wav'];
    
        print(["Current playback level: " + str(currentSNR)]);
        print(["Round " + str(i) + " out of " + str(listSentences)]);
        # audio files are labeled from Ger_male001 and not Ger_male000 so add '1'
        curr_sent = loadSentenceAudio(testLists[j], index + 1, currentSNR, hintDir);
    
        sentLen = len(curr_sent);
        #[noiseSegment, noiseIndex] = circularNoise(noise, sentLen, noiseIndex);

        if practiceCondition == "noiseLeft":
            sd.play(audioBuffer, blocking = 'true', mapping = [ChFront, ChLeft]);
        elif practiceCondition == "noiseRight":
            sd.play(audioBuffer, blocking = 'true', mapping = [ChFront, ChRight]);
        elif practiceCondition == "noiseFront":
            sd.play(curr_sent + noise[0:len(curr_sent)], blocking = 'true', mapping = [ChFront]);
        else:
            sd.play(audioBuffer[0], blocking = 'true', mapping = [ChFront]);
            

        # get length of current sentence
        sentenceLength = len(sentences[index].split());

        # print out current sentence string
        print("Sentence length: " + str(sentenceLength))
        print(sentences[index]);    

        # get experimenter feedback
        print("How many words have been correct?");
        correctWords = input();
    
        # alternative: just ask if below or above 50% hit
        # less data but quicker
        while correctWords > sentenceLength:
            print("Invalid input. Try again!");
            print("How many words have been correct?");
            correctWords = input();
        
        print(['Sentence len: ' + str(sentenceLength) + ' correct: ' + str(correctWords)]);
        hitQuote = correctWords / sentenceLength;
        print("HitQuote: " + str(hitQuote));
        
        # adapt SNR based on hitQuote
        if i < 4:
            if hitQuote < 0.5:
                currentSNR = currentSNR + 4;
            else:
                currentSNR = currentSNR - 4;
        else:
            
            # store sentence data
            hitQuotes[i] = hitQuote;
            listSNR[i] = currentSNR;
            
            # adapt SNR based on hitQuote
            if hitQuote < 0.5:
                currentSNR = currentSNR + 2;
            else:
                currentSNR = currentSNR - 2;

    
        # SNR sanity check
        if currentSNR < minSNR:
            currentSNR = minSNR;
            print(["Warning: reached min SNR!" + str(minSNR)]);
        elif currentSNR > maxSNR:
            currentSNR = maxSNR;
            print(["Warning: reached max SNR!" + str(maxSNR)]);
        
    

    print(["List" + str(j) + " out of" + str(numTestLists) + " done!"]);

    # store data in resultStorage
    resultStorage[j]["ListIndex"] = testLists[j];
    resultStorage[j]["Condition"] = testConditions[j];
    resultStorage[j]["ListSNRs"] = listSNR;
    resultStorage[j]["ListHitQuotes"] = hitQuotes;

   
#%% Write results into file
# parse dict into json
results = json.dumps(resultStorage, indent = 4, cls=NumpyEncoder);
# store json into file
with open(resultFileName, "w") as outfile:
    outfile.write(results)



