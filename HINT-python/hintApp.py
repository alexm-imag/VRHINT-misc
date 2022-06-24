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
    


def quit_me():
    root.quit();
    root.destroy();

def addPath():  
    global stimuliDir;
    pathname = filedialog.askdirectory();
    
    if pathSanityCheck(pathname) != True:
        pathLabel['text'] = "Invalid path!";
        pathLabel.after(2000, resetPathLabel);
        return;
    
    stimuliDir = pathname + '/';
    pathLabel['text'] = "Path: " + stimuliDir;
    
    
def pathSanityCheck(path):
    
    dir = os.listdir(path);
    for file in dir:
        if file == "noiseGR_male.wav":
            return True;
    
    return False;
 
    
      
def enterName(event=None):
    global userName;
    userName = nameField.get();
    print("UserName: " + userName);
    userLabel['text'] = userName;
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
    userIndexLabel['text'] = str(userIndex);

    hintObject = hint.hintTest(stimuliDir, 5, userIndex, 5);
    show_test()
    

def practice():
    print("Start HINT practice");
    global hintObject;    
    hintObject.practiceSetup();
    hintObject.playPracticeSentence();
    


def startTest():
    
    global hintObject;           
    print("Start test procedure");
    
    show_test_running();    
     
    setSentence(hintObject.getCurrentSentenceString(), hintObject.getCurrentSentenceLen());
    setSentenceNumber(hintObject.getSentenceIndex());
    setSNR(hintObject.getCurrentSNR());
    setCondition(hintObject.getCurrentCondition());
      
    feedbackField.grid_forget();
    submitBtn.grid_forget();
        
    
    
def setSentence(sentence, length):
    currentSentence['text'] = sentence.replace("\n", "" );
    currentLength['text'] = str(length);
    
def setSNR(snr):
    currentSNR['text'] = str(snr) + " dB";  
  
def setCondition(condition):
    currentCondition['text'] = condition;
    
def setSentenceNumber(sentIndex):
    sentenceIndexLabel['text'] = str(sentIndex);
    
def setFeedbackOptions(sentLen):
    print("sent len is: " + str(sentLen));
    # add buttons (0, 1, 2, 3, ..., sentLen)
    
def resetPathLabel():
    pathLabel['text'] = "Path: " + stimuliDir;
    
    
def takeFeedback():
    
    global hintObject;
    
    submission = int(feedbackField.get());
    
    if submission < 0 or submission > hintObject.getCurrentSentenceLen():
        print("Invalid input");
        return;

    
    hintObject.enterFeedback(int(submission));
    
    ##### WRAP THESE INTO UPDATE TEST MONITORING FUNCTION
    setSentence(hintObject.getCurrentSentenceString(), hintObject.getCurrentSentenceLen());
    setSentenceNumber(hintObject.getSentenceIndex());
    setSNR(hintObject.getCurrentSNR());
    setCondition(hintObject.getCurrentCondition());
     
    feedbackField.grid_forget();
    submitBtn.grid_forget();
    
    continueBtn.grid(row = 2, column = 2);
 
    
def nextRound():
    hintObject.playCurrentSentence();
    continueBtn.grid_forget();
    feedbackField.grid(row = 2, column = 2);
    submitBtn.grid(row = 3, column = 2);
 
    
# Define a function for switching the frames
def show_setup():
   setup.pack(fill='both', expand=1)
   test.pack_forget()
   test_running.pack_forget()

def show_test():
    
   global userName; 
   
   userLabel1['text'] = "Name: " + userName;
   userIndexLabel1['text'] = "Index: " + str(hint.getUserIndex());
   test.pack(fill='both', expand=1)
   
   setup.pack_forget()
   test_running.pack_forget()
    
def show_test_running():
    test_running.pack(fill='both', expand=1)
    root.geometry("550x300");
    setup.pack_forget()
    test.pack_forget()
    
    
root = ctk.CTk()
root.geometry("400x300");
root.title("Python HINT");
root.protocol("WM_DELETE_WINDOW", quit_me);  
    
# Create two frames in the window
setup = ctk.CTkFrame(root)
test = ctk.CTkFrame(root)
test_running = ctk.CTkFrame(root)


######### SHOW SETUP SCREEN AT LAUNCH
show_setup()

     
############# SETUP SCREEN

root.bind('<Return>', enterName)

setup.columnconfigure(0, weight = 1)
setup.columnconfigure(1, weight = 1)
setup.columnconfigure(2, weight = 1)

topLabel = ctk.CTkLabel(setup, text="Setup")
topLabel.grid(row = 0, column = 1);


nameField = ctk.CTkEntry(setup)
nameField.grid(row = 1, column = 1);

userNameLabel = ctk.CTkLabel(setup, text="Username: default");
userNameLabel.grid(row = 2, column = 1);

pathBtn = ctk.CTkButton(setup, text="Select Path", padx = 15, pady = 5, bg = "#263D42", command=addPath)
pathBtn.grid(row = 3, column = 1, pady = 5);

