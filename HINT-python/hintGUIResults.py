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
        
        self.topLabel = ctk.CTkLabel(self, text="Setup")
        self.topLabel.grid(row = 0, column = 1);
        
        
        self.userNameLabel = ctk.CTkLabel(self, text="Username: default");
        self.userNameLabel.grid(row = 2, column = 1);
        
        #self.pathBtn = ctk.CTkButton(self, text="Select Path", padx = 15, pady = 5, bg = "#263D42", command=self.addPath)
        #self.pathBtn.grid(row = 3, column = 1, pady = 5);
        
        #self.pathLabel = ctk.CTkLabel(self, text = self.path);
        #self.pathLabel.grid(row = 4, columnspan = 3)
        
        self.returnBtn = ctk.CTkButton(self, text="Return", padx = 15, pady = 5, bg = "#263D42", command= controller.quit_app)
        self.returnBtn.grid(row = 7, column = 1, pady = 5);
        
        self.quitBtn = ctk.CTkButton(self, text="Quit", padx = 15, pady = 5, bg = "#263D42", command= controller.quit_app)
        self.quitBtn.grid(row = 7, column = 1, pady = 5);
        
    
    def setData(self, hintObject):
        print("Get data from hint Object");
        
    def updateLabels(self):
        self.pathLabel['text'] = self.path;

