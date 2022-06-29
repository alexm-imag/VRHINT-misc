# -*- coding: utf-8 -*-
"""
Created on Fri May 20 13:50:50 2022

@author: cocot
"""
import numpy as np;
#import json;
import soundfile as sf;
#import sounddevice as sd;
import csv;
import datetime as dt;
import hintUtilities as util

#%% Global / static
# variables that are always constant / not to be changed via GUI

# number of sentences in each list
listSentences = 20;
# lists open for test (1...10)
availableTestLists = 10;
# lists open for practice (11,12)
availablePracticeLists = 2;

# maybe add these to setup
ChLeft = 1;
ChFront = 2;
ChRight = 2;


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


def createTestSetup(userIndex, numTestLists):
    
    with open('lqConditions.csv', mode ='r')as file:
      lqConditions = list(csv.reader(file));
            
    with open('lqLists.csv', mode ='r')as file:
      lqLists = list(csv.reader(file));
    
    # convert List<List<str>> to List<List<int>>
    for i in range(len(lqLists)):
        lqLists[i] = [int(j) for j in lqLists[i]];

    
    # this will be determined by number of result files!
    testLists = [lqLists[userIndex % availableTestLists][k] for k in range(numTestLists)];
    
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
def hintProcedure(testLists, testConditions, storeResults, sentenceCbk, snrCbk):
    
    if storeResults == True:
        resultStorage = createResultStorage(len(testLists));
        
    minSNR = -16;
    maxSNR = 2;
    
    noise, fs = sf.read(hintDir + "noiseGR_male.wav");        
    
    for j in range(len(testLists)):
        sentences = util.loadListSentences(testLists[j], hintDir);
        randOrder = np.random.permutation(range(20));
        
        # store SNR for each sentence
        listSNR = np.zeros(20);
        # store hitQuote for each sentence
        hitQuotes = np.zeros(20);
        
        # starting at 0 dB
        currentSNR = 0;
    
    
        print("Starting List " + str(testLists[j]) + " with condition: " + testConditions[j]);
    
        print("List sentences: " + str(listSentences));
    
        for i in range(listSentences):
            # get random index
            index = randOrder[i];
            print("Play sentence " + str(index));
            
            sentenceCbk(sentences[index]);
        
            print(["Current playback level: " + str(currentSNR)]);
            print(["Round " + str(i) + " out of " + str(listSentences)]);
            # audio files are labeled from Ger_male001 and not Ger_male000 so add '1'
            curr_sent = util.loadSentenceAudio(testLists[j], index + 1, currentSNR, hintDir);
            
            util.playAudio(curr_sent, noise, testConditions[j], ChFront, ChLeft, ChRight);
                
    
            # get length of current sentence
            sentenceLength = len(sentences[index].split());
    
            # print out current sentence string
            print("Sentence length: " + str(sentenceLength))
            print(sentences[index]);    
    
            # get experimenter feedback
            print("How many words have been correct?");
            #correctWords = input();
            correctWords = 3;
        
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
            
            snrCbk(currentSNR);
        
    
        print(["List" + str(j) + " out of" + str(testLists.count) + " done!"]);
    
        if storeResults == True:
            # store data in resultStorage
            resultStorage[j]["ListIndex"] = testLists[j];
            resultStorage[j]["Condition"] = testConditions[j];
            resultStorage[j]["ListSNRs"] = listSNR;
            resultStorage[j]["ListHitQuotes"] = hitQuotes;
            
            
    print("Test procedure done!");
    return resultStorage;


