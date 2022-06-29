# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 10:42:03 2022

@author: Alexander Müller
"""

import customtkinter as ctk

class HintTestOverview(ctk.CTkFrame):
    
    def __init__(self, parent, controller):   
                
        ctk.CTkFrame.__init__(self, parent);
        
        self.controller = controller;
        
        self.userName = "default";
        self.path = "emptyPath";
        self.userIndex = 0;
        
        self.topLabel = ctk.CTkLabel(self, text="Test Overview")
        self.topLabel.grid(row = 0, column = 0, columnspan = 3, pady = 10);
        
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)
        
        self.practiceBtn = ctk.CTkButton(self, text="Practice", padx = 15, pady = 5, bg = "#263D42", command= controller.startHintPractice);
        self.practiceBtn.grid(row = 1, column = 1, pady = 5);
        
        self.startBtn = ctk.CTkButton(self, text="Start test", padx = 15, pady = 5, bg = "#263D42", command= controller.startHintProcedure);
        self.startBtn.grid(row = 2, column = 1, pady = 5);
        
        self.setupBtn = ctk.CTkButton(self, text="Setup", padx = 15, pady = 5, bg = "#263D42", command= controller.showSetup);
        self.setupBtn.grid(row = 4, column = 1, pady = 5);
        
        self.quitBtn = ctk.CTkButton(self, text="Quit", padx = 15, pady = 5, bg = "#263D42", command= controller.quit_app)
        self.quitBtn.grid(row = 5, column = 1, pady = 5);      
        
    def setParams(self, userName, userIndex):
        self.userName = userName;
        self.userIndex = userIndex;
        self.updateLabels();
        
    def updateLabels(self):
        self.topLabel['text'] = "Test Overview (" + self.userName +") " + str(self.userIndex);
        
        
class HintTestProcedure(ctk.CTkFrame):
       
    def __init__(self, parent, controller):   
                
        ctk.CTkFrame.__init__(self, parent);
        
        self.controller = controller;
        
        self.hintObject = '';
        
        self.topLabel = ctk.CTkLabel(self, text="Test screen")
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
        
        self.quitBtn = ctk.CTkButton(self, text="Quit", padx = 15, pady = 5, bg = "#263D42", command= controller.quit_app)
        self.quitBtn.grid(row = 6, column = 2);
        
        self.feedbackField.bind('<Return>', self.takeFeedback);
        self.continueBtn.bind('<Return>', self.nextRound);
    
    
    def nextRound(self):
        
        if self.continueBtn.grid_info() == {}:
            print("Play not available");
            return;
            
        self.hintObject.playCurrentSentence();
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

        self.hintObject.enterFeedback(int(submission));
        self.updateHintLabels();
        
        self.feedbackField.delete(0, 'end');
        self.feedbackField.grid_forget();
        self.continueBtn.grid(row = 2, column = 2);
        
    def startTest(self):
        self.updateHintLabels();          
        self.feedbackField.grid_forget();
        
    def setSentence(self, sentence, length):
        self.currentSentence['text'] = sentence.replace("\n", "" );
        self.currentLength['text'] = str(length);
        
    def setSNR(self, snr):
        self.currentSNR['text'] = str(snr) + " dB";  
      
    def setCondition(self, condition):
        self.currentCondition['text'] = condition;
        
    def setSentenceNumber(self, sentIndex):
        self.sentenceIndexLabel['text'] = str(sentIndex);
        
    def setParams(self, userName, userIndex, hintObject):
        self.userName = userName;
        self.userIndex = userIndex;
        self.hintObject = hintObject;
        self.updateLabels();
        
    def updateHintLabels(self):
        self.setSentence(self.hintObject.getCurrentSentenceString(), self.hintObject.getCurrentSentenceLen());
        self.setSentenceNumber(self.hintObject.getSentenceIndex());
        self.setSNR(self.hintObject.getCurrentSNR());
        self.setCondition(self.hintObject.getCurrentCondition());
        
    def updateLabels(self):
        self.userLabel['text'] = self.userName;
        self.userIndexLabel['text'] = self.userIndex;
        

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

        self.hintObject.enterPracticeFeedback(int(submission));
        self.updateHintLabels();
        
        self.feedbackField.delete(0, 'end');
        self.feedbackField.grid_forget();
        self.continueBtn.grid(row = 2, column = 2);
        
        if self.hintObject.getSentenceIndex() >= self.hintObject.getPracticeRounds():
            # hide Play button
            self.continueBtn.grid_forget();
            self.doneBtn.grid(row = 2, column = 2);
        
    def startTest(self):
        self.updateHintLabels();          
        self.feedbackField.grid_forget();
        
        
    def setSentence(self, sentence, length):
        self.currentSentence['text'] = sentence.replace("\n", "" );
        self.currentLength['text'] = str(length);
        
    def setSNR(self, snr):
        self.currentSNR['text'] = str(snr) + " dB";  
      
    def setCondition(self, condition):
        self.currentCondition['text'] = condition;
        
    def setSentenceNumber(self, sentIndex):
        self.sentenceIndexLabel['text'] = str(sentIndex);
        
    def setParams(self, userName, userIndex, hintObject):
        self.userName = userName;
        self.userIndex = userIndex;
        self.hintObject = hintObject;
        self.updateLabels();
        
    def updateHintLabels(self):
        self.setSentence(self.hintObject.getCurrentSentenceString(), self.hintObject.getCurrentSentenceLen());
        self.setSentenceNumber(self.hintObject.getSentenceIndex());
        self.setSNR(self.hintObject.getCurrentSNR());
        self.setCondition(self.hintObject.getCurrentCondition());
        
    def updateLabels(self):
        self.userLabel['text'] = self.userName;
        self.userIndexLabel['text'] = self.userIndex;
        