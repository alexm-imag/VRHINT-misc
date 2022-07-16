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
        
        self.listsDescLabel = ctk.CTkLabel(self, text="Lists: ")
        self.listsDescLabel.grid(row = 2, column = 0, pady = 5);
        
        self.condDescLabel = ctk.CTkLabel(self, text="Conditions: ")
        self.condDescLabel.grid(row = 3, column = 0, pady = 5);
        
        self.condsLabel = ctk.CTkLabel(self, text="cond1 cond2")
        self.condsLabel.grid(row = 3, column = 1, pady = 5);
        
        self.listsLabel = ctk.CTkLabel(self, text="8 4 3")
        self.listsLabel.grid(row = 2, column = 1, pady = 5);
        
        self.avgSNRDescLabel = ctk.CTkLabel(self, text="Average SNRs: ")
        self.avgSNRDescLabel.grid(row = 4, column = 0, pady = 5);
        
        self.avgSNRLabel = ctk.CTkLabel(self, text="3.7 -4.9 -2.3")
        self.avgSNRLabel.grid(row = 4, column = 1, pady = 5);
        
        
        self.returnBtn = ctk.CTkButton(self, text="Return", padx = 15, pady = 5, bg = "#263D42", command= controller.quit_app)
        self.returnBtn.grid(row = 7, column = 1, pady = 5);
        
        self.quitBtn = ctk.CTkButton(self, text="Quit", padx = 15, pady = 5, bg = "#263D42", command= controller.quit_app)
        self.quitBtn.grid(row = 7, column = 1, pady = 5);
        
    
    def setUserName(self, userName):
        self.userNameLabel['text'] = userName;
        
    def setConditions(self, conds):
        self.condsLabel['text'] = str(conds);
        
    def setAverageSNRs(self, snrs):
            self.avgSNRLabel['text'] = str(snrs);
        
    def setLists(self, lists):
        self.listsLabel['text'] = str(lists);
    
    def setData(self, hintObject, userName, userIndex):        
        resultData = hintObject.resultStorage['subResults'];
        self.setUserName(userName);
        conds = [resultData[k]['Condition'] for k in range(len(resultData))]
        lists = [resultData[k]['ListIndex'] for k in range(len(resultData))]
        snrs = [resultData[k]['ListSNRAverage'] for k in range(len(resultData))]
        
        self.setConditions(conds);
        self.setLists(lists);
        self.setAverageSNRs(snrs);

