# -*- coding: utf-8 -*-
"""
Created on Fri May 20 13:50:50 2022

@author: cocot
"""
import numpy as np;
import json;
import soundfile as sf;
import sounddevice as sd;
import csv;
import datetime as dt;
import os;
import hintUtilities as util


#%% Global / static
# variables that are always constant / not to be changed via GUI

# number of sentences in each list
listSentences = 20;
# lists open for test (1...10)
availableTestLists = 10;
# lists open for practice (11,12)
availablePracticeLists = 2;

# min/max available SNR
minSNR = -16;
maxSNR = 2;

# maybe add these to setup
ChLeft = 1;
ChFront = 3;
ChRight = 5;


#%% Setup variables
hintDir = 'german-hint-adaptive-48kHz\\';





def createResultStorage(numTestLists):
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
    return resultStorage;

def getUserIndex():
    return len(os.listdir('results'));    
    

def createTestSetup(userIndex, numTestLists):
    
    with open('lqConditions.csv', mode ='r')as file:
      lqConditions = list(csv.reader(file));
            
    with open('lqLists.csv', mode ='r')as file:
      lqLists = list(csv.reader(file));
    
    # convert List<List<str>> to List<List<int>>
    for i in range(len(lqLists)):
        lqLists[i] = [int(j) for j in lqLists[i]];

    
    # this will be determined by number of result files!
    testLists = lqLists[userIndex % availableTestLists];
    
    # pre-allocate text array
    testConditions = ["emptyCondition" for k in range(numTestLists)]; 
    
    # userIndex determines start line of lqConditions matrix
    # 5th condition is taken from the next line (considering wrapping!)
    testConditions[0:4] = lqConditions[userIndex % len(lqConditions)];
    testConditions[4] = lqConditions[(userIndex + 1) % len(lqConditions)][0];
    
    return testLists, testConditions;


# Params:
# testLists: array, determining numTestLists and order
# testConditions: array, has to match length of testLists!
# storeResults: bool, create and fill result storage
# userName: string, required for JSON export
def hintProcedure(testLists, testConditions, storeResults):
    
    if storeResults == True:
        resultStorage = createResultStorage();
        
    
    noise, fs = sf.read(hintDir + "noiseGR_male.wav");
        
    
    for j in range(testLists.count):
        sentences = util.loadListSentences(testLists[j], hintDir);
        randOrder = np.random.permutation(range(20));
        
        # store SNR for each sentence
        listSNR = np.zeros(20);
        # store hitQuote for each sentence
        hitQuotes = np.zeros(20);
        
        # starting at 0 dB
        currentSNR = 0;
    
    
        print(["Starting List " + str(testLists[j]) + " with condition" + testConditions[j]]);
    
        for i in range(listSentences):
            # get random index
            index = randOrder[i];
        
            print(["Current playback level: " + str(currentSNR)]);
            print(["Round " + str(i) + " out of " + str(listSentences)]);
            # audio files are labeled from Ger_male001 and not Ger_male000 so add '1'
            curr_sent = util.loadSentenceAudio(testLists[j], index + 1, currentSNR, hintDir);
            
            audioBuffer = np.array([curr_sent, noise[0:len(curr_sent)]]).transpose();
    
            if testConditions[j]== "noiseLeft":
                sd.play(audioBuffer, blocking = 'true', mapping = [ChFront, ChLeft]);
            elif testConditions[j] == "noiseRight":
                sd.play(audioBuffer, blocking = 'true', mapping = [ChFront, ChRight]);
            elif testConditions[j] == "noiseFront":
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
            
        
    
        print(["List" + str(j) + " out of" + str(testLists.count) + " done!"]);
    
        if storeResults == True:
            # store data in resultStorage
            resultStorage[j]["ListIndex"] = testLists[j];
            resultStorage[j]["Condition"] = testConditions[j];
            resultStorage[j]["ListSNRs"] = listSNR;
            resultStorage[j]["ListHitQuotes"] = hitQuotes;
            
            
    print("Test procedure done!");
    return resultStorage;