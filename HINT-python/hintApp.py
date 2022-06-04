# -*- coding: utf-8 -*-
"""
Created on Fri May 20 10:25:07 2022

@author: Alexander Mueller
"""



from tkinter import filedialog
import customtkinter as ctk
import os
import hintFunctions as hint
#from functools import partial

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root = ctk.CTk()


stimuliDir = "emptyPath";
userName = "default";
hintObject = '';

# use save.txt for path and stuff
if os.path.isfile('save.txt'):
    with open('save.txt', 'r') as f:
        print("load save file");
        savedData = f.read()
        print(savedData);
        stimuliDir = savedData;
        #splitData = savedData.split(',');
        #print(savedData);
        #stimuliDir = splitData;
#        apps = [x for x in tempApps if x.strip()]
 

def testCallback(num):
    print("Hey I'm a callback!" + num)
      

def addPath():  
    pathname = filedialog.askdirectory();
    print(pathname)
    # add a sanity check to this (check if .wav are within dir)
    
    global stimuliDir;
    stimuliDir = pathname + '\\';
    print(stimuliDir)
    
    
    
def enterName():
    global userName;
    userName = nameField.get();
    print("UserName: " + userName);
    userLabel['text'] = "Name: " + userName;
    
    
def clearUserName():
    nameField.delete(0, 'end');


def initTest():
    global hintObject;    
    
    userIndex = hint.getUserIndex();
    userIndexLabel['text'] = "User Index: " + str(userIndex);
    global stimuliDir;
    if stimuliDir == "emptyPath":
        print("Hint path not set!");
        return;
    
    hintObject = hint.hintTest(stimuliDir, 5, userIndex, 5);

def practice():
    print("Start HINT practice");
    global hintObject;    
    hintObject.practiceSetup();
    hintObject.playPracticeSentence();
    


def startTest():
    print("Start test procedure");
        
    global hintObject;    
    #hintObject = hint.hintTest(stimuliDir, 5, userIndex, 5);
    setSentence(hintObject.getCurrentSentenceString());
    hintObject.playCurrentSentence();
    
    
    
def setSentence(sentence):
    currentSentence['text'] = "Sentence: " + sentence;
    
def setSNR(snr):
    currentSNR['text'] = "SNR: " + str(snr) + " dB";  
  
    
def setFeedbackOptions(sentLen):
    print("sent len is: " + str(sentLen));
    # add buttons (0, 1, 2, 3, ..., sentLen)
    
    
def takeFeedback():
    
    global hintObject;
    
    submission = int(feedbackField.get());
    
    if submission < 0 or submission > hintObject.getCurrentSentenceLen():
        print("Invalid input");
        return;

    
    setSNR(hintObject.enterFeedback(int(submission)));
    setSentence(hintObject.getCurrentSentenceString());
    
    hintObject.playCurrentSentence();
    
def leaveGUI():
    root.destroy();
    #root.quit();
       
#canvas = ctk.CTkCanvas(root, height = 700, width = 700, bg = '#263D42')
#canvas.pack()

frame = ctk.CTkFrame(root, bg = 'white')
frame.place(relwidth = 0.8, relheight = 1.5, relx = 0.1, rely = 0.1)


topLabel = ctk.CTkLabel(frame, text="Enter user name")
topLabel.pack()


nameField = ctk.CTkEntry(frame)
nameField.pack()

# command=partial(enterName, tmp)
nameBtn = ctk.CTkButton(frame, text="Enter participants name", padx = 15, pady = 5, bg = "#263D42", command=enterName)
nameBtn.pack()

clearBtn = ctk.CTkButton(frame, text="Clear field", padx = 15, pady = 5, bg = "#263D42", command=clearUserName)
clearBtn.pack()

pathBtn = ctk.CTkButton(frame, text="Add Path", padx = 15, pady = 5, bg = "#263D42", command=addPath)
pathBtn.pack()

initBtn = ctk.CTkButton(frame, text="Init Test", padx = 15, pady = 5, bg = "#263D42", command=initTest)
initBtn.pack();


practiceBtn = ctk.CTkButton(frame, text="Practice", padx = 15, pady = 5, bg = "#263D42", command=practice)
practiceBtn.pack();

startBtn = ctk.CTkButton(frame, text="Start test", padx = 15, pady = 5, bg = "#263D42", command=startTest)
startBtn.pack();


userLabel = ctk.CTkLabel(frame, text="Name: ")
userLabel.pack()

userIndexLabel = ctk.CTkLabel(frame, text="Index: ")
userIndexLabel.pack()

currentSentence = ctk.CTkLabel(frame, text="Sentence: ")
currentSentence.pack()

currentSNR = ctk.CTkLabel(frame, text="SNR: ")
currentSNR.pack()

feedbackField = ctk.CTkEntry(frame)
feedbackField.pack()

submitBtn = ctk.CTkButton(frame, text="Enter", padx = 15, pady = 5, bg = "#263D42", command=takeFeedback)
submitBtn.pack()

quitBtn = ctk.CTkButton(frame, text="Quit", padx = 15, pady = 5, bg = "#263D42", command=leaveGUI)
quitBtn.pack()


root.mainloop()

if stimuliDir != "emptyPath":
    with open('save.txt', 'w') as f:
        print("write save file");
        f.write(stimuliDir);
else:
    print("Don't update save.txt if nothing has been set!");

    #f.write(stimuliDir + ',');
    #f.write(userName);



