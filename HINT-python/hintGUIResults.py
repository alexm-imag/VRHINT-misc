# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 09:00:59 2022

@author: Alexander Müller
"""

import customtkinter as ctk


class HintResults(ctk.CTkFrame):
        
    def __init__(self, parent, controller):   
                
        ctk.CTkFrame.__init__(self, parent);
        
        self.parent = parent;
        self.controller = controller;
        
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)
        
        self.topLabel = ctk.CTkLabel(self, text="Results")
        self.topLabel.grid(row = 0, column = 1);
        
        
        self.nameDescLabel = ctk.CTkLabel(self, text="Username: ")
        self.nameDescLabel.grid(row = 1, column = 0, pady = 5);
        
        self.userNameLabel = ctk.CTkLabel(self, text="default")
        self.userNameLabel.grid(row = 1, column = 1, pady = 5);
        
        self.snrLabel = ctk.CTkLabel(self, text="Conditions: ")
        self.snrLabel.grid(row = 2, column = 0, pady = 5);
        
        self.currentSNR = ctk.CTkLabel(self, text="cond1 cond2")
        self.currentSNR.grid(row = 2, column = 1, pady = 5);
        
        self.snrLabel = ctk.CTkLabel(self, text="Lists: ")
        self.snrLabel.grid(row = 3, column = 0, pady = 5);
        
        self.currentSNR = ctk.CTkLabel(self, text="8 4 3")
        self.currentSNR.grid(row = 3, column = 1, pady = 5);
        
        self.snrLabel = ctk.CTkLabel(self, text="Average SNRs: ")
        self.snrLabel.grid(row = 4, column = 0, pady = 5);
        
        self.currentSNR = ctk.CTkLabel(self, text="3.7 -4.9 -2.3")
        self.currentSNR.grid(row = 4, column = 1, pady = 5);
        
        
        self.returnBtn = ctk.CTkButton(self, text="Return", padx = 15, pady = 5, bg = "#263D42", command= controller.quit_app)
        self.returnBtn.grid(row = 7, column = 1, pady = 5);
        
        self.quitBtn = ctk.CTkButton(self, text="Quit", padx = 15, pady = 5, bg = "#263D42", command= controller.quit_app)
        self.quitBtn.grid(row = 7, column = 1, pady = 5);
        
    
    def setUserName(self, userName):
        self.userNameLabel['text'] = "TestName";
    
    def setData(self, hintObject, userName, userIndex):
        print("Get data from hint Object");
        resultData = hintObject.resultStorage;
        print(resultData);
        self.setUserName(userName);
        print(resultData['Condition'])
        
        
    def updateLabels(self):
        self.pathLabel['text'] = self.path;

