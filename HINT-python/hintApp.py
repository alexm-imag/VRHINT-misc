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
    
    global userName;
    global stimuliDir;
    global hintObject;   
    
    if userName == "default":
        print("Set username!");
        return
    
    
    if stimuliDir == "emptyPath":
        print("Set path!");
        return;
    
    
    userIndex = hint.getUserIndex();
    userIndexLabel['text'] = "User Index: " + str(userIndex);

    hintObject = hint.hintTest(stimuliDir, 5, userIndex, 5);
    change_to_test()

def practice():
    print("Start HINT practice");
    global hintObject;    
    hintObject.practiceSetup();
    hintObject.playPracticeSentence();
    


def startTest():
    
    global hintObject;           
    print("Start test procedure");
     
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

# Create two frames in the window
setup = ctk.CTkFrame(root)
test = ctk.CTkFrame(root)

# Define a function for switching the frames
def change_to_setup():
   setup.pack(fill='both', expand=1)
   test.pack_forget()

def change_to_test():
   test.pack(fill='both', expand=1)
   setup.pack_forget()
   
 
############## PERSISITENT STUFF (MAPPED TO ROOT)
# Add a button to switch between two frames
#btn1 = ctk.CTkButton(root, text="Switch to setup", command=change_to_setup)
#btn1.pack(pady=10)

#btn2 = ctk.CTkButton(root, text="Switch to test", command=change_to_test)
#btn2.pack(pady=10)


######### SHOW SETUP SCREEN AT LAUNCH
change_to_setup()

     
############# SETUP SCREEN

topLabel = ctk.CTkLabel(setup, text="Setup screen")
topLabel.pack()

userNameLabel = ctk.CTkLabel(setup, text="Enter user name");
userNameLabel.pack();

nameField = ctk.CTkEntry(setup)
nameField.pack()

nameBtn = ctk.CTkButton(setup, text="Enter participants name", padx = 15, pady = 5, bg = "#263D42", command=enterName)
nameBtn.pack()

clearBtn = ctk.CTkButton(setup, text="Clear field", padx = 15, pady = 5, bg = "#263D42", command=clearUserName)
clearBtn.pack()

pathBtn = ctk.CTkButton(setup, text="Add Path", padx = 15, pady = 5, bg = "#263D42", command=addPath)
pathBtn.pack()

initBtn = ctk.CTkButton(setup, text="Init Test", padx = 15, pady = 5, bg = "#263D42", command=initTest)
initBtn.pack();

quitBtn = ctk.CTkButton(setup, text="Quit", padx = 15, pady = 5, bg = "#263D42", command=leaveGUI)
quitBtn.pack()




############ TEST SCREEN

topLabel = ctk.CTkLabel(setup, text="Test screen")
topLabel.pack()

practiceBtn = ctk.CTkButton(test, text="Practice", padx = 15, pady = 5, bg = "#263D42", command=practice)
practiceBtn.pack();

startBtn = ctk.CTkButton(test, text="Start test", padx = 15, pady = 5, bg = "#263D42", command=startTest)
startBtn.pack();


userLabel = ctk.CTkLabel(test, text="Name: ")
userLabel.pack()

userIndexLabel = ctk.CTkLabel(test, text="Index: ")
userIndexLabel.pack()

currentSentence = ctk.CTkLabel(test, text="Sentence: ")
currentSentence.pack()

currentSNR = ctk.CTkLabel(test, text="SNR: ")
currentSNR.pack()

feedbackField = ctk.CTkEntry(test)
feedbackField.pack()

submitBtn = ctk.CTkButton(test, text="Enter", padx = 15, pady = 5, bg = "#263D42", command=takeFeedback)
submitBtn.pack()

setupBtn = ctk.CTkButton(test, text="Setup", padx = 15, pady = 5, bg = "#263D42", command=change_to_setup)
setupBtn.pack()

quitBtn = ctk.CTkButton(test, text="Quit", padx = 15, pady = 5, bg = "#263D42", command=leaveGUI)
quitBtn.pack()






root.mainloop()