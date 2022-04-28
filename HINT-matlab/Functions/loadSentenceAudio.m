function [sent, fs] = loadSentenceAudio(listIndex, sentenceIndex, dbLevel, hintDir)

    if listIndex < 10
        audioPath = [hintDir '0' int2str(listIndex)]; 
    else
        audioPath = [hintDir int2str(listIndex)]; 
    end

    if dbLevel == 0
        audioPath = [audioPath '\-' int2str(dbLevel) 'dB'];
    elseif dbLevel > 0
        audioPath = [audioPath '\+' int2str(dbLevel) 'dB'];
    else
        audioPath = [audioPath '\' int2str(dbLevel) 'dB'];
    end

    sentenceNum = sentenceIndex + (listIndex - 1) * 20;

    if sentenceNum < 10
        audioPath = [audioPath '\Ger_male00' num2str(sentenceNum) '.wav'];
    elseif sentenceNum < 100
        audioPath = [audioPath '\Ger_male0' num2str(sentenceNum) '.wav'];
    else
        audioPath = [audioPath '\Ger_male' num2str(sentenceNum) '.wav'];
    end

    disp(audioPath);
    [sent, fs] = audioread(audioPath);

end

