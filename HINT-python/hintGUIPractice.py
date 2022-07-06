# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 08:40:18 2022

@author: Alexander Müller
"""

import customtkinter as ctk

class HintPractice(ctk.CTkFrame):
    def __init__(self, parent, controller):   
                
        ctk.CTkFrame.__init__(self, parent);
        
        self.controller = controller;
        
        self.hintObject = '';
        
        self.topLabel = ctk.CTkLabel(self, text="Practice screen")
        self.topLabel.grid(row = 0, column = 0);
        
        self.nameLabel = ctk.CTkLabel(self, text="Name: ")
        self.nameLabel.grid(row = 0, column = 0, pady = 7);
        
        self.userLabel = ctk.CTkLabel(self, text="default")
        self.userLabel.grid(row = 0, column = 1, pady = 7);
        
        self.indexLabel = ctk.CTkLabel(self, text="User Index: ")
        self.indexLabel.grid(row = 1, column = 0, pady = 7);
        
        self.userIndexLabel = ctk.CTkLabel(self, text= "0");
        self.userIndexLabel.grid(row = 1, column = 1, pady = 7, padx = 80);
        
        self.sentenceLabel = ctk.CTkLabel(self, text="Sentence: ")
        self.sentenceLabel.grid(row = 2, column = 0, pady = 7);
        
        self.currentSentence = ctk.CTkLabel(self, text="")
        self.currentSentence.grid(row = 2, column = 1, pady = 7);
        
        self.lengthLabel = ctk.CTkLabel(self, text="Length: ")
        self.lengthLabel.grid(row = 3, column = 0, pady = 7);
        
        self.currentLength = ctk.CTkLabel(self, text="0")
        self.currentLength.grid(row = 3, column = 1, pady = 7);
        
        self.roundLabel = ctk.CTkLabel(self, text="Round: ");
        self.roundLabel.grid(row = 4, column = 0, pady = 7);
        
        self.sentenceIndexLabel = ctk.CTkLabel(self, text="0");
        self.sentenceIndexLabel.grid(row = 4, column = 1, pady = 7);
        
        self.conditionLabel = ctk.CTkLabel(self, text="Condition: ")
        self.conditionLabel.grid(row = 5, column = 0, pady = 7);
        
        self.currentCondition = ctk.CTkLabel(self, text="emptyCondition")
        self.currentCondition.grid(row = 5, column = 1, pady = 7);
        
        self.snrLabel = ctk.CTkLabel(self, text="SNR: ")
        self.snrLabel.grid(row = 6, column = 0, pady = 5);
        
        self.currentSNR = ctk.CTkLabel(self, text="0 dB")
        self.currentSNR.grid(row = 6, column = 1, pady = 5);
        
        self.feedbackField = ctk.CTkEntry(self)
        self.feedbackField.grid(row = 1, column = 2);
        
        self.continueBtn = ctk.CTkButton(self, text="Play", padx = 15, pady = 5, bg = "#263D42", command=self.nextRound)
        self.continueBtn.grid(row = 2, column = 2);
        
        self.doneBtn = ctk.CTkButton(self, text="Done", padx = 15, pady = 5, bg = "#263D42", command=controller.practiceDone)
        
        self.returnBtn = ctk.CTkButton(self, text="Return", padx = 15, pady = 5, bg = "#263D42", command= controller.practiceDone)
        self.returnBtn.grid(row = 5, column = 2);
        
        self.quitBtn = ctk.CTkButton(self, text="Quit", padx = 15, pady = 5, bg = "#263D42", command= controller.quit_app)
        self.quitBtn.grid(row = 6, column = 2);
        
        self.feedbackField.bind('<Return>', self.takeFeedback)
        self.continueBtn.bind('<Return>', self.nextRound)
    
    
    def nextRound(self):
        
        if self.continueBtn.grid_info() == {}:
            print("Play not available");
            return;
        
        self.hintObject.playPracticeSentence();
        self.continueBtn.grid_forget();
        self.feedbackField.grid(row = 2, column = 2);
        self.feedbackField.focus();
        
    def takeFeedback(self, event=None):
        
        if self.feedbackField.grid_info() == {}:
            print("Feedback not active");
            return;
        
        submission = int(self.feedbackField.get());
    
        if submission < 0 or submission > self.hintObject.getCurrentSentenceLen():
            print("Invalid input");
            self.feedbackField['text'] = 'Invalid input!';
            return;

        if self.hintObject.enterPracticeFeedback(int(submission)) == 1:
            print("GUI Prac: Practice done");
            self.continueBtn.grid_forget();
            self.doneBtn.grid(row = 2, column = 2);
            
        self.updateHintLabels();
        
        self.feedbackField.delete(0, 'end');
        self.feedbackField.grid_forget();
        self.continueBtn.grid(row = 2, column = 2);
        
        
    def startTest(self):
        self.updateHintLabels();    
        self.doneBtn.grid_forget();
        self.feedbackField.grid_forget();
        
        
    def setSentence(self, sentence, length):
        self.currentSentence['text'] = sentence.replace("\n", "" );
        self.currentLength['text'] = str(length);
        
    def setSNR(self, snr):
        self.currentSNR['text'] = str(snr) + " dB";  
      
    def setCondition(self, condition):
        self.currentCondition['text'] = condition;
        
    def setSentenceNumber(self, sentIndex, sentCount):
        self.sentenceIndexLabel['text'] = str(sentIndex) + " of " + str(sentCount); 
        
    def setParams(self, userName, userIndex, hintObject):
        self.userName = userName;
        self.userIndex = userIndex;
        self.hintObject = hintObject;
        self.updateLabels();
        
    def updateHintLabels(self):
        self.setSentence(self.hintObject.getCurrentSentenceString(), self.hintObject.getCurrentSentenceLen());
        self.setSentenceNumber(self.hintObject.getSentenceIndex() + 1, self.hintObject.getPracticeRounds());
        self.setSNR(self.hintObject.getCurrentSNR());
        self.setCondition(self.hintObject.getCurrentCondition());
        
    def updateLabels(self):
        self.userLabel['text'] = self.userName;
        self.userIndexLabel['text'] = self.userIndex;
        