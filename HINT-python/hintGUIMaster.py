# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 12:48:37 2022

@author: Alexander Müller
"""

import customtkinter as ctk
import os

import hintFunctions as hint
import hintGUISetup as setup
import hintGUITest as test
import hintGUICalibration as calib
import hintGUIPractice as prac
import hintGUIResults as res

ctk.set_appearance_mode("System")
#ctk.set_default_color_theme("blue")

# globals
ChLeft = 3;
ChFront = 2;
ChRight = 1;
# use sounddevice.query_devices() to find correct one!
# 8 on laptop, 10 on TH desktop
audioInterface = 10;

class hintGUIMaster(ctk.CTk):
    
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        self.root = ctk.CTk;
        # Adding a title to the window
        self.wm_title("Test Application")
 
        # set default values
        self.userName = "default";
        self.path = "emptyPath";
        self.userIndex = 0;
        self.hintObject = '';
 
        self.loadPersistentData();
         
        # creating a frame and assigning it to container
        self.container = ctk.CTkFrame(self, height=400, width=600)
        # specifying the region where the frame is packed in root
        self.container.pack(side="top", fill="both", expand=True)
 
        # configuring the location of the container using grid
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
    
        self.frames = {}
        
        for F in (setup.HintSetup, 
                  calib.HintCalibration,
                  test.HintTestOverview, 
                  test.HintTestProcedure, 
                  prac.HintPractice,
                  res.HintResults):
            
            frame = F(self.container, self)
 
            # the windows class acts as the root window for the frames.
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
         
        # show first frame
        print("Call sd setup...");
        self.frames[calib.HintCalibration].setAudioChannels(ChLeft, ChFront, ChRight, audioInterface);
        
        self.frames[setup.HintSetup].setDefaultPath(self.path);
        self.frames[setup.HintSetup].setAudioChannels(ChLeft, ChFront, ChRight);
        self.showSetup()
        
    def show_frame(self, cont):
       frame = self.frames[cont]
       # raises the current frame to the top
       frame.tkraise()

    def quit_app(self):
       self.storePersistentData();
       self.quit();
       self.destroy();
       
    def loadPersistentData(self): 
        if os.path.isfile('save.txt'):
            with open('save.txt', 'r') as f:
                print("Master: Loaded persistent data.");
                savedData = f.read()
                self.path = savedData;
                
    def storePersistentData(self):
        if self.path != "emptyPath":
            with open('save.txt', 'w') as f:
                print("write save file");
                print(self.path);
                f.write(self.path);
        else:
            print("Don't update s'ave.txt if nothing has been set!");
       
    def showSetup(self):
        
        # set all setup bindings
        self.bind('<space>', self.frames[setup.HintSetup].initTest);
        
        self.root.geometry(self, "450x400");
        self.show_frame(setup.HintSetup);
        
    def showCalibration(self, path):
        self.root.geometry(self, "450x250");
        self.frames[calib.HintCalibration].setAudioChannels(ChLeft, ChFront, ChRight, audioInterface);
        self.frames[calib.HintCalibration].setPath(path);
        self.show_frame(calib.HintCalibration);
       
    def setHintParameters(self, userName, path, testOrder):
        self.userName = userName;
        self.path = path;
        
        # unbind events for other screens
        self.unbind('<space>');
        self.unbind('<Tab>');
    
        self.hintObject = hint.hintTest(path, self.userName, testOrder); 
        #self.hintObject = hint.hintTest(self.path, self.userName, testOrder, 5, 8, 0); 
        self.hintObject.audioSettings(ChLeft, ChFront, ChRight);
        self.userIndex = self.hintObject.getUserIndex();
        
        self.frames[test.HintTestOverview].setParams(self.userName, self.userIndex);  
        
        self.root.geometry(self, "400x250");
        self.show_frame(test.HintTestOverview);
        
    def startHintPractice(self):
        self.frames[prac.HintPractice].setParams(self.userName, self.userIndex, self.hintObject);
        self.hintObject.practiceSetup();
        self.frames[prac.HintPractice].startTest();
        self.root.geometry(self, "600x300");
        self.show_frame(prac.HintPractice);
        
    def startHintProcedure(self):
        
        self.unbind_all('<space>')
        self.bind('<space>', self.frames[test.HintTestProcedure].nextRound)
        self.bind('<Tab>', self.frames[test.HintTestProcedure].setFocus)
        
        self.frames[test.HintTestProcedure].setParams(self.userName, self.userIndex, self.hintObject);
        self.hintObject.testSetup();
        self.frames[test.HintTestProcedure].startTest();
        self.root.geometry(self, "600x400");
        self.show_frame(test.HintTestProcedure);
        
    def showResults(self):
        self.frames[res.HintResults].setData(self.hintObject, self.userName, self.userIndex);
        self.root.geometry(self, "550x350");
        self.show_frame(res.HintResults);
        
    def practiceDone(self):
        self.show_frame(test.HintTestOverview);
        
    def setPath(self, path):
        self.path = path;
        
    def getPath(self):
        return self.path;
               

# Create guiMasterObject        
hintGuiMaster = hintGUIMaster();

# run mainloop
hintGuiMaster.mainloop();
