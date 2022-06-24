# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 12:48:37 2022

@author: Alexander Müller
"""

from tkinter import filedialog
import customtkinter as ctk
import os

import hintFunctions as hint
import hintGUISetup as setup
import hintGUITest as test

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# globals
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


class hintGUIMaster(ctk.CTk):
    
    def __init__(self, *args, **kwargs):
        #self.root = 
        ctk.CTk.__init__(self, *args, **kwargs)
        self.root = ctk.CTk;
        # Adding a title to the window
        self.wm_title("Test Application")
 
        self.userName = "default";
        self.path = stimuliDir;
        self.userIndex = 0;
        self.hintObject = '';
 
        # creating a frame and assigning it to container
        self.container = ctk.CTkFrame(self, height=400, width=600)
        # specifying the region where the frame is packed in root
        self.container.pack(side="top", fill="both", expand=True)
 
        # configuring the location of the container using grid
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
    
        self.frames = {}
        
        for F in (setup.HintSetup, test.HintTestOverview, test.HintTestProcedure, test.HintPractice):
            frame = F(self.container, self)
 
            # the windows class acts as the root window for the frames.
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
 
        
        # show first frame
        self.frames[setup.HintSetup].setDefaultPath(self.path);
        #self.show_frame(setup.HintSetup)
        self.showSetup()
        
    def show_frame(self, cont):
        # ALSO RESIZE WINDOW HERE?
       frame = self.frames[cont]
       # raises the current frame to the top
       frame.tkraise()

    def quit_app(self):
       self.quit();
       self.destroy();
       
    def showSetup(self):
        print("Show setup");
        self.root.geometry(self, "400x300");
        self.show_frame(setup.HintSetup);
       
    def setHintParameters(self, userName, path):
        self.userName = userName;
        self.path = path;
    
        self.userIndex = hint.getUserIndex();
        self.hintObject = hint.hintTest(stimuliDir, 5, self.userIndex, 5); 
        
        self.frames[test.HintTestOverview].setParams(self.userName, self.userIndex);  
        
        self.root.geometry(self, "400x250");
        self.show_frame(test.HintTestOverview);
        
    def startHintPractice(self):
        self.frames[test.HintPractice].setParams(self.userName, self.userIndex, self.hintObject);
        self.hintObject.practiceSetup();
        self.frames[test.HintPractice].startTest();
        self.root.geometry(self, "550x300");
        self.show_frame(test.HintPractice);
        
    def startHintProcedure(self):
        self.frames[test.HintTestProcedure].setParams(self.userName, self.userIndex, self.hintObject);
        self.frames[test.HintTestProcedure].startTest();
        self.root.geometry(self, "550x300");
        self.show_frame(test.HintTestProcedure);
        
    def practiceDone(self):
        self.show_frame(test.HintTestOverview);
               

        
testObj = hintGUIMaster()
testObj.mainloop();


if stimuliDir != "emptyPath":
    with open('save.txt', 'w') as f:
        print("write save file");
        f.write(stimuliDir);
else:
    print("Don't update save.txt if nothing has been set!");