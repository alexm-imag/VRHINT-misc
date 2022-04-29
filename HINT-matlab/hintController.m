
%% Path stuff

addpath('Functions')  
addpath('german-hint-adaptive-48kHz/')  
addpath('Third-party')  
%savepath matlab/myfiles/pathdef.m

hintDir = 'german-hint-adaptive-48kHz\';

%% Test setup
% lists open for test
availableTestLists = 10;
% number of lists used in the test
numTestLists = 5;
% number of sentences in each list
listSentences = 20;

% min/max available SNR
minSNR = -16;
maxSNR = 2;

% practice setup
practiceList = 12;
practiceRounds = 5;
practiceCondition = "noiseFront";

%% Type definitions etc
tempAudioStruct = struct('AudioData', 1, 'Channel', 1);

% this format works for sentence indices, SNR values and hit Quotes
templateData = zeros(listSentences, 1);
templateCondition = "noiseLeft";
templateListIndex = 12;

resTemplate = struct('ListIndex', templateListIndex, 'Condition', templateCondition, 'ListSNRs', templateData, 'ListHitQuotes', templateData);

% allocate numTestLists structs to store results
resultStorage = repmat(resTemplate, numTestLists, 1 ); 

%% user login
prompt = "Enter participants name:\n";
name = input(prompt, "s");

%% pre-allocate struct array for results

% add system to check if username has already been used!
% create file name based on user name
%jsonFileName = sprintf("results-%s-%s.json", name, datestr(now, 'dd-mm-yyyy-hh:MM'));
jsonFileName = sprintf("results-%s.json", name);

%% load stimuli
% load calibration noise
calibrationNoise = audioread([hintDir 'NBNoise1000.wav']);
[noise,fs] = audioread([hintDir 'noiseGR_male.wav']);

%% Initialize playrec
init_playrec(fs);

% define channel map
%ChMap= [1 3 5]; % uni setup
%ChLeft = 1;
%ChFront = 3;
%ChRight = 5;

ChMap = [1 2]; % at home
ChLeft = 1;
ChRight = 2;
% only have 2 channels here so do this for testing...
ChFront = 2;
save('setup.mat');

%% Load counterbalanced test order

% get sentence list order (5 lists total)
testLists = randperm(availableTestLists, numTestLists);

% pre-allocate text array
testConditions = repmat("emptyCondition", numTestLists, 1 ); 

% assign random order of test conditions
% REPLACE THIS WITH LATIN SQUARES!
for i=1:numTestLists
    randNum = randi(4,1);

    switch(randNum)
        case 1
            testConditions(i) = "quiet";
        case 2
            testConditions(i) = "noiseFront";
        case 3
            testConditions(i) = "noiseLeft";
        case 4
            testConditions(i) = "noiseRight";
    end
end



%% start practice condition 
sentences = loadListSentences(practiceList, hintDir);
randOrder = randperm(20);

% store SNR for each sentence
listSNR = zeros(20, 1);
% store hitQuote for each sentence
hitQuotes = zeros(20, 1);

% starting at 0 dB
currentSNR = 0;
noiseIndex = 1;
audioStruct = repmat(tempAudioStruct, 2, 1); 

for i=1:practiceRounds
    % get random index
    index = randOrder(i);
    % load current sentence
    sentencePath = [hintDir '0' int2str(practiceList) '\-0dB\Ger_male00' num2str(index) '.wav'];

    disp(["Current playback level: " int2str(currentSNR)]);
    disp(["Round " int2str(i) " out of " int2str(practiceRounds)]);
    [curr_sent, fs] = loadSentenceAudio(practiceList, index, currentSNR, hintDir);

    sentLen = size(curr_sent, 1);
    [noiseSegment, noiseIndex] = circularNoise(noise, sentLen, noiseIndex);

    audioStruct(1).AudioData = curr_sent;
    audioStruct(1).Channel = ChFront;

    audioStruct(2).AudioData = noiseSegment;

    if practiceCondition == "noiseLeft"
        audioStruct(2).Channel = ChLeft;
    elseif practiceCondition == "noiseRight"
        audioStruct(2).Channel = ChRight;
    elseif practiceCondition == "noiseFront"
        audioStruct(2).Channel = ChFront;
    else
        audioStruct(2).AudioData = 0;
    end

    buffer = combineAudioFiles(audioStruct, sentLen);

    % play current sentence and noise
    playbackID = playrec('play', buffer, ChMap);

    % get length of current sentence
    sentenceLength = numel(strsplit(sentences(index)));

    % print out current sentence string
    disp([sentences(index) sentenceLength]);

    % only prompt this after playback is done
    while ~playrec('isFinished', playbackID) end

    % get experimenter feedback
    prompt = "How many words have been correct?";
    correctWords = input(prompt);
    disp(correctWords);

    % alternative: just ask if below or above 50% hit
    % less data but quicker
    while correctWords > sentenceLength
        disp("Invalid input. Try again!");
        prompt = "How many words have been correct?";
        correctWords = input(prompt);
    end
    disp(['Sentence len: ' int2str(sentenceLength) ' correct: ' int2str(correctWords)]);
    hitQuote = correctWords / sentenceLength;
    disp(hitQuote);

    % store sentence data
    hitQuotes(i) = hitQuote;
    listSNR(i) = currentSNR;

    % adapt SNR based on hitQuote
    if i < 4         
        if hitQuote < 0.5
            currentSNR = currentSNR + 4;
        else
            currentSNR = currentSNR - 4;
        end
    else
        % adapt SNR based on hitQuote
        if hitQuote < 0.5
            currentSNR = currentSNR + 2;
        else
            currentSNR = currentSNR - 2;
        end
    end

    % SNR sanity check
    if currentSNR < minSNR
        currentSNR = minSNR;
        disp(["Warning: reached min SNR!" int2str(minSNR)]);
    elseif currentSNR > maxSNR
        currentSNR = maxSNR;
        disp(["Warning: reached max SNR!" int2str(maxSNR)]);
    end

