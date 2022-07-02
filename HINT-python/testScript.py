# -*- coding: utf-8 -*-


import sounddevice as sd
import soundfile as sf
#from tkinter import *
import tkinter as tk;  

importDir = 'G:\VRHINT-misc\HINT-python\german-hint-adaptive-48kHz\\';
data, fs = sf.read(importDir + "01\\-0dB\\Ger_male001.wav");
sd.play(data, fs);
status = sd.wait();


#%%
hintDir = 'german-hint-adaptive-48kHz\\';
  
def Voice_rec():
    fs = 48000
      
    # seconds
    duration = 5
    myrecording = sd.rec(int(duration * fs), 
                         samplerate=fs, channels=2)
    sd.wait()
      
    # Save as FLAC file at correct sampling rate
    return sf.write('my_Audio_file.flac', myrecording, fs)


def audioPlayer():
    noise, fs = sf.read(hintDir + "noiseGR_male.wav");   
    sd.play(noise, blocking = 'true', mapping = [1, 2]);
    
  
  
master = tk.Tk()
  
tk.Label(master, text=" Voice Recoder : ").grid(row=0, sticky=W, rowspan=5)
  
  
#b = tk.Button(master, text="Start", command=Voice_rec)
b = tk.Button(master, text="Start", command=audioPlayer)
b.grid(row=0, column=2, columnspan=2, rowspan=2,
       padx=5, pady=5)
  
tk.mainloop()


#%%
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
#data, fs = sf.read(importDir + "noiseGR_male.wav");
data, fs = sf.read(importDir + "01\\-0dB\\Ger_male001.wav");
sd.play(data, fs);
status = sd.wait();
#noise = AudioSegment.from_file(hintDir + "noiseGR_male.wav", base_type);
#sd.play(noise, 48000);

#%%
class Test:
    
    def __init__(self, testVar):
        self.value = testVar;

    def printValue(self):
        print(self.value);


obj = Test(7)
obj.printValue();


#%%
import hintFunctions as hint

stimuliDir = 'G:\VRHINT-misc\HINT-python\german-hint-adaptive-48kHz\\';
userIndex = 1;


hintObject = hint.hintTest(stimuliDir, 5, userIndex);
hintObject.playCurrentSentence();



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
    