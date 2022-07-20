# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 12:30:11 2022

@author: Alexander Müller
"""

from tkinter import filedialog
import customtkinter as ctk
import os

class HintSetup(ctk.CTkFrame):
        
    def __init__(self, parent, controller):   
                
        ctk.CTkFrame.__init__(self, parent);
        
        self.path = "emptyPath";
        self.userName = "default";
        
        self.ChLeft = 1;
        self.ChFront = 2;
        self.ChRight = 5;
        
        self.parent = parent;
        self.controller = controller;
        
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)
        
        self.topLabel = ctk.CTkLabel(self, text="Setup")
        self.topLabel.grid(row = 0, column = 1);
        
        self.nameField = ctk.CTkEntry(self)
        self.nameField.grid(row = 1, column = 1);
        
        self.userNameLabel = ctk.CTkLabel(self, text="Username: default");
        self.userNameLabel.grid(row = 2, column = 1);
        
        self.pathBtn = ctk.CTkButton(self, text="Select Path", padx = 15, pady = 5, bg = "#263D42", command=self.addPath)
        self.pathBtn.grid(row = 3, column = 1, pady = 5);
        
        self.pathLabel = ctk.CTkLabel(self, text = self.path);
        self.pathLabel.grid(row = 4, columnspan = 3)
        
        self.init1Btn = ctk.CTkButton(self, text="Init Test (1)", padx = 15, pady = 5, bg = "#263D42", command=lambda: self.initTest(1))
        self.init1Btn.grid(row = 5, column = 1, pady = 5);
        
        self.init2Btn = ctk.CTkButton(self, text="Init Test (2)", padx = 15, pady = 5, bg = "#263D42", command=lambda: self.initTest(2))
        self.init2Btn.grid(row = 6, column = 1, pady = 5);
        
        self.errorLabel = ctk.CTkLabel(self, text=" ");
        self.errorLabel.grid(row = 7, column = 1);
        
        self.calibBtn = ctk.CTkButton(self, text="Calibrate", padx = 15, pady = 5, bg = "#263D42", command= self.calibrate)
        self.calibBtn.grid(row = 8, column = 1, pady = 5);
        
        self.quitBtn = ctk.CTkButton(self, text="Quit", padx = 15, pady = 5, bg = "#263D42", command= controller.quit_app)
        self.quitBtn.grid(row = 9, column = 1, pady = 5);
        
        self.nameField.bind('<Return>', self.enterName)
    
    def setDefaultPath(self, path):
        self.path = path;
        self.updateLabels();
        
    def setAudioChannels(self, left, front, right):
        self.ChLeft = left;
        self.ChFront = front;
        self.ChRight = right;
        
    def updateLabels(self):
        self.pathLabel['text'] = self.path;

    def addPath(self):  
        pathname = filedialog.askdirectory();
        
        if self.pathSanityCheck(pathname) != True:
            self.pathLabel['text'] = "Invalid path!";
            self.pathLabel.after(2000, self.resetPathLabel);
            return;
        
        self.path = pathname + '/';
        self.pathLabel['text'] = self.path;
        
        self.controller.setPath(self.path);
        
        
    def pathSanityCheck(self, path):  
        dir = os.listdir(path);
        for file in dir:
            if file == "noiseGR_male.wav":
                return True;
        
        return False;
    
    def resetPathLabel(self):
        self.pathLabel['text'] = self.path;
     
              
    def enterName(self, event=None):
        self.userName = self.nameField.get();
        self.userNameLabel['text'] = "Name: " + self.userName;
        
    
    def initTest(self, testOrder, event = None):        
        if self.userName == "default":
            self.errorLabel['text'] = "No userName set!"; 
            return
        
        
        if self.path == "emptyPath":
            self.errorLabel['text'] = "No path set!"; 
            return;     
            
        print("testOrder: " + str(testOrder));
            
        # hand over setup data to master after sanity check    
        self.controller.setHintParameters(self.userName, self.path, testOrder);
        
    def calibrate(self):
        
        if self.pathSanityCheck(self.path) != True:
            self.pathLabel['text'] = "Invalid path!";
            self.pathLabel.after(2000, self.resetPathLabel);
            return;
            
        self.controller.showCalibration(self.path);
        return;

        