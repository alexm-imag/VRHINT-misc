function sentences = loadListSentences(listIndex, hintDir)
    
    if listIndex < 10
        filePath = [hintDir '\0' int2str(listIndex) '\list' int2str(listIndex) '.txt'];
    else
        filePath = [hintDir '\' int2str(listIndex) '\list' int2str(listIndex) '.txt'];
    end

    sentences = readlines(filePath);
