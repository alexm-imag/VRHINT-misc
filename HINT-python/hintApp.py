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
    

def addPath():  
    global stimuliDir;
    pathname = filedialog.askdirectory();
    
    if pathSanityCheck(pathname) != True:
        pathErrorLabel['text'] = "Invalid path!";
        return;
       
    # clean up error label    
    pathErrorLabel['text'] = "";   
    
    stimuliDir = pathname + '/';
    pathLabel['text'] = "Path: " + stimuliDir;
    
    
def pathSanityCheck(path):
    
    dir = os.listdir(path);
    for file in dir:
        if file == "noiseGR_male.wav":
            return True;
    
    return False;
 
    
      
def enterName():
    global userName;
    userName = nameField.get();
    print("UserName: " + userName);
    userLabel['text'] = "Name: " + userName;
    userNameLabel['text'] = "Name: " + userName;
    

def initTest():
    
    global userName;
    global stimuliDir;
    global hintObject;   
    
    if userName == "default":
        print("Set username!");
        errorLabel['text'] = "No userName set!"; 
        return
    
    
    if stimuliDir == "emptyPath":
        print("Set path!");
        errorLabel['text'] = "No path set!"; 
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
    
    # clean up GUI
    practiceBtn.destroy();
    startBtn.destroy();
    continueBtn.pack_forget();
     
    setSentence(hintObject.getCurrentSentenceString(), hintObject.getCurrentSentenceLen());
    setSNR(hintObject.getCurrentSNR());
    setCondition(hintObject.getCurrentCondition());
    hintObject.playCurrentSentence();
    

    
    
    
def setSentence(sentence, length):
    currentSentence['text'] = "Sentence: " + sentence + "(" + str(length) + ")";
    
def setSNR(snr):
    currentSNR['text'] = "SNR: " + str(snr) + " dB";  
  
def setCondition(condition):
    currentCondition['text'] = "Condition:" + condition;
    
def setFeedbackOptions(sentLen):
    print("sent len is: " + str(sentLen));
    # add buttons (0, 1, 2, 3, ..., sentLen)
    
    
def takeFeedback():
    
    global hintObject;
    
    submission = int(feedbackField.get());
    
    if submission < 0 or submission > hintObject.getCurrentSentenceLen():
        print("Invalid input");
        return;


    hintObject.enterFeedback(int(submission));
    setSNR(hintObject.getCurrentSNR());
    setSentence(hintObject.getCurrentSentenceString(), hintObject.getCurrentSentenceLen());
    
    continueBtn.grid(row=5);
 
    
def nextRound():
    hintObject.playCurrentSentence();
    continueBtn.pack_forget();
    
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
   
 

######### SHOW SETUP SCREEN AT LAUNCH
change_to_setup()

     
############# SETUP SCREEN

topLabel = ctk.CTkLabel(setup, text="Setup screen")
topLabel.pack(pady=10)

enterUserNameLabel = ctk.CTkLabel(setup, text="Enter user name");
enterUserNameLabel.pack();

nameField = ctk.CTkEntry(setup)
nameField.pack()

nameBtn = ctk.CTkButton(setup, text="Enter username", padx = 15, pady = 5, bg = "#263D42", command=enterName)
nameBtn.pack()

userNameLabel = ctk.CTkLabel(setup, text="Username: default");
userNameLabel.pack();

pathBtn = ctk.CTkButton(setup, text="Add Path", padx = 15, pady = 5, bg = "#263D42", command=addPath)
pathBtn.pack()

pathErrorLabel = ctk.CTkLabel(setup, text="");
pathErrorLabel.pack();

pathLabel = ctk.CTkLabel(setup, text="Path: " + stimuliDir);
pathLabel.pack();


initBtn = ctk.CTkButton(setup, text="Init Test", padx = 15, pady = 5, bg = "#263D42", command=initTest)
initBtn.pack(pady=20);

errorLabel = ctk.CTkLabel(setup, text=" ");
errorLabel.pack();

quitBtn = ctk.CTkButton(setup, text="Quit", padx = 15, pady = 5, bg = "#263D42", command=leaveGUI)
quitBtn.pack()




############ TEST SCREEN

topLabel = ctk.CTkLabel(test, text="Test screen")
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

currentCondition = ctk.CTkLabel(test, text="Condition: ")
currentCondition.pack()

currentSNR = ctk.CTkLabel(test, text="SNR: ")
currentSNR.pack()

feedbackField = ctk.CTkEntry(test)
feedbackField.pack()

submitBtn = ctk.CTkButton(test, text="Enter", padx = 15, pady = 5, bg = "#263D42", command=takeFeedback)
submitBtn.pack()

continueBtn = ctk.CTkButton(test, text="Next", padx = 15, pady = 5, bg = "#263D42", command=nextRound)
continueBtn.pack()

setupBtn = ctk.CTkButton(test, text="Setup", padx = 15, pady = 5, bg = "#263D42", command=change_to_setup)
setupBtn.pack(pady=20)

quitBtn = ctk.CTkButton(test, text="Quit", padx = 15, pady = 5, bg = "#263D42", command=leaveGUI)
quitBtn.pack()



root.mainloop()

if stimuliDir != "emptyPath":
    with open('save.txt', 'w') as f:
        print("write save file");
        f.write(stimuliDir);
else:
    print("Don't update save.txt if nothing has been set!");