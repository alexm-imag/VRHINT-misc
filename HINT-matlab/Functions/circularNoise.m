
function noiseBuf = circularNoise(noise, len)

    persistent nLen;
    persistent noiseIndex;

    noiseLen = size(noise(:,1));

    if isempty(nLen)
        nLen = 0;
        noiseIndex = 1;
    end

    if nLen ~= noiseLen
        nLen = noiseLen;
        % reset noiseIndex if a new noise was submitted!
        noiseIndex = 1;
        disp("New nosie file detected");
    end

    noiseBuf = noise;

    % circ case
    if noiseIndex + len > noiseLen
        noiseBuf(1: len - noiseIndex) = noise(noiseIndex:noiseLen);
        noiseBuf(len - noiseIndex) = nnoise(1:len - (noiseLen - noiseIndex));
        noiseIndex = len - (noiseLen - noiseIndex);
    else
        noiseBuf = noise(noiseIndex:noiseIndex + len);
        noiseIndex = noiseIndex + len;
    end

    %disp(["Len: " len " noiseInd: " noiseIndex]);