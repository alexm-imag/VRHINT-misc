
function buffer = combineAudioFiles(audioStruct, buflen)
    
    buffer = zeros(buflen, max([audioStruct.Channel]));
    %nonZeroChannels = zeros(max([audioStruct.Channel]));

    for i=1:size(audioStruct)

        % check for channel dublications
        %nonZeroChannels(i) = audioStruct(i).Channel;
        if max(buffer(:,audioStruct(i).Channel)) > 0
            buffer(:,audioStruct(i).Channel) = buffer(:,audioStruct(i).Channel) + audioStruct(i).AudioData(1:(min(buflen, size(audioStruct(i).AudioData, 1))));

            if max(buffer(:,audioStruct(i).Channel)) > 1
                disp(["Warning: Clipping on channel " audioStruct(i).Channel]);
            end
        else
            buffer(:,audioStruct(i).Channel) = audioStruct(i).AudioData(1:(min(buflen, size(audioStruct(i).AudioData, 1))));
        end
    end