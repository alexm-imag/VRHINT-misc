# -*- coding: utf-8 -*-
"""
Created on Fri May 20 13:50:50 2022

@author: Alexander Müller
"""
import numpy as np;
import soundfile as sf;
import csv;
import datetime as dt;
import hintUtilities as util

## statics
sentencesPerList = 20;
minSNR = -30;
maxSNR = 2;
# contents of -6 dB folder match RMS of noiseGR_-27dB
# therefore 6 dB is the offset for our SNR
snrOffset = -6;

class hintTest:
    
    # put stuff here that only has to be set once
    def __init__(self, hintDir, userName, numLists = 5, rounds = 20, calibrationRounds = 4, practiceList = 12, numPracticeSentences = 5):
        
        self.hintDir = hintDir;
        self.userName = userName;
        
        if numLists > 10:
            print("Error: Invalid list number! Using default instead!");
            numLists = 5;
        
        if rounds > sentencesPerList:
            print("Error: Invalid Sentence number! Using default instead!");
            rounds = 20;
            
        if numPracticeSentences > sentencesPerList:
            print("Error: Invalid practiceSentence number! Using default instead!");
            numPracticeSentences = 5;
        
        if practiceList < 11:
            print("Error: Invalid practiceList! Using default instead!");
            practiceList = 12;
            
        if calibrationRounds > rounds:
            print("Error: Invalid rounds / calibration rounds pair! Using default instead!");
            rounds = 20;
            calibrationRounds = 4;
            
        
        print("Test Setup: " + str(numLists) + " lists, " + str(rounds) + " rounds, " + str(calibrationRounds) + " (calib)");
        
        self.sentenceCount = rounds;
        self.practiceList = practiceList;
        self.numPracticeSentences = numPracticeSentences;
        self.calibrationRounds = calibrationRounds;
        # make this into a parameter
        self.practiceCondition = "noiseLeft";
        
        self.chLeft = 1;
        self.chFront = 2;
        self.chRight = 5;
        
        self.snrCalibStepSize = 4;
        self.snrStepSize = 2;
        
        self.numTestLists = numLists;
        self.userIndex = util.getUserIndex();
        
        [self.testLists, self.testConditions] = self.createTestSetup(self.userIndex, numLists);
        self.resultStorage = self.createResultStorage(numLists, self.userIndex, self.sentenceCount, self.calibrationRounds);
        
        self.noise, self.fs = sf.read(self.hintDir + "noiseGR_male_-27dB.wav");    
        
        self.listIndex = 0;     #self.testLists[0];
        self.sentenceIndex = 0;
        
        self.listSentenceOrder = np.zeros(self.sentenceCount);
        #self.listSentenceOrder = np.random.permutation(range(self.sentenceCount));
        self.listSentenceStrings = util.loadListSentences(self.testLists[self.listIndex], self.hintDir);
        
        self.currSNR = 0;
        self.offsetSNR = self.currSNR + snrOffset;
        self.currCondition = "emptyCondition";
        self.currList = 0;
        self.currSentenceString = "empty";
        
        #self.listSetup();
        
    def audioSettings(self, chLeft, chFront, chRight):
        self.chLeft = chLeft;
        self.chFront = chFront;
        self.chRight = chRight
        
    def createTestSetup(self, userIndex, numTestLists):
        
        with open('lqConditions.csv', mode ='r')as file:
          lqConditions = list(csv.reader(file));
                
        with open('lqLists.csv', mode ='r')as file:
          lqLists = list(csv.reader(file));
        
        # convert List<List<str>> to List<List<int>>
        for i in range(len(lqLists)):
            lqLists[i] = [int(j) for j in lqLists[i]];

        
        # this will be determined by number of result files!
        testLists = [lqLists[userIndex % len(lqLists)][k] for k in range(numTestLists)];
        
        # pre-allocate text array
        testConditions = ["emptyCondition" for k in range(numTestLists)]; 
        
        # userIndex determines start line of lqConditions matrix
        lqCondDim = len(lqConditions[0]);
        
        for i in range((int)(numTestLists / lqCondDim) + 1):
            testConditions[(i * lqCondDim):min(numTestLists, (i *lqCondDim))] = lqConditions[(userIndex + i) % len(lqConditions)];
        
        return testLists, testConditions;
        
    def createResultStorage(self, numTestLists, userIndex, numListSentences, calibRounds):
        # first 4 rounds of each round are not considered in results
        templateData = np.zeros(numListSentences - calibRounds);
        templateCondition = "noiseLeft";
        templateListIndex = 12;
        
        resultTemplate = {
            "ListIndex": templateListIndex,
            "Time": dt.datetime.now().strftime("%d-%m-%y--%H-%M-%S"),
            "Condition": templateCondition,
            "ListSNRs": templateData,
            "ListHitQuotes": templateData,
            "ListSNRAverage": 0
            };
        
        # allocate numTestLists structs to store results
        subResults = [resultTemplate.copy() for k in range(numTestLists)];
        
        resultStorage = {
            "testSetup": "loudspeaker",
            "userIndex": userIndex,
            "subResults": subResults
            };
        
        return resultStorage;
        
        
    def listSetup(self):
        print("Starting List " + str(self.listIndex) + " with condition: " + self.testConditions[self.listIndex]);
        
        self.listSentenceOrder = np.random.permutation(range(sentencesPerList))[0:self.sentenceCount];
        
        self.listSentenceStrings = util.loadListSentences(self.testLists[self.listIndex], self.hintDir);
        
        self.listSNR = np.zeros(self.sentenceCount  - self.calibrationRounds);
        self.listHitQuotes = np.zeros(self.sentenceCount - self.calibrationRounds);
        
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
    
    def getCurrentListIndex(self):
        return self.currList;
    
    def getCurrentSNR(self):
        return self.currSNR;
    
    def getCurrentCondition(self):
        return self.currCondition;
    
    def getPracticeRounds(self):
        return self.numPracticeSentences;
    
    def getNumTestLists(self):
        return self.numTestLists;
    
    def getCurrentListCount(self):
        return self.listIndex;
    
    def getUserIndex(self):
        return self.userIndex;

    def practiceSetup(self):
         print("Practice setup: List: " + str(self.practiceList) + " Condition: " + str(self.practiceCondition));
         self.currSNR = 0;
         self.sentenceIndex = 0;
         self.listSentenceOrder = np.zeros(self.numPracticeSentences);
         self.listSentenceOrder = np.random.permutation(range(sentencesPerList))[0:self.numPracticeSentences];  
         self.listSentenceStrings = util.loadListSentences(self.practiceList, self.hintDir);
         self.currSentenceString = self.listSentenceStrings[self.listSentenceOrder[0]];
         self.currSentenceLength = len(self.currSentenceString.split());
         self.currCondition = self.practiceCondition;
         self.currList = self.practiceList;
               
         
    def playPracticeSentence(self):
         # get random index        
        index = self.listSentenceOrder[self.sentenceIndex];
        
        print("Practice: Current SNR: " + str(self.currSNR));
        print("Practice: Round " + str(self.sentenceIndex + 1) + " out of " + str(self.numPracticeSentences));
        # audio files are labeled from Ger_male001 and not Ger_male000 so add '1'
        currSentenceAudio = util.loadSentenceAudio(self.practiceList, index + 1, self.offsetSNR, self.hintDir);
            
        util.playAudio(currSentenceAudio, self.noise, self.practiceCondition, self.chFront, self.chLeft, self.chRight);
        
    
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
            return 1;
        else:
            index = self.listSentenceOrder[self.sentenceIndex];
            self.currSentenceString = self.listSentenceStrings[index];
            self.currSentenceLength = len(self.currSentenceString.split());
            
        return 0;
             
    def testSetup(self):
        self.currSNR = 0;
        self.sentenceIndex = 0;
        self.listSentenceOrder = np.zeros(self.sentenceCount);
        self.listSentenceOrder = np.random.permutation(range(sentencesPerList))[0:self.sentenceCount];  
        self.listSentenceStrings = util.loadListSentences(self.practiceList, self.hintDir);
        self.currSentenceString = self.listSentenceStrings[self.listSentenceOrder[0]];
        self.currSentenceLength = len(self.currSentenceString.split());
        self.listSetup();
        

    def playCurrentSentence(self):
               
        # a new list has been loaded
        if self.sentenceIndex >= self.sentenceCount:
            print("Sentence range exceeded!");

        # get random index        
        index = self.listSentenceOrder[self.sentenceIndex];
        
        print("Current playback level: " + str(self.currSNR));
        print("Round " + str(self.sentenceIndex + 1) + " out of " + str(self.sentenceCount));
        # audio files are labeled from Ger_male001 and not Ger_male000 so add '1'
        currSentenceAudio = util.loadSentenceAudio(self.currList, index + 1, self.offsetSNR, self.hintDir);
            
        util.playAudio(currSentenceAudio, self.noise, self.currCondition, self.chFront, self.chLeft, self.chRight);       
    
   
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
                util.exportResults(self.resultStorage, self.userIndex, self.userName)
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
                self.currSNR = self.currSNR + self.snrStepSize;
            else:
                self.currSNR = self.currSNR - self.snrStepSize;
            
        
        self.offsetSNR = self.currSNR + snrOffset;

        # SNR sanity check
        if self.offsetSNR < minSNR:
            self.offsetSNR = minSNR;
            print("Warning: reached min SNR!" + str(minSNR));
        elif self.offsetSNR > maxSNR:
            self.offsetSNR = maxSNR;
            print("Warning: reached max SNR!" + str(maxSNR));
            
        self.currSNR = self.offsetSNR - snrOffset;
        print("Offset SNR: " + str(self.offsetSNR) + " currSNR: " + (str(self.currSNR)));
 
    def storeResults(self):
        print(["Storing resutls for list " + str(self.listIndex + 1) + " out of " + str(self.numTestLists)]);
        print("List index: " + str(self.listIndex));
        
        
        self.resultStorage['subResults'][self.listIndex]["Time"] = dt.datetime.now().strftime("%d-%m-%y--%H-%M-%S");
        self.resultStorage['subResults'][self.listIndex]["ListIndex"] = self.testLists[self.listIndex];
        self.resultStorage['subResults'][self.listIndex]["Condition"] = self.testConditions[self.listIndex];
        self.resultStorage['subResults'][self.listIndex]["ListSNRs"] = self.listSNR;
        self.resultStorage['subResults'][self.listIndex]["ListHitQuotes"] = self.listHitQuotes;
        # calculate average SNR of current list
        self.resultStorage['subResults'][self.listIndex]["ListSNRAverage"] = sum(self.listSNR) / len(self.listSNR);
        
        print(self.resultStorage)
            
