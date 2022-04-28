%% Helper function to play multiple audio files at once through playrec
% - data: contains mono audio files
% - channels: contains to channel assignment for each audio file
% - length: holds to total playback length 
%           (get this by using audioLen = size(curr_sent, 1))
%  - totalChannels: the number of channels initialized for playrec

function buffer = createAudioBuffer(bufLen, data1, data1Chn, data2, data2Chn, nChannels)
        
        buffer = zeros(bufLen, nChannels);

        if size(data2(:,1)) < bufLen
            bufLen = size(data2(:,1));
        end
               
        if data1Chn == data2Chn
            buffer(:,data2Chn) = data2(1:min(bufLen, size(data2(:,1)))) + data1(1:min(bufLen, size(data1(:,1))));
            % clip warning
            if max(abs(buffer(:,data2Chn)) > 1)
                disp(["Warning: Clipping on channel " data2Chn]);
            end
        else
            buffer(:,data1Chn) = data1(1:min(bufLen, size(data1(:,1))));
            buffer(:,data2Chn) = data2(1:min(bufLen, size(data2(:,1))));
        end