end

disp("Practice done!");

%% Test JSON format
% create file name based on user name
jsonFile = sprintf("practice-%s.json", name);
% fill struct with list data
s = struct('ListIndex', practiceList, 'Condition', practiceCondition, 'ListSNRs', listSNR, 'ListHitQuotes', hitQuotes);
% parse struct into json
practiceResults = jsonencode(s,PrettyPrint=true);
% store json into file
fid = fopen(jsonFile,'w');
fprintf(fid,'%s', practiceResults);
fclose(fid);


%% Store test data into json file
% parse struct into json
resultJSON = jsonencode(resultStorage,PrettyPrint=true);
% store json into file
fid = fopen(jsonFileName,'w');
fprintf(fid,'%s', resultJSON);
fclose(fid);


%% Test procedure
for j=1:numTestLists

    sentences = loadListSentences(testLists(j), hintDir);
    randOrder = randperm(20);
    currentCondition = testConditions(j);
    
    % store SNR for each sentence
    listSNR = zeros(20, 1);
    % store hitQuote for each sentence
    hitQuotes = zeros(20, 1);
    
    % starting at 0 dB
    currentSNR = 0;
    noiseIndex = 1;

    if testConditions(j) == "noiseLeft"
        audioStruct(2).Channel = ChLeft;
    elseif testConditions(j) == "noiseRight"
        audioStruct(2).Channel = ChRight;   
    elseif testConditions(j) == "noiseFront"
        audioStruct(2).Channel = ChFront;
    end

    disp(["Starting List " int2str(testLists(j)) " with condition" testConditions(j)]);

    for i=1:listSentences
        % get random index
        index = randOrder(i);
        % load current sentence
        sentencePath = [hintDir '0' int2str(testLists(j)) '\-0dB\Ger_male00' num2str(index) '.wav'];
    
        disp(["Current playback level: " int2str(currentSNR)]);
        disp(["Round " int2str(i) " out of " int2str(listSentences)]);
        [curr_sent, fs] = loadSentenceAudio(testLists(j), index, currentSNR, hintDir);
    
        sentLen = size(curr_sent, 1);
        [noiseSegment, noiseIndex] = circularNoise(noise, sentLen, noiseIndex);
    
        audioStruct(1).AudioData = curr_sent;
        audioStruct(1).Channel = ChFront;

        if testConditions(j) ~= "quiet"
            audioStruct(2).AudioData = noiseSegment;
        else
            audioStrcut(2).AudioData = 0;
        end

        buffer = combineAudioFiles(audioStruct, sentLen);
        % play current sentence
        playbackID = playrec('play', curr_sent, ChMap);
    

        % get length of current sentence
        sentenceLength = numel(strsplit(sentences(index)));

        % print out current sentence string
        disp([sentences(index) sentenceLength]);      
        
        % only prompt this after playback is done
        while ~playrec('isFinished', playbackID) end

        % get experimenter feedback
        prompt = "How many words have been correct?";
        correctWords = input(prompt);
        disp(correctWords);
    
        % alternative: just ask if below or above 50% hit
        % less data but quicker
        while correctWords > sentenceLength
            disp("Invalid input. Try again!");
            prompt = "How many words have been correct?";
            correctWords = input(prompt);
        end
        disp(['Sentence len: ' int2str(sentenceLength) ' correct: ' int2str(correctWords)]);
        hitQuote = correctWords / sentenceLength;
        disp(hitQuote);
    
        % store sentence data
        hitQuotes(i) = hitQuote;
        listSNR(i) = currentSNR;
    
        % adapt SNR based on hitQuote
        if i < 4         
            if hitQuote < 0.5
                currentSNR = currentSNR + 4;
            else
                currentSNR = currentSNR - 4;
            end
        else
            % adapt SNR based on hitQuote
            if hitQuote < 0.5
                currentSNR = currentSNR + 2;
            else
                currentSNR = currentSNR - 2;
            end
        end
    
        % SNR sanity check
        if currentSNR < minSNR
            currentSNR = minSNR;
            disp(["Warning: reached min SNR!" int2str(minSNR)]);
        elseif currentSNR > maxSNR
            currentSNR = maxSNR;
            disp(["Warning: reached max SNR!" int2str(maxSNR)]);
        end
    
    end

    disp(["List" int2str(j) " out of" int2str(numTestLists) " done!"]);

    % store data in resultStorage
    resultStorage(j).ListIndex = testLists(j);
    resultStorage(j).Condition = testConditions(j);
    resultStorage(j).ListSNRs = listSNR;
    resultStorage(j).ListHitQuotes = hitQuotes;
end  
   
%% Write results into file
% parse struct into json
results = jsonencode(resultStorage,PrettyPrint=true);
% store json into file
fid = fopen(jsonFile,'w');
fprintf(fid,'%s', results);
fclose(fid);

       