pathLabel = ctk.CTkLabel(setup, text = stimuliDir);
pathLabel.grid(row = 4, columnspan = 3)


initBtn = ctk.CTkButton(setup, text="Init Test", padx = 15, pady = 5, bg = "#263D42", command=initTest)
initBtn.grid(row = 5, column = 1, pady = 5);

errorLabel = ctk.CTkLabel(setup, text=" ");
errorLabel.grid(row = 6, column = 1);

quitBtn = ctk.CTkButton(setup, text="Quit", padx = 15, pady = 5, bg = "#263D42", command=quit_me)
quitBtn.grid(row = 7, column = 1, pady = 5);




############ TEST SCREEN 1

topLabel = ctk.CTkLabel(test, text="Test Overview ")
topLabel.grid(row = 0, column = 1);

practiceBtn = ctk.CTkButton(test, text="Practice", padx = 15, pady = 5, bg = "#263D42", command=practice)
practiceBtn.grid(row = 1, column = 1);

startBtn = ctk.CTkButton(test, text="Start test", padx = 15, pady = 5, bg = "#263D42", command=startTest)
startBtn.grid(row = 2, column = 1);

userLabel1 = ctk.CTkLabel(test, text="Name: ")
userLabel1.grid(row = 1, column = 0);

userIndexLabel1 = ctk.CTkLabel(test, text="Index: ")
userIndexLabel1.grid(row = 2, column = 0);


setupBtn = ctk.CTkButton(test, text="Setup", padx = 15, pady = 5, bg = "#263D42", command=show_setup)
setupBtn.grid(row = 4, column = 1);

quitBtn = ctk.CTkButton(test, text="Quit", padx = 15, pady = 5, bg = "#263D42", command=quit_me)
quitBtn.grid(row = 5, column = 1);





################ TEST SCREEN 2
topLabel = ctk.CTkLabel(test_running, text="Test screen")
topLabel.grid(row = 0, column = 0);

nameLabel = ctk.CTkLabel(test_running, text="Name: ")
nameLabel.grid(row = 0, column = 0, pady = 7);

userLabel = ctk.CTkLabel(test_running, text="default")
userLabel.grid(row = 0, column = 1, pady = 7);

indexLabel = ctk.CTkLabel(test_running, text="User Index: ")
indexLabel.grid(row = 1, column = 0, pady = 7);

userIndexLabel = ctk.CTkLabel(test_running, text= "0");
userIndexLabel.grid(row = 1, column = 1, pady = 7, padx = 80);

sentenceLabel = ctk.CTkLabel(test_running, text="Sentence: ")
sentenceLabel.grid(row = 2, column = 0, pady = 7);

currentSentence = ctk.CTkLabel(test_running, text="")
currentSentence.grid(row = 2, column = 1, pady = 7);

lengthLabel = ctk.CTkLabel(test_running, text="Length: ")
lengthLabel.grid(row = 3, column = 0, pady = 7);

currentLength = ctk.CTkLabel(test_running, text="0")
currentLength.grid(row = 3, column = 1, pady = 7);

roundLabel = ctk.CTkLabel(test_running, text="Round: ");
roundLabel.grid(row = 4, column = 0, pady = 7);

sentenceIndexLabel = ctk.CTkLabel(test_running, text="0");
sentenceIndexLabel.grid(row = 4, column = 1, pady = 7);

conditionLabel = ctk.CTkLabel(test_running, text="Condition: ")
conditionLabel.grid(row = 5, column = 0, pady = 7);

currentCondition = ctk.CTkLabel(test_running, text="emptyCondition")
currentCondition.grid(row = 5, column = 1, pady = 7);

snrLabel = ctk.CTkLabel(test_running, text="SNR: ")
snrLabel.grid(row = 6, column = 0, pady = 5);

currentSNR = ctk.CTkLabel(test_running, text="0 dB")
currentSNR.grid(row = 6, column = 1, pady = 5);

feedbackField = ctk.CTkEntry(test_running)
feedbackField.grid(row = 1, column = 2);

submitBtn = ctk.CTkButton(test_running, text="Enter", padx = 15, pady = 5, bg = "#263D42", command=takeFeedback)
submitBtn.grid(row = 2, column = 2);

continueBtn = ctk.CTkButton(test_running, text="Play", padx = 15, pady = 5, bg = "#263D42", command=nextRound)
continueBtn.grid(row = 2, column = 2);

quitBtn = ctk.CTkButton(test_running, text="Quit", padx = 15, pady = 5, bg = "#263D42", command=quit_me)
quitBtn.grid(row = 6, column = 2);
    


root.mainloop()


if stimuliDir != "emptyPath":
    with open('save.txt', 'w') as f:
        print("write save file");
        f.write(stimuliDir);
else:
    print("Don't update save.txt if nothing has been set!");