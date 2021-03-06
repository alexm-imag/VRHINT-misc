
function [noiseBuf, noiseIndex] = circularNoise(noise, len, noiseIndex)

    persistent nLen;
    %persistent noiseIndex;

    noiseLen = size(noise(:,1));

    if isempty(nLen)
        nLen = 0;
    %    noiseIndex = 1;
    end

    if nLen ~= noiseLen
        nLen = noiseLen;
        % reset noiseIndex if a new noise was submitted!
        noiseIndex = 1;
        disp("New noise file detected");
    end

    noiseBuf = noise;
    disp(["Len: " len " noiseInd: " noiseIndex " noiseLen: " noiseLen]);

    % circ case
    if noiseIndex + len > noiseLen
        disp("Circ overflow");
        disp(["nL - NI+1: " length(1:noiseLen - noiseIndex+1) " nI:NL " length(noiseIndex:noiseLen)])
        noiseBuf(1: noiseLen - noiseIndex + 1) = noise(noiseIndex:noiseLen);
        disp(["nL - NI+1: " length(noiseLen - noiseIndex + 1:len) " nI:NL " length(1:len - (noiseLen - noiseIndex))])
        noiseBuf(noiseLen - noiseIndex + 1:len) = noise(1:len - (noiseLen - noiseIndex));
        noiseIndex = len - (noiseLen - noiseIndex);
    else
        noiseBuf = noise(noiseIndex:noiseIndex + len);
        noiseIndex = noiseIndex + len;
    end

    disp(["Post noiseInd: " noiseIndex]);