

%% Load HD600 filt & audio stimuli
load('Sennheiser-HD600_reg.mat');
hpcf = hpcf.minPhase;
a=dir(['HINT_Ger_male_single_sentences' '/*.wav']);


%% Load and upSample audio files
for i = 1:size(a,1)
    sAudioFile = a(i).name;
    [y,Fs] = audioread(sAudioFile); 
    y_resamp = resample(y,48000,24000);


%% Convolve filter with upsampled audio
    hd600HINT = conv(y_resamp, hpcf);

%% Store filtered audio file
% Write .wavs pf stimuli + headphone filter
    filename = ['filteredStimuli/hd600' a(i).name];
    audiowrite(filename,hd600HINT, 48000);
end

%% Resample only
a=dir(['HINT_Ger_male_single_sentences' '/*.wav']);

%% Load and upSample audio files
for i = 1:size(a,1)
    sAudioFile = a(i).name;
    [y,Fs] = audioread(['HINT_Ger_male_single_sentences/' sAudioFile]); 
    y_resamp = resample(y,48000,24000);

    %% avoid clipping after resamp
    if max(abs(y_resamp) >= 1)
        y_norm = y_resamp ./ max(abs(y_resamp));
    else
        y_norm = y_resamp;
    end

% Store filtered audio file
    filename = ['german-hint-48kHz/' a(i).name];
    audiowrite(filename, y_norm, 48000);
end