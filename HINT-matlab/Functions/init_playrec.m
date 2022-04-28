%%
%% init_playrec(fs)
% Initialize playrec for the current setup
% Input: 
% sampling freq

% Dependencies: playrec.mexw64 

function init_playrec(fs)

    if playrec('isInitialised')
        playrec('reset');
    end

    dev = playrec('getDevices');
    % Check installed ASIO drivers etc. if this fails!
    if length(dev) < 1
        disp("Warning: Playrec found no matching audio device!");
    else
        disp([length(dev) " audio devices found"]);
    end

    playrec('init',fs,0,0)

    disp('Playrec successfully initialized!')
end

