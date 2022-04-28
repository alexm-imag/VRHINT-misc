# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 11:07:55 2022

@author: Alexander Müller
"""


from pydub import AudioSegment
import os

def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

# %% parameters
base_type = 'wav';

importPath = 'D:\MA\german-hint-48kHz';
exportPath = r'D:\MA\HINT';

importDir = 'german-hint-48kHz\\';
exportDir = 'HINT\\';

stepSize = 2
lowerBound = -16
upperBound = +4

listSize = 20
# %% setup
dir = os.listdir(importPath);

subPaths = []

if not os.path.exists(exportPath):
    os.makedirs(exportPath);

c = 0;

if listSize > 0:
    for l in range(int(len(dir) / listSize)):    
        if l+1 < 10:
            listPath = exportPath + '\\' + '0' + str(l+1); 
        else:
            listPath = exportPath + '\\' + str(l+1);
        
        if not os.path.exists(listPath):
            os.makedirs(listPath);
            
        
        for i in range(lowerBound, upperBound, stepSize):
            if i > 0:
                subPaths.append(listPath + "\\+" + str(i) + "dB");    
            else:
                subPaths.append(listPath + "\\-" + str(abs(i)) + "dB");
        
            if not os.path.exists(subPaths[c]):
                os.makedirs(subPaths[c]);
                
            c = c + 1;
        
else:
    for i in range(lowerBound, upperBound, stepSize):
        if i > 0:
            subPaths.append(exportPath + "\\+" + str(i) + "dB");    
        else:
            subPaths.append(exportPath + "\\-" + str(abs(i)) + "dB");
            
        if not os.path.exists(subPaths[c]):
            os.makedirs(subPaths[c]);
            
        c = c + 1;
    
# %% processing and export

c = 0;
lst = 1;

for j in range(len(dir)):
    print("Processing file " + str(j) + " of " + str(len(dir)));
    sound = AudioSegment.from_file(importDir + dir[j], base_type)
    
    k = 0
    
    for i in range(lowerBound, upperBound, stepSize):
        dSound = sound.apply_gain(i);
        
        outPath = subPaths[k + c] + '\\' + dir[j];
        k = k + 1

        if dSound.max >= dSound.max_possible_amplitude:
            print("Warning: Possible clip at " + str(i) + " dB!");
            print("Max amp: " + str(dSound.max));
        
        dSound.export(outPath, base_type);
        
    
    if (j+1) % 20 == 0:
        if (j+1) >= 20:
            c = c + 10
            lst = lst + 1;
            print("Next list " + str(lst) +  " at file " + str(j));

print("All done!");    
    


# %% Testing and debugging
#sound = AudioSegment.from_file('HINT_Ger_male_single_sentences\\' + dir[0], base_type)
sound = AudioSegment.from_file('german-hint-48kHz\Ger_male001.wav', base_type)
print(sound.max_dBFS)
print(sound.dBFS)
print(sound.max)
gain = sound.max_dBFS - sound.dBFS
print(gain)
maxSound = match_target_amplitude(sound, sound.max_dBFS)
print(maxSound.dBFS)
max_sound2 =  sound.apply_gain(4)
print(max_sound2.dBFS);
print(max_sound2.max_possible_amplitude);
print(max_sound2.max);
#max_sound2.export("testfile2.wav", base_type)


# %%
test = []

for i in range(10):
    test.append(i)
    print(test[i])
    