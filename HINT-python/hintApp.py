# -*- coding: utf-8 -*-
"""
Created on Fri May 20 10:25:07 2022

@author: Alexander Mueller
"""

import tkinter as tk
import os
#from tkinter import ttk
#from tkinter import * #filedialog, Text, messagebox
#from functools import partial

root = tk.Tk()

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
    
    
    
    

canvas = tk.Canvas(root, height = 700, width = 700, bg = '#263D42')
canvas.pack()

frame = tk.Frame(root, bg = 'white')
frame.place(relwidth = 0.8, relheight = 0.8, relx = 0.1, rely = 0.1)


nameField = tk.Entry(frame)
#nameField.place(relx = 0.45, rely = 0.5)
nameField.pack()
#nameField.grid(row=0, column=0)

# command=partial(enterName, tmp)
nameBtn = tk.Button(frame, text="Enter participants name", padx = 10, pady = 5, fg = "white", bg = "#263D42", command=enterName)
nameBtn.pack()

clearBtn = tk.Button(frame, text="Clear field", padx = 10, pady = 5, fg = "white", bg = "#263D42", command=clearUserName)
clearBtn.pack()

pathBtn = tk.Button(frame, text="Add Path", padx = 10, pady = 5, fg = "white", bg = "#263D42", command=addPath)
pathBtn.pack()

practiceBtn = tk.Button(frame, text="Practice", padx = 10, pady = 5, fg = "white", bg = "#263D42", command=practice)
practiceBtn.pack();

startBtn = tk.Button(frame, text="Start test", padx = 10, pady = 5, fg = "white", bg = "#263D42", command=startTest)
startBtn.pack();


root.mainloop()


with open('save.txt', 'w') as f:
    print("write save file");
    f.write(stimuliDir + ',');
    f.write(userName);



