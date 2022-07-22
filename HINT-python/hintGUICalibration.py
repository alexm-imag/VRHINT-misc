# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 15:53:02 2022

@author: Alexander Müller
"""


import customtkinter as ctk
import soundfile as sf
import sounddevice as sd


class HintCalibration(ctk.CTkFrame):
        
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
        
        self.topLabel = ctk.CTkLabel(self, text="Calibration")
        self.topLabel.grid(row = 0, column = 1);
        
        self.stop = False;
        
        
        self.initBtn = ctk.CTkButton(self, text="Noise Left", padx = 15, pady = 5, bg = "#263D42", command=lambda: self.calibrateNoise(self.ChLeft))
        self.initBtn.grid(row = 1, column = 0, pady = 5);
        
        self.initBtn = ctk.CTkButton(self, text="Noise Front", padx = 15, pady = 5, bg = "#263D42", command=lambda: self.calibrateNoise(self.ChFront))
        self.initBtn.grid(row = 1, column = 1, pady = 5);
        
        self.initBtn = ctk.CTkButton(self, text="Noise Right", padx = 15, pady = 5, bg = "#263D42", command=lambda: self.calibrateNoise(self.ChRight));
        self.initBtn.grid(row = 1, column = 2, pady = 5);
        
        self.initBtn = ctk.CTkButton(self, text="Speech Front", padx = 15, pady = 5, bg = "#263D42", command=self.calibrateSpeech)
        self.initBtn.grid(row = 2, column = 1, pady = 5);
        
        
        self.calibBtn = ctk.CTkButton(self, text="Stop", padx = 15, pady = 5, bg = "#263D42", command=self.calibrateStop)
        self.calibBtn.grid(row = 3, column = 1, pady = 5);
        
        self.quitBtn = ctk.CTkButton(self, text="Return", padx = 15, pady = 5, bg = "#263D42", command= controller.showSetup)
        self.quitBtn.grid(row = 4, column = 1, pady = 5);
    
        
    def setAudioChannels(self, left, front, right, defaultDevice = 0):
        self.ChLeft = left;
        self.ChFront = front;
        self.ChRight = right;
        
        print("Set default device to: " + str(defaultDevice));
        sd.default.device = defaultDevice;
        
        
        
    def setPath(self, path):
        self.path = path;
        noise, fs = sf.read(self.path + "noiseGR_male_-27dB.wav");
        print("Set default sampleRate to: " + str(fs));
        sd.default.samplerate = fs;
             
        
    def calibrateNoise(self, channel):
        noise, fs = sf.read(self.path + "noiseGR_male_-27dB.wav");
        
        print("Noise (" + str(channel) + ")");
        sd.play(noise, loop = 'true', mapping = channel);
        
        
    def calibrateSpeech(self):
        
        print("Speech front (" + str(self.ChFront) + ")");
        #speech,fs = sf.read(self.path + "\\01\\-6dB\\Ger_male001.wav");
        #sd.play(speech, loop = 'true', mapping = self.ChFront);
        
        for i in range(20):
            
            if self.stop == True:
                self.stop = False;
                return;
            
            if (i+1) < 10:
                speechPath = self.path + "\\01\\-6dB\\Ger_male00" + str(i+1) + ".wav"
            else:
                speechPath = self.path + "\\01\\-6dB\\Ger_male0" + str(i+1) + ".wav"
                
            speech,fs = sf.read(speechPath);
            sd.play(speech, blocking = 'true', mapping = self.ChFront);                
        
    def calibrateStop(self):
        self.stop = False;
        sd.stop();
        