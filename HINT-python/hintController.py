# -*- coding: utf-8 -*-
"""
Created on Thu May  5 13:52:26 2022

@author: Alexander Mueller
"""

import numpy as np;
import json;
import soundfile as sf;
import sounddevice as sd;

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


def combineAudioFiles(audioStruct, buflen):
    
    #chnNums = max([audioStruct["Channel"]]);
    chnNums = 0;
    for i in range (len(audioStruct)):
        if audioStruct[i]["Channel"] > chnNums:
            chnNums = audioStruct[i]["Channel"];
            
            
    print("Channels: " + chnNums);
    
    #testAud = np.array([curr_sent, noise[0:len(curr_sent)]]).transpose();
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
        
    
    return buffer;

    
    
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
#audioStructTemplate = {"AudioData": 1,
#                       "Channel": 1};

# this format works for sentence indices, SNR values and hit Quotes
templateData = np.zeros(listSentences);
templateCondition = "noiseLeft";
templateListIndex = 12;

resultTemplate = {
    "ListIndex": templateListIndex,
    "Condition": templateCondition,
    "SNRs": templateData,
    "HitQuotes:": templateData};

print(resultTemplate);

# allocate numTestLists structs to store results
resultStorage = [resultTemplate for k in range(numTestLists)];

json_obj = json.dumps(resultStorage, indent = 4, cls=NumpyEncoder);

# Writing to sample.json
with open("sample2.json", "w") as outfile:
    outfile.write(json_obj)


#%% user login
print("Enter participants name:");
name = input();

#%% pre-allocate struct array for results

# add system to check if username has already been used!
# create file name based on user name
#jsonFileName = sprintf("results-%s-%s.json", name, datestr(now, 'dd-mm-yyyy-hh:MM'));
jsonFileName = "results-%s.json" % (name);

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

# get sentence list order (5 lists total)
testLists = np.random.permutation(range(10));

# pre-allocate text array
testConditions = ["emptyCondition" for k in range(numTestLists)]; 

# assign random order of test conditions
# REPLACE THIS WITH LATIN SQUARES!
for i in range(numTestLists):
    #randNum = randi(4,1);
    randNum = np.random.randint(1, 5);
    if(randNum == 1):
        testConditions[i] = "quiet";
    elif(randNum == 2):
        testConditions[i] = "noiseFront";
    elif(randNum == 3):
        testConditions[i] = "noiseLeft";
    else:
        testConditions[i] = "noiseRight";



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
#audioStruct = [audioStructTemplate for k in range(2)]; 

for i in range(practiceRounds):
    # get random index
    index = randOrder[i];
    # load current sentence
    sentencePath = [hintDir + '0' + str(practiceList) + '\-0dB\Ger_male00' + str(index) + '.wav'];

    print(["Current playback level: " + str(currentSNR)]);
    print(["Round " + str(i) + " out of " + str(practiceRounds)]);
    curr_sent = loadSentenceAudio(practiceList, index, currentSNR, importDir);
        
    #noiseSegment = noise[0:len(curr_sent)];
    #[noiseSegment, noiseIndex] = circularNoise(noise, sentLen, noiseIndex);

        
   # audioStruct = [
    #            {
     #              "AudioData": curr_sent,
      #             "Channel": ChFront
       #          },
       #         {
       #           "AudioData": noise[0:len(curr_sent)],
       #           "Channel": "noiseLeft"
       #         }
       #         ];
    
    audioBuffer = np.array([curr_sent, noise[0:len(curr_sent)]]).transpose();
    
    sentLen = len(curr_sent);

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
    print([sentences[index] + str(sentenceLength)]);


    # get experimenter feedback
    print("How many words have been correct?");
    correctWords = int(input());
    print(type(correctWords));

    # alternative: just ask if below or above 50% hit
    # less data but quicker
    while correctWords > sentenceLength:
        print("Invalid input. Try again!");
        print("How many words have been correct?");
        correctWords = input();
    
    print(['Sentence len: ' + str(sentenceLength) + ' correct: ' + str(correctWords)]);
    hitQuote = correctWords / sentenceLength;
    print(hitQuote);

    # store sentence data
    hitQuotes[i] = hitQuote;
    listSNR[i] = currentSNR;

    # adapt SNR based on hitQuote
    if i < 4 :        
        if hitQuote < 0.5:
            currentSNR = currentSNR + 4;
        else:
            currentSNR = currentSNR - 4;
    else:
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
# create file name based on user name
jsonFile = "practice-%s.json" % (name);
# fill struct with list data
pracRes = resultTemplate;
pracRes["ListIndex"] = practiceList;
pracRes["Condition"] = practiceCondition;
pracRes["SNRs"] = listSNR;
pracRes["HitQuotes"] = hitQuotes;

# parse struct into json
practiceResults = json.dumps(pracRes, indent = 4, cls=NumpyEncoder);
# store json into file
with open(jsonFile, "w") as outfile:
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

    if testConditions[j] == "noiseLeft":
        audioStruct[1]["Channel"] = ChLeft;
    elif testConditions[j] == "noiseRight":
        audioStruct[1]["Channel"] = ChRight;   
    elif testConditions[j] == "noiseFront":
        audioStruct[1]["Channel"] = ChFront;


    print(["Starting List " + str(testLists[j]) + " with condition" + testConditions[j]]);

    for i in range(listSentences):
        # get random index
        index = randOrder[i];
        # load current sentence
        sentencePath = [hintDir +'0' + str(testLists[j]) + '\-0dB\Ger_male00' + str(index) + '.wav'];
    
        print(["Current playback level: " + str(currentSNR)]);
        print(["Round " + str(i) + " out of " + str(listSentences)]);
        curr_sent = loadSentenceAudio(testLists[j], index, currentSNR, hintDir);
    
        sentLen = len(curr_sent);
        #[noiseSegment, noiseIndex] = circularNoise(noise, sentLen, noiseIndex);
    
        audioStruct[0]["AudioData"] = curr_sent;
        audioStruct[0]["Channel"] = ChFront;

        if testConditions[j] != "quiet":
            audioStruct[1]["AudioData"] = noiseSegment;
        else:
            audioStruct[1]["AudioData"] = 0;
        

        buffer = combineAudioFiles(audioStruct, sentLen);
        # play current sentence
        #playbackID = playrec('play', curr_sent, ChMap);
    

        # get length of current sentence
        sentenceLength = len(sentences[index].split());

        # print out current sentence string
        print([sentences(index) + sentenceLength]);      
        
        # only prompt this after playback is done
        #while ~playrec('isFinished', playbackID) end

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
        print(hitQuote);
    
        # store sentence data
        hitQuotes[i] = hitQuote;
        listSNR[i] = currentSNR;
    
        # adapt SNR based on hitQuote
        if i < 4:
            if hitQuote < 0.5:
                currentSNR = currentSNR + 4;
            else:
                currentSNR = currentSNR - 4;
        else:
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
with open(jsonFileName, "w") as outfile:
    outfile.write(results)



