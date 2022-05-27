# -*- coding: utf-8 -*-
"""
Created on Fri May 20 10:25:07 2022

@author: Alexander Mueller
"""

import tkinter as tk
import customtkinter as ctk
import os
import hintFunctions as hint
#from tkinter import ttk
#from tkinter import * #filedialog, Text, messagebox
#from functools import partial


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

#root = tk.Tk()
root = ctk.CTk()

stimuliDir = "emptyPath";
userName = "default";
# use save.txt for path and stuff

if os.path.isfile('save.txt'):
    with open('save.txt', 'r') as f:
        print("load save file");
        savedData = f.read()
        splitData = savedData.split(',');
        print(savedData);
#        apps = [x for x in tempApps if x.strip()]
 

def testCallback():
    print("Hey I'm a callback!")
      

def addPath():  
    pathname = tk.filedialog.askdirectory();
    print(pathname)
    # add a sanity check to this (check if .wav are within dir)
    
    global stimuliDir;
    stimuliDir = pathname;
    print(stimuliDir)
    
    
    
def enterName():
    global userName;
    userName = nameField.get();
    print("UserName: " + userName);
    
    
def clearUserName():
    nameField.delete(0, 'end');


def practice():
    print("Start HINT practice");


def startTest():
    print("Start test procedure");
    #storage = hint.createResultStorage(5);
    testLists, testConditions = hint.createTestSetup(hint.getUserIndex, 5);
    hint.hintProcedure(testLists, testConditions, True);
    
    
    
    
#canvas = ctk.CTkCanvas(root, height = 700, width = 700, bg = '#263D42')
#canvas.pack()

frame = ctk.CTkFrame(root, bg = 'white')
frame.place(relwidth = 0.8, relheight = 0.8, relx = 0.1, rely = 0.1)


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

practiceBtn = ctk.CTkButton(frame, text="Practice", padx = 15, pady = 5, bg = "#263D42", command=practice)
practiceBtn.pack();

startBtn = ctk.CTkButton(frame, text="Start test", padx = 15, pady = 5, bg = "#263D42", command=startTest)
startBtn.pack();



# somehow get test information into GUI
# listNumber, condition, SNR, current sentence, current SNR, ...


root.mainloop()


with open('save.txt', 'w') as f:
    print("write save file");
    f.write(stimuliDir + ',');
    f.write(userName);