class hintTest:
    
    # put stuff here that only has to be set once
    def __init__(self, testDir, numLists, userIndex, practiceSentences):
        
        self.hintDir = testDir;
        # statics
        self.sentenceCount = 20;
        
        self.practiceList = 12;
        self.numPracticeSentences = practiceSentences;
        self.practiceCondition = "noiseLeft";
        
        self.numTestLists = numLists;
        
        [self.testLists, self.testConditions] = createTestSetup(userIndex, numLists);
        self.resultsStorage = createResultStorage(numLists);
        
        self.noise, self.fs = sf.read(hintDir + "noiseGR_male.wav");    
        
        self.listIndex = self.testLists[0];
        self.sentenceIndex = 0;
        
        self.listSentenceOrder = np.random.permutation(range(self.sentenceCount));
        self.listSentenceStrings = util.loadListSentences(self.testLists[self.listIndex], self.hintDir);
        
        self.minSNR = -16;
        self.maxSNR = 2;
        self.currSNR = 0;
        self.currCondition = "emptyCondition";
        self.currList = 0;
        self.currSentenceString = "empty";
        
        self.listSetup();
        
    def audioSettings(self, chLeft, chFront, chRight):
        self.chLeft = chLeft;
        self.chFront = chFront;
        self.chRight = chRight
        
    def createTestSetup(userIndex, numTestLists):
        
        with open('lqConditions.csv', mode ='r')as file:
          lqConditions = list(csv.reader(file));
                
        with open('lqLists.csv', mode ='r')as file:
          lqLists = list(csv.reader(file));
        
        # convert List<List<str>> to List<List<int>>
        for i in range(len(lqLists)):
            lqLists[i] = [int(j) for j in lqLists[i]];

        
        # this will be determined by number of result files!
        testLists = [lqLists[userIndex % availableTestLists][k] for k in range(numTestLists)];
        
        # pre-allocate text array
        testConditions = ["emptyCondition" for k in range(numTestLists)]; 
        
        # userIndex determines start line of lqConditions matrix
        lqCondDim = len(lqConditions[0]);
        
        for i in range(numTestLists / lqCondDim):
            testConditions[(i * lqCondDim):min(numTestLists, (i *lqCondDim))] = lqConditions[(userIndex + i) % len(lqConditions)];
        
        return testLists, testConditions;
        
    def createResultStorage(numTestLists, numListSentences, calibRounds):
        # first 4 rounds of each round are not considered in results
        templateData = np.zeros(numListSentences - calibRounds);
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
        
        
    def listSetup(self):
        print(["Starting List " + str(self.listIndex) + " with condition: " + self.testConditions[self.listIndex]]);
        
        self.listSentenceOrder = np.random.permutation(range(self.sentenceCount));
        
        self.listSentenceStrings = util.loadListSentences(self.testLists[self.listIndex], self.hintDir);
        
        self.listSNR = np.zeros(20);
        self.listHitQuotes = np.zeros(20);
        
        self.currSNR = 0;
        self.currCondition = self.testConditions[self.listIndex];
        self.currList = self.testLists[self.listIndex];
        
        self.currSentenceString = self.listSentenceStrings[self.listSentenceOrder[0]];
        self.currSentenceLength = len(self.currSentenceString.split());
        
        self.sentenceIndex = 0;
        
    
    def getCurrentSentenceString(self):
        return self.currSentenceString;
    
    def getCurrentSentenceLen(self):
        return self.currSentenceLength;
    
    def getSentenceIndex(self):
        return self.sentenceIndex;
    
    def getSentenceCount(self):
        return self.sentenceCount;
    
    def getCurrentSNR(self):
        return self.currSNR;
    
    def getCurrentCondition(self):
        return self.currCondition;
    
    def getPracticeRounds(self):
        return self.numPracticeSentences;
    

    def practiceSetup(self):
         self.currSNR = 0;
         self.listSentenceOrder = np.random.permutation(range(self.sentenceCount));  
         self.listSentenceStrings = util.loadListSentences(self.practiceList, self.hintDir);
         self.currSentenceString = self.listSentenceStrings[self.listSentenceOrder[0]];
         self.currSentenceLength = len(self.currSentenceString.split());
         
        
    def playPracticeSentence(self):
         # get random index        
        index = self.listSentenceOrder[self.sentenceIndex];
        print("Prac index: " + str(index));
        
        print("Practice: Current playback level: " + str(self.currSNR));
        print("Practice: Round " + str(self.sentenceIndex + 1) + " out of " + str(self.numPracticeSentences));
        # audio files are labeled from Ger_male001 and not Ger_male000 so add '1'
        currSentenceAudio = util.loadSentenceAudio(self.practiceList, index + 1, self.currSNR, self.hintDir);
            
        util.playAudio(currSentenceAudio, self.noise, self.practiceCondition, ChFront, ChLeft, ChRight);
        
    
    def enterPracticeFeedback(self, correctWords):
        
        if correctWords > self.currSentenceLength:
            print("Invalid input. Try again!");
            return;
    
        print('Sentence len: ' + str(self.currSentenceLength) + ' correct: ' + str(correctWords));
        hitQuote = correctWords / self.currSentenceLength;
        print("HitQuote: " + str(hitQuote));

        # adapt SNR based on hitQuote
        self.adaptSNR(hitQuote, True);
            
        self.sentenceIndex = self.sentenceIndex + 1;
        
        if self.sentenceIndex + 1 >= self.numPracticeSentences:
            print("Practice finished!");
            #self.listSetup();
        else:
            index = self.listSentenceOrder[self.sentenceIndex];
            self.currSentenceString = self.listSentenceStrings[index];
            self.currSentenceLength = len(self.currSentenceString.split());
             


    def playCurrentSentence(self):
               
        # a new list has been loaded
        if self.sentenceIndex >= self.sentenceCount:
            print("Sentence range exceeded!");

        # get random index        
        index = self.listSentenceOrder[self.sentenceIndex];
        
        print("Current playback level: " + str(self.currSNR));
        print("Round " + str(self.sentenceIndex + 1) + " out of " + str(self.sentenceCount));
        # audio files are labeled from Ger_male001 and not Ger_male000 so add '1'
        currSentenceAudio = util.loadSentenceAudio(self.currList, index + 1, self.currSNR, self.hintDir);
            
        util.playAudio(currSentenceAudio, self.noise, self.currCondition, ChFront, ChLeft, ChRight);       
    
   
    def enterFeedback(self, correctWords):    

        # alternative: just ask if below or above 50% hit
        # less data but quicker
        if correctWords > self.currSentenceLength:
            print("Invalid input. Try again!");
            return;

        
        print('Sentence len: ' + str(self.currSentenceLength) + ' correct: ' + str(correctWords));
        hitQuote = correctWords / self.currSentenceLength;
        print("HitQuote: " + str(hitQuote));
        
        # adapt SNR based on hitQuote
        self.adaptSNR(hitQuote, False);
            
        self.sentenceIndex = self.sentenceIndex + 1;
        
        if self.sentenceIndex >= self.sentenceCount:
            print("List " + str(self.listIndex) + " finished!");
            self.storeResults();
            self.listIndex = self.listIndex + 1;
            
            
            if self.listIndex + 1 > self.numTestLists:
                print("Test done!");
                util.exportResults(self.resultStorage, self.userName)
                return 1;
            
            self.listSetup();
        else:
            index = self.listSentenceOrder[self.sentenceIndex];
            self.currSentenceString = self.listSentenceStrings[index];
            print("Next sentence: " + self.currSentenceString);
            self.currSentenceLength = len(self.currSentenceString.split());
             
        return 0;
    
    
    def adaptSNR(self, hitQuote, practiceMode):
        
        if self.sentenceIndex < self.calibrationRounds:
            if hitQuote < 0.5:
                self.currSNR = self.currSNR + self.snrCalibStepSize;
            else:
                self.currSNR = self.currSNR - self.snrCalibStepSize;
       # other sentences: 2 dB steps         
        else:
            # store sentence data
            if practiceMode == False:
                self.listHitQuotes[self.sentenceIndex - self.calibrationRounds] = hitQuote;
                self.listSNR[self.sentenceIndex - self.calibrationRounds] = self.currSNR;
            
            # adapt SNR based on hitQuote
            if hitQuote < 0.5:
                self.currSNR = self.currSNR+ self.snrStepSize;
            else:
                self.currSNR = self.currSNR - self.snrStepSize;

        # SNR sanity check
        if self.currSNR < self.minSNR:
            self.currSNR = self.minSNR;
            print("Warning: reached min SNR!" + str(self.minSNR));
        elif self.currSNR > self.maxSNR:
            self.currSNR = self.maxSNR;
            print("Warning: reached max SNR!" + str(self.maxSNR));
            
            
        
        self.sentenceIndex = self.sentenceIndex + 1;
        
        if self.sentenceIndex + 1 >= self.sentenceCount:
            print("List " + self.listIndex + " finished!");
            self.listIndex = self.listIndex + 1;
            print("Storing results");
            self.storeResults();
            self.listSetup();
        else:
            index = self.listSentenceOrder[self.sentenceIndex];
            self.currSentenceString = self.listSentenceStrings[index];
            self.currSentenceLength = len(self.currSentenceString.split());
             
            
 
    def storeResults(self):
        print(["Storing resutls for list" + str(self.listIndex) + " out of" + str(self.numTestLists)]);
    
        # store data in resultStorage
        self.resultStorage[self.listIndex]["ListIndex"] = self.testLists[self.listIndex];
        self.resultStorage[self.listIndex]["Condition"] = self.testConditions[self.listIndex];
        self.resultStorage[self.listIndex]["ListSNRs"] = self.listSNR;
        self.resultStorage[self.listIndex]["ListHitQuotes"] = self.hitQuotes;
            